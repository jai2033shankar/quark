# Copyright 2015 datawire. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from collections import OrderedDict
from .match import match, many, choice
from .ir import Definition, Name, Ref, Invoke, Class, Interface, Function, Check, Invoke, Void, Block
from .ir import dfn_of
from . import tr

class TargetNamespace(object):
    """ Name of an importable namespace/package in the target """
    @match((many(basestring),))
    def __init__(self, target_name):
        self.target_name = target_name
        self.names = OrderedDict()
        self.target_names = OrderedDict()

    def __repr__(self):
        return "TargetNamespace(%s, %s, %s)" % (self.target_name, self.names, self.target_names)

class TargetDefinition(object):
    """ Name of a ir.Definition in the target """
    @match(basestring, TargetNamespace)
    def __init__(self, target_name, namespace):
        self.target_name = target_name
        self.namespace = namespace

    def __repr__(self):
        return "TargetDefinition(%s, %s)" % (self.namespace.target_name, self.target_name)

class Target(object):

    def __init__(self, parent=None):
        self.parent = parent
        if parent:
            self.depth = parent.depth + 1
        else:
            self.depth = 0
        self.files = OrderedDict()
        self.modules = OrderedDict()
        self.definitions = OrderedDict()

    @match(Definition)
    def define(self, dfn):
        """Install a mapping in self.definitions[dfn.name] -> AllRequiredInfoOnTargetName"""
        tgt_namespace = self.define_namespace(dfn)
        tgt_def = self.define(tgt_namespace, dfn)
        tgt_def.namespace.names[dfn.name] = tgt_def
        self.definitions[dfn.name] = tgt_def
        return tgt_def

    @match(tr.File, basestring)
    def file(self, module, contents):
        name = module.filename
        if name not in self.files:
            self.files[name] = ""
        self.files[name] += contents

    @match(TargetNamespace, Definition)
    def define(self, namespace, dfn):
        """ return a TargetDefinition inside the TargetNamespace for a given ir.Definition """
        assert False, "%s does not have define(TargetNamespace, Definition)" % self.__class__.__name__

    @match(TargetNamespace, basestring)
    def define_name(self, namespace, defname):
        assert defname
        target_name = self.UNKEYWORDS.get(defname, defname)
        assert target_name
        target_name = target_name
        assert target_name not in namespace.target_names
        namespace.names[defname] = target_name
        namespace.target_names[target_name] = defname
        return target_name

    @match(Definition)
    def define_namespace(self, dfn):
        """ return a TargetNamespace for a given ir.Definition and install it in self.definitions"""
        assert False, "%s does not have define_namespace(Definition)" % self.__class__.__name__

    @match(Definition)
    def module(self, dfn):
        """ REWORD: Return or create a tr.File for a target as previously defined with a TargetNamespace and TargetDefinition """
        tgtdfn = self.definitions[dfn.name]
        filename = self.filename(dfn, tgtdfn)
        if filename not in self.modules:
            module = tr.File(filename)
            self.header(dfn, module)
            self.modules[filename] = module
        return self.modules[filename]

    @match(Definition, tr.File)
    def header(self, dfn, module):
        module.add(tr.Comment("Quark %s backend generated code. override header() for a better comment" % self.__class__.__name__))

    @match(Definition, Ref)
    def reference(self, dfn, ref):
        assert dfn.name in self.definitions
        if ref not in self.definitions:
            self.define_ffi(ref.parent)
        assert ref in self.definitions
        tgtdfn = self.definitions[dfn.name]
        tgtref = self.definitions[ref]
        module = self.module(dfn)
        if ref not in tgtdfn.namespace.names:
            self.reference(module, dfn, tgtdfn, ref, tgtref)
        assert ref in tgtdfn.namespace.names, "%s.reference() does not install into target namespace" % self.__class__.__name__

    @match(tr.File, Definition, TargetDefinition, Ref, TargetDefinition)
    def reference(self, module, dfn, tgtdfn, ref, tgtref):
        """ generate the import statement and store import name in the tgtdfn namespace """
        assert False, "TODO: add import logic for %s" % self.__class__.__name__

    @match(Invoke)
    def define_ffi(self, invoke):
        self.define(Function(Name(invoke.name.package, *invoke.name.path), Void(), Block()))

    @match(Name)
    def nameof(self, name):
        return self.definitions[name].target_name

    @match(Ref)
    def nameof(self, ref):
        assert ref in self.definitions
        dfn = dfn_of(ref)
        assert dfn.name in self.definitions
        tgtdfn = self.definitions[dfn.name]
        assert ref in tgtdfn.namespace.names
        return tgtdfn.namespace.names[ref]

    @match(basestring)
    def upcase(self, s):
        return s[0:1].capitalize() + s[1:]

