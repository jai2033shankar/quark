from collections import OrderedDict

from quarkc.match import match, many, choice, lazy
from quarkc.ast import (
    AST, Field, Param, Declaration, Package, File, Function, Primitive, Class, Interface, TypeParam, Method, Local
)
from quarkc.compiler import Compiler
from quarkc.symbols import Self

###############################################################################
# Check that a given file/content produces the expected symbols or errors
###############################################################################

@match(AST)
def dfn_sig(n):
    return n.__class__, n.name.text

@match(choice(Field, Param))
def dfn_sig(n):
    return n.__class__, n.name.text

@match(Declaration)
def dfn_sig(n):
    return n.parent.__class__, n.name.text

@match([Package, many(Package)])
def dfn_sig(pkgs):
    pkg = pkgs[0]
    result = pkg.name.text
    for p in pkgs[1:]:
        assert p.name.text == result
    if pkg.name.text == "f":
        return File, result
    else:
        return pkg.__class__, result

def check(name, content, expected=None, duplicates=(), missing=()):
    c = Compiler()
    c.parse(name, content)
    c.check_symbols()
    assert set(duplicates) == set(c.symbols.duplicates)
    assert set(missing) == set(c.symbols.missing.values())
    if expected is not None:
        elided = {}
        for k, v in c.symbols.definitions.items():
            elided[k] = dfn_sig(v)
        assert expected == elided

###############################################################################


###############################################################################
# Utilities for generating input code that covers the many
# permutations of symbols and/or symbol conflicts possible
###############################################################################

TOP = [File, Package, Class, Function]
CHILDREN = {File: (Package, Function, Class, Interface),
            Package: (Package, Function, Class, Interface),
            Interface: (TypeParam, Field, Method),
            Class: (TypeParam, Field, Method),
            Function: (Param, Local),
            Method: (Param, Local)}

@match(basestring)
def block(code):
    if code:
        return "{\n    " + code.replace("\n", "\n    ").rstrip() + "\n}"
    else:
        return "{}"

class SymbolTree(object):

    @match(choice(File, Package, Function, Class, Interface, Method, Field, Local, TypeParam, Param))
    def __init__(self, type):
        self.type = type
        # map of name to a list of child trees
        self.children = OrderedDict()

    @match(basestring, many(lazy("SymbolTree"), min=1))
    def add(self, name, *subtrees):
        if name in self.children:
            children = self.children[name]
        else:
            children = []
            self.children[name] = children
        children.extend(subtrees)

    @match(many(type, min=1))
    def get(self, *types):
        subtrees = [(name, tree) for name in self.children for tree in self.children[name] if tree.type in types]
        return tuple([tree.code(name) for name, tree in subtrees])

    @match(basestring)
    def code(self, name):
        return self.assemble(self.type, name)

    @match(choice(Function, Method), basestring)
    def assemble(self, _, name):
        return "T {name}({params}) {body}".format(name=name, params=", ".join(self.get(Param)),
                                                  body=block("\n".join(self.get(Local))))

    @match(choice(Class, Interface), basestring)
    def assemble(self, t, name):
        tparams = self.get(TypeParam)
        if tparams:
            params = "<%s>" % ", ".join(tparams)
        else:
            params = ""
        definitions = self.get(*[c for c in CHILDREN[t] if c != TypeParam])
        return "{kw} {name}{params} {body}".format(kw="interface" if t == Interface else "class",
                                                   name=name, params=params,
                                                   body=block("\n".join(definitions)))

    @match(TypeParam, basestring)
    def assemble(self, _, name):
        return name

    @match(Param, basestring)
    def assemble(self, _, name):
        return "T %s" % name

    @match(choice(Local, Field), basestring)
    def assemble(self, _, name):
        return "T %s;" % name

    @match(Package, basestring)
    def assemble(self, t, name):
        return "namespace {name} {body}".format(name=name, body=block("\n".join(self.get(*CHILDREN[t]))))

    @match(File, basestring)
    def assemble(self, t, name):
        definitions = "\n".join(self.get(*CHILDREN[t]))
        return "quark 1.0;\n\npackage {name} 1.2.3;\n\n{definitions}".format(name=name, definitions=definitions)

    def nodes(self):
        yield self
        for trees in self.children.values():
            for tree in trees:
                for n in tree.nodes():
                    yield n

    def symbols(self, filename, name):
        if self.type in (File, Package):
            path = (name,)
        else:
            path = (filename, name)
            yield filename, (Package, filename)

        for sym, sig in self.symbols_r(path):
            yield sym, sig

    def symbols_r(self, path):
        yield ".".join(path), (Package if self.type == File else self.type, path[-1])
        if self.type == Class:
            yield ".".join(path + (path[-1],)), (Method, path[-1])
        if self.type == Method and self.children:
            yield ".".join(path + ("self",)), (Self, path[-2])
        for name, trees in self.children.items():
            for tree in trees:
                if self.type == File and tree.type == Package:
                    extended = (name,)
                else:
                    extended = path + (name,)
                for sym, sig in tree.symbols_r(extended):
                    yield sym, sig

