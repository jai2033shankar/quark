var _qrt = require("quark_runtime.js");

// CLASS Foo
function Foo() {
    this.__init_fields__();
}
exports.Foo = Foo;

function Foo__init_fields__() {}
Foo.prototype.__init_fields__ = Foo__init_fields__;

function Foo_m1() { /* interface */ }
Foo.prototype.m1 = Foo_m1;

function Foo_m2(arg) { /* interface */ }
Foo.prototype.m2 = Foo_m2;

function Foo_m3(args) { /* interface */ }
Foo.prototype.m3 = Foo_m3;

// CLASS Bar
function Bar() {
    this.__init_fields__();
}
exports.Bar = Bar;

function Bar__init_fields__() {}
Bar.prototype.__init_fields__ = Bar__init_fields__;

function Bar_m1() { /* interface */ }
Bar.prototype.m1 = Bar_m1;

function Bar_m2(arg) { /* interface */ }
Bar.prototype.m2 = Bar_m2;

function Bar_m3(args) { /* interface */ }
Bar.prototype.m3 = Bar_m3;

// CLASS Baz
function Baz() {
    Baz.super_.call(this);
}
exports.Baz = Baz;
_qrt.util.inherits(Baz, Foo);

function Baz__init_fields__() {
    Foo.prototype.__init_fields__.call(this);
}
Baz.prototype.__init_fields__ = Baz__init_fields__;

function Baz_m2(arg) {}
Baz.prototype.m2 = Baz_m2;

function Baz_m1() {}
Baz.prototype.m1 = Baz_m1;

function Baz_m3(args) {}
Baz.prototype.m3 = Baz_m3;