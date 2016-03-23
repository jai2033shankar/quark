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

import itertools
from collections import OrderedDict
from .helpers import *

lower = lambda name: name[0].lower() + name[1:]
upper = lambda name: name[0].upper() + name[1:]

class Templates:

    method = """\
def {name}({parameters})
    {body}

    nil
end
""".format

    method_call = '{receiver}.{method}({args})'.format

    gemspec = """\
Gem::Specification.new do |spec|
  spec.name        = '{name}'
  spec.version     = '{version}'
  spec.summary     = 'Quark generated {name}'
  # spec.description = ''
  spec.author      = 'Quark compiled code'
  # spec.email       = ''
  # spec.license     = ''
  spec.files       = ['{files}']
  # spec.homepage    = ''
{runtime_deps}
end
""".format

    runtime_dep = """\
  spec.add_runtime_dependency '{module}', '= {version}'\
""".format

    class_ = """\
def self.{alias}; {name}; end
class {name} < {base}
    {prologue}

    {constructors}

    {methods}
end
{name}.unlazy_statics
""".format

## Packaging

def package(name, version, packages, srcs, deps):
    # TODO handle deps
    files = OrderedDict()
    files.update(("lib/%s" % k, v) for k, v in srcs.iteritems())
    paths = files.keys()
    for path, readme in packages.items():
        files['lib/%s/README.md' % '/'.join(path)] = readme
    gemspec = Templates.gemspec(
        name=name,
        version=version,
        runtime_version='TODO',
        files="', '".join(paths),
        runtime_deps="\n".join(Templates.runtime_dep(module=d[1],version=d[2])
                                for d in deps)
    )
    files['%s.gemspec' % (name)] = gemspec
    return files

def class_file(path, name, fname):
    assert path
    return '/'.join(path) + '.rb'

def function_file(path, name, fname):
    return class_file(path, name, fname)

def package_file(path, name, fname):
    return None

def _make_file(path):
    epilogue = 'def self.{alias}; {name}; end\nmodule {name}\n'.format
    prologue = 'end # module {name}\n'.format
    names = [name.replace('-', '_') for name in path]
    head = ''
    # head += 'puts "begin loading module %s"\n' % ".".join(path)
    if tuple(path) == ('builtin',):
        head += 'require_relative "datawire-quark-core"\n'
    head += ''.join(epilogue(name='MODULE_' + name, alias=name) for name in names)
    tail = ''.join(prologue(name='MODULE_' + name) for name in reversed(names))
    # tail += 'puts "end loading module %s"\n' % ".".join(path)
    return Code(head='module Quark\n' + head, tail=tail + 'end # module Quark')

def make_class_file(path, name):
    return _make_file(path)

def make_function_file(path, name):
    return _make_file(path)

def make_package_file(path, name):
    assert False

def main(fname, common):
    template = 'require_relative "{file}"\n\nQuark.{path}.main\n'.format
    return Code(template(file=common.replace('-', '_') + '.rb',
                         path=common.replace('-', '_')))

## Naming and imports

SUBS = {'Class': 'QuarkClass', 'end': 'end_', 'next': 'next_'}
def name(n):
    return SUBS.get(n, n).replace('-', '_')

def type(path, name, parameters):
    return ".".join(path + [name])

def import_(path, origin, dep, cache={}):
    if dep is None:
        # common 'directories'
        common = len(tuple(itertools.takewhile(
            lambda p: p[0]==p[1], zip(path[:-1], origin[:-1]))))
        # uncommon path directories
        lpath = path[common:-1]
        # uncommon origin directories
        lorigin = origin[common:-1]
        # go up and down and load the file
        rpath = "/".join(('..',) * len(lorigin) + lpath + path[-1:])
        require = "require_relative '%s' # %s %s %s" % (rpath, common, lpath, lorigin)
        if origin == ('builtin_md',) and path != ('builtin', 'reflect', ):
            # XXX: why does quark think that builtin_md depends on builtin.concurrent and builtin.behavior ???
            require = "# for builtin_md: " + require
        return require
    else:
        if len(origin) == 1:
            if len(path) == 1:
                return "require '%s' " % path[0]
            else:
                return "require '%s' # .../%s" % (path[0], "/".join(path[1:]))
        else:
            return "require '%s' # .../%s %s" % (path[0], "/".join(path[1:]), "/".join(origin))

def qualify(package, origin):
    # Always fully-qualify names, because Ruby is not fully lexically-scoped.
    return package

## Documentation

def doc(lines):
    return doc_helper(lines, '#  ', '#  ', '#  ')

## Comments

def comment(stuff):
    return '# %s\n' % stuff

## Class definition

def clazz(doc, abstract, name, parameters, base, interfaces, static_fields, fields, constructors, methods):
    prologue = 'attr_accessor %s' % ', '.join(':' + name for name, value in fields)
    prologue += indent('extend DatawireQuarkCore::Static\n')
    if static_fields:
        prologue += indent('\n'.join(static_fields))
        
    init_fields = Templates.method(
        name='__init_fields__',
        parameters='',
        body=indent(''.join('\nself.%s = %s' % pairs for pairs in fields)),
    )
    source = Templates.class_(
        name='CLASS_' + name,
        alias=name,
        base=('::Quark.' + base) if base else 'Object',
        prologue=prologue,
        constructors=indent('\n'.join(constructors)),
        methods=indent('\n'.join(methods + [init_fields])),
    )
    return source