class Namer(object):

    def __init__(self, prefix, suffix=""):
        self.prefix = prefix
        self.suffix = suffix
        self.count = 0

    def __call__(self):
        result = "%s%s%s" % (self.prefix, self.count, self.suffix)
        self.count = self.count + 1
        return result

@match(type, Namer, int)
def symtree(type, namer, depth):
    tree = SymbolTree(type)
    if depth > 0 and type in CHILDREN:
        types = CHILDREN[type]
        names = (namer() for t in CHILDREN[type])
        for name, t in zip(names, types):
            tree.add(name, symtree(t, namer, depth - 1))
    return tree

###############################################################################


###############################################################################
# Tests
###############################################################################

def test_implicit_foobar():
    check("asdf", """
    quark 1.0;
    void foo() {}
    void bar() {}
    """,
    {
        "asdf.foo": (Function, "foo"),
        "asdf.bar": (Function, "bar"),
        "asdf": (Package, "asdf")
    }, missing=["void"])

def test_implicit_foofoo():
    check("asdf", """
    quark 1.0;
    void foo() {}
    void foo() {}
    """,
    duplicates=["asdf.foo"],
    missing=["void"])


def test_explicit_foobar():
    check("asdf", """
    quark 1.0;

    namespace ns {
        void foo() {}
        void bar() {}
    }
    """,
    {
        "ns.foo": (Function, "foo"),
        "ns.bar": (Function, "bar"),
        "ns": (Package, "ns")
    },
    missing=['void'])

def test_explicit_foofoo():
    check("asdf", """
    quark 1.0;

    namespace ns {
        void foo() {}
        void foo() {}
    }
    """,
    duplicates=["ns.foo"],
    missing=["void"])

def symerr(filename, topname, tree):
    expected = {}
    dups = []
    for sym, sig in tree.symbols(filename, topname):
        if sym in expected:
            prev = expected[sym]
            if prev[0] != Package or sig[0] != Package:
                dups.append(sym)
        else:
            expected[sym] = sig
    return expected, dups

def test_permutations():
    fname = "fname"
    topname = "asdf"
    depth = 5
    for t in TOP:
        tree = symtree(t, Namer("n"), depth)
        expected, dups = symerr(fname, topname, tree)
        assert not dups
        check(fname, tree.code(topname), expected, missing=['T'])

def test_collisions():
    fname = "fname"
    topname = "asdf"
    depth = 5
    for t in TOP:
        tree = symtree(t, Namer("name_", "_"), depth)
        for nd in tree.nodes():
            for name in nd.children:
                nd.add(name, *[SymbolTree(c) for c in CHILDREN[nd.type]])
        expected, dups = symerr(fname, topname, tree)
        check(fname, tree.code(topname), duplicates=dups, missing=['T'])

def test_missing_type1():
    check("missing_type", """
    void foo() {}
    """, missing=["void"])

def test_missing_type2():
    check("missing_type", """
    primitive void {}
    void foo() {
        Foo x;
    }
    """, missing=["Foo"])

def test_missing_type2():
    check("missing_type", """
    primitive void {}
    void foo(Foo y) {
    }
    """, missing=["Foo"])

def test_missing_type3():
    check("missing_type", """
    class Foo {
        Bar field;
    }
    """, missing=["Bar"])

def test_missing_var1():
    check("missing_var", """
    primitive void {}
    void foo() {
        bar;
    }
    """, missing=["bar"])