class Snowflake(str):
    def __eq__(self, other):
        return type(self) is type(other) and str(self) == str(other)

    def __hash__(self):
        return hash(str(self))

class Java(Target):

    UNKEYWORDS = dict((k, k+"_") for k in
                      """
                      abstract    continue        for             new             switch
                      assert      default         goto            package         synchronized
                      boolean     do              if              private         this
                      break       double          implements      protected       throw
                      byte        else            import          public          throws
                      case        enum            instanceof      return          transient
                      catch       extends         int             short           try
                      char        final           interface       static          void
                      class       finally         long            strictfp        volatile
                      const       float           native          super           while

                      null        true            false 

                      Functions   Tests""".split())

    @match(TargetNamespace, Definition)
    def define(self, namespace, dfn):
        target_name = self.define_name(namespace, dfn.name.path[-1])
        return TargetDefinition(target_name, namespace)

    @match(choice(Class, Interface))
    def define_namespace(self, dfn):
        return self.define_namespace(dfn, dfn.name.path)

    @match(Function)
    def define_namespace(self, dfn):
        return self.define_namespace(dfn.name.path[:-1] + (Snowflake("Functions"),))

    @match(Check)
    def define_namespace(self, dfn):
        return self.define_namespace(dfn.name.path[:-1] + (Snowflake("Tests"),))

    @match((many(basestring, min=1),))
    def define_namespace(self, path):
        if path not in self.definitions:
            parent = self.define_namespace(path[:-1])
            target_name = self.define_name(parent, path[-1])
            # XXX: here we can inject additional implementation namespace
            self.definitions[path] = TargetNamespace(parent.target_name + (target_name, ))
        return self.definitions[path]

    @match(())
    def define_namespace(self, path):
        # XXX: as a consequence, we don't check for duplicates of
        # toplevel namespace names because we don't store root, should that be prohibited by the IR anyways?
        return TargetNamespace(())

    @match(Definition, TargetDefinition)
    def filename(self, dfn, tgtdfn):
        return "/".join(("src", "main", "java") + tgtdfn.namespace.target_name) + ".java"

    @match(Check, TargetDefinition)
    def filename(self, dfn, tgtdfn):
        return "/".join(("src", "test", "java") + tgtdfn.namespace.target_name) + ".java"

    @match(tr.File, Definition, TargetDefinition, Ref, TargetDefinition)
    def reference(self, module, dfn, tgtdfn, ref, tgtref):
        # Java fully qualifies all references, imports are not necessary
        tgtdfn.namespace.names[ref] = ".".join(tgtref.namespace.target_name + (tgtref.target_name, ))
        pass

class Python(Target):

    UNKEYWORDS = dict((k, k+"_") for k in """self map list None True False""".split())

    @match(TargetNamespace, Definition)
    def define(self, namespace, dfn):
        target_name = self.define_name(namespace, dfn.name.path[-1])
        return TargetDefinition(target_name, namespace)

    @match(Definition)
    def define_namespace(self, dfn):
        return self.define_namespace(dfn.name.path)

    @match(Check)
    def define_namespace(self, dfn):
        return self.define_namespace(dfn.name.path[:-1] + ("test_" + dfn.name.path[-2],))

    @match((many(basestring, min=1),))
    def define_namespace(self, path):
        if path not in self.definitions:
            parent = self.define_namespace(path[:-1])
            target_name = self.define_name(parent, path[-1])
            # XXX: here we can inject additional implementation namespace
            self.definitions[path] = TargetNamespace(parent.target_name + (target_name, ))
        return self.definitions[path]

    @match(())
    def define_namespace(self, path):
        # XXX: as a consequence, we don't check for duplicates of
        # toplevel namespace names because we don't store root, should that be prohibited by the IR anyways?
        return TargetNamespace(())

    @match(Definition, TargetDefinition)
    def filename(self, dfn, tgtdfn):
        return "/".join(tgtdfn.namespace.target_name) + ".py"

    @match(tr.File, Definition, TargetDefinition, Ref, TargetDefinition)
    def reference(self, module, dfn, tgtdfn, ref, tgtref):
        ref_module = ".".join(tgtref.namespace.target_name)
        ref_module_name = "_".join(tgtref.namespace.target_name)

        tgtdfn.namespace.names[ref] = ".".join((ref_module_name, tgtref.target_name))

        module.add(tr.Simple("import {ref_module} as {ref_module_name}".format(
            ref_module = ref_module, ref_module_name = ref_module_name)))