def static_field(doc, clazz, type, name, value):
    return "static {name}: -> {{ {value} }}".format(name=name, value=value or 'nil')

def field(doc, clazz, type, name, value):
    return (name, value or null())

def field_init():
    return 'self.__init_fields__'

def default_constructor(clazz):
    return Templates.method(
        name='initialize',
        parameters='',
        body=field_init(),
    )

def constructor(doc, name, parameters, body):
    return Templates.method(
        name='initialize',
        parameters=', '.join(parameters),
        body=body,
    )

def method(doc, clazz, type, name, parameters, body):
    return Templates.method(
        name=name,
        parameters=', '.join(parameters),
        body=body,
    )

def static_method(doc, clazz, type, name, parameters, body):
    return Templates.method(
        name='self.' + name,
        parameters=', '.join(parameters),
        body=body,
    )

def abstract_method(doc, clazz, type, name, parameters):
    return Templates.method(
        name=name,
        parameters=', '.join(parameters),
        body='raise NotImplementedError, "this is an abstract method"',
    )

## Interface definition

def interface(doc, iface, parameters, bases, static_fields, methods):
    return clazz(doc, False, iface, parameters, None, [], static_fields, [], [default_constructor(iface)], methods)

def interface_method(doc, iface, type, name, parameters, body):
    return Templates.method(
        name=name,
        parameters=', '.join(parameters),
        body=body or 'raise NotImplementedError, "this is an abstract method"',
    )

## Function definition

def function(doc, type, name, parameters, body):
    return Templates.method(
        name='self.' + name,
        parameters=', '.join(parameters),
        body=body,
    )

## Parameters for methods and functions

def param(type, name, value):
    if value is None:
        return name
    else:
        return '{}={}'.format(name, value)

## Blocks

def block(statements):
    return indent('\n'.join(statements) or null())

## Statements

def local(type, name, value):
    return '{} = {}'.format(name, value or null())

def expr_stmt(e):
    assert e
    return e

def assign(lhs, rhs):
    return '{} = {}'.format(lhs, rhs)

def if_(pred, cons, alt):
    assert pred, pred
    if alt:
        return 'if ({}){}else{}end'.format(pred, cons, alt)
    else:
        return 'if ({}){}end'.format(pred, cons)

def while_(cond, body):
    return 'while ({}) do{}end'.format(cond, body)

def break_():
    return 'break'

def continue_():
    return 'next'

def return_(expr):
    return ('return ' + (expr or '')).strip()

## Expressions

def class_ref(v):
    return v

def method_ref(name):
    return 'self.' + name

def field_ref(name):
    return "@" + name

def local_ref(v):
    # assert v
    return v

def invoke_function(path, name, args):
    return Templates.method_call(receiver='::Quark',
                                 method='.'.join([p.replace('-', '_') for p in path] + [name]),
                                 args=', '.join(args))

def construct(class_, args):
    if class_ in ('Hash', 'DatawireQuarkCore::List'):
        # XXX HACK need to distinguish ::Quark and non-::Quark things
        receiver = class_
    else:
        receiver = '::Quark.' + class_.replace('-', '_')
    return Templates.method_call(receiver=receiver,
                                 method='new',
                                 args=', '.join(args))

def invoke_super(clazz, base, args):
    return 'super({args})'.format(args=', '.join(args))

def invoke_method(expr, method, args):
    return Templates.method_call(receiver=expr,
                                 method=method,
                                 args=', '.join(args))

def invoke_method_implicit(method, args):
    return Templates.method_call(receiver='self',
                                 method=method,
                                 args=', '.join(args))

def invoke_super_method(clazz, base, method, args):
    template = "method(:{method}).super_method.call({args})".format
    return template(method=method, args=', '.join(args))

def invoke_static_method(path, clazz, method, args):
    return Templates.method_call(receiver='.'.join(["::Quark"] + path + [clazz]),
                                 method=method,
                                 args=', '.join(args))

def get_field(expr, field):
    return "({receiver}).{name}".format(receiver=expr, name=field)

def get_static_field(path, clazz, field):
    return '.'.join(['::Quark'] + path + [clazz]) + '.' + field

def cast(type, expr):
    assert expr
    return expr

## Literals

def null():
    return 'nil'

def bool_(b):
    assert b.text in ('true', 'false')
    return b.text

def number(n):
    assert n.text
    return n.text

def string(s):
    result = s.text[0]
    idx = 1
    while idx < len(s.text) - 1:
        c = s.text[idx]
        next = s.text[idx + 1]
        if c == "\\" and next == "x":
            result += "\\u00"
            idx += 1
        else:
            result += c
        idx += 1
    result += s.text[-1]
    assert result
    return result

def list(elements):
    return 'DatawireQuarkCore::List.new([%s])' % ', '.join(elements)

def map(entries):
    pair = '{} => {}'.format
    return '{%s}' % (', '.join(pair(key, value) for key, value in entries))