def test_missing_var2():
    check("missing_var", """
    primitive void {}
    void foo() {
        bar();
    }
    """, missing=["bar"])

def test_missing_var3():
    check("missing_var", """
    primitive void {}
    void foo() {
        foo(bar);
    }
    """, missing=["bar"])

def test_missing_string1():
    check("missing_string", """
    primitive void {}
    void foo() {
        "asdf";
    }
    """, missing=["String"])

def test_missing_string2():
    check("missing_string", """
    primitive void {}
    void foo() {
        foo("asdf");
    }
    """, missing=["String"])

def test_missing_int1():
    check("missing_int", """
    primitive void {}
    void foo() {
        1;
    }
    """, missing=["int"])

def test_missing_int2():
    check("missing_int", """
    primitive void {}
    void foo() {
        foo(1);
    }
    """, missing=["int"])

def test_missing_float1():
    check("missing_int", """
    primitive void {}
    void foo() {
        1.0;
    }
    """, missing=["float"])

def test_missing_float2():
    check("missing_int", """
    primitive void {}
    void foo() {
        foo(1.0);
    }
    """, missing=["float"])

def test_missing_bool1():
    check("missing_bool", """
    primitive void {}
    void foo() {
        true;
    }
    """, missing=["bool"])

def test_missing_bool2():
    check("missing_bool", """
    primitive void {}
    void foo() {
        false;
    }
    """, missing=["bool"])

def test_missing_bool3():
    check("missing_bool", """
    primitive void {}
    void foo() {
        if (foo()) {}
    }
    """, missing=["bool"])

def test_missing_bool4():
    check("missing_bool", """
    primitive void {}
    void foo() {
        while (foo()) {}
    }
    """, missing=["bool"])

def test_nesting():
    check("nesting", """
    primitive int {}
    primitive bool {}
    int foo() {
        int a;
        if (a) {
           int b = c;
           int d = 1;
           int d = 2;
        }

        while(a) {
           int e = a;
        }
    }
    """,
    expected={"nesting": (Package, "nesting"),
              "nesting.foo": (Function, "foo"),
              "nesting.foo.a": (Local, "a"),
              "nesting.foo.b": (Local, "b"),
              "nesting.foo.d": (Local, "d"),
              "nesting.foo.e": (Local, "e"),
              "nesting.int": (Primitive, "int"),
              "nesting.int.int": (Method, "int"),
              "nesting.bool": (Primitive, "bool"),
              "nesting.bool.bool": (Method, "bool")},
    duplicates=["nesting.foo.d"], missing=["c"])

def test_import():
    check("import", """
    package quark {
        primitive void {}
    }

    package a {
        void foo() {}
    }

    import a;

    package b {
        void bar() {
            foo();
        }
    }
    """)

def test_self():
    check("f", """
    package quark {
        primitive void {}
        primitive int {}
    }

    class C {
        int field = 0;
        void meth() {
            self;
        }
    }
    """,
    expected={
        'f': (File, 'f'),
        'f.C': (Class, 'C'),
        'f.C.C': (Method, 'C'),
        'f.C.field': (Field, 'field'),
        'f.C.meth': (Method, 'meth'),
        'f.C.meth.self': (Self, 'C'),
        'quark': (Package, 'quark'),
        'quark.int': (Primitive, 'int'),
        'quark.int.int': (Method, 'int'),
        'quark.void': (Primitive, 'void'),
        'quark.void.void': (Method, 'void')
    })

def test_selfdup():
    check("f", """
    package quark {
        primitive void {}
        primitive int {}
    }

    class C {
        int field = 0;
        void meth() {
            int self = 0;
        }
    }
    """,
    expected={
        'f': (File, 'f'),
        'f.C': (Class, 'C'),
        'f.C.C': (Method, 'C'),
        'f.C.field': (Field, 'field'),
        'f.C.meth': (Method, 'meth'),
        'f.C.meth.self': (Self, 'C'),
        'quark': (Package, 'quark'),
        'quark.int': (Primitive, 'int'),
        'quark.int.int': (Method, 'int'),
        'quark.void': (Primitive, 'void'),
        'quark.void.void': (Method, 'void')
    },
    duplicates=["f.C.meth.self"])

###############################################################################