class Ruby(Target):

    UNKEYWORDS = dict((k, k+"_") for k in
    """ BEGIN END __ENCODING__ __END__ __FILE__ __LINE__ alias and begin
         break case class def defined?  do else elsif end ensure false
         for if in module next nil not or redo rescue retry return
         self super then true undef unless until when while yield
    """.split())

    @match(TargetNamespace, Definition)
    def define(self, namespace, dfn):
        target_name = self.define_name(namespace, self.upcase(dfn.name.path[-1]))
        return TargetDefinition(target_name, namespace)

    @match(Definition)
    def define_namespace(self, dfn):
        return self.define_namespace(dfn.name.path[:-1])

    @match(Check)
    def define_namespace(self, dfn):
        return self.define_namespace(dfn.name.path[:-2] + ("tc_" + dfn.name.path[-2],))

    @match((many(basestring, min=1),))
    def define_namespace(self, path):
        if path not in self.definitions:
            parent = self.define_namespace(path[:-1])
            target_name = self.define_name(parent, self.upcase(path[-1]))
            self.definitions[path] = TargetNamespace(parent.target_name + (target_name, ))
        return self.definitions[path]

    @match(())
    def define_namespace(self, path):
        return TargetNamespace(())

    @match(Definition, TargetDefinition)
    def filename(self, dfn, tgtdfn):
        return "/".join(("lib", dfn.name.package) + tgtdfn.namespace.target_name) + ".rb"

    @match(Check, TargetDefinition)
    def filename(self, dfn, tgtdfn):
        return "/".join(("test", dfn.name.package) + tgtdfn.namespace.target_name) + ".rb"

    @match(tr.File, Definition, TargetDefinition, Ref, TargetDefinition)
    def reference(self, module, dfn, tgtdfn, ref, tgtref):
        """ generate the import statement and store import name in the target namespace """
        tgtdfn.namespace.names[ref] = ".".join(tgtref.namespace.target_name + (tgtref.target_name, ))
        module.add(tr.Simple("# TODO: add import logic for %s" % self.__class__.__name__))

class Go(Target):

    """Toplevel quark namespace maps to go package, the nested quark
       namespaces are flattened as part of identifier names to work
       around package cycle issues """

    UNKEYWORDS = dict((k, k+"_") for k in
                      """
                      break        default      func         interface    select
                      case         defer        go           map          struct
                      chan         else         goto         package      switch
                      const        fallthrough  if           range        type
                      continue     for          import       return       var""".split())


    @match(Definition)
    def define_namespace(self, dfn):
        return self.define_namespace((dfn.name.path[0], ))

    @match(TargetNamespace, Definition)
    def define(self, namespace, dfn):
        target_name = self.define_name(namespace, self.upcase("_".join(dfn.name.path[1:])))
        return TargetDefinition(target_name, namespace)

    @match((many(basestring, min=1),))
    def define_namespace(self, path):
        if path not in self.definitions:
            parent = self.define_namespace(path[:-1])
            target_name = self.define_name(parent, path[-1])
            self.definitions[path] = TargetNamespace(parent.target_name + (target_name, ))
        return self.definitions[path]

    @match(())
    def define_namespace(self, path):
        # XXX: as a consequence, we don't check for duplicates of
        # toplevel namespace names because we don't store root, should that be prohibited by the IR anyways?
        return TargetNamespace(())

    @match(Definition, TargetDefinition)
    def filename(self, dfn, tgtdfn):
        return "/".join((dfn.name.package,) + tgtdfn.namespace.target_name + (tgtdfn.target_name.lower(),)) + ".go"

    @match(Check, TargetDefinition)
    def filename(self, dfn, tgtdfn):
        return "/".join((dfn.name.package,) + tgtdfn.namespace.target_name + (tgtdfn.target_name.lower() + "_test",)) + ".go"

    @match(tr.File, Definition, TargetDefinition, Ref, TargetDefinition)
    def reference(self, module, dfn, tgtdfn, ref, tgtref):
        tgtdfn.namespace.names[ref] = ".".join(tgtref.namespace.target_name + (tgtref.target_name, ))

