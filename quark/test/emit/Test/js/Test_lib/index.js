var _qrt = require("datawire-quark-core");




/* BEGIN_BUILTIN */


// CLASS Class

function Class(id) {
    this.__init_fields__();
    (this).id = id;
    _class(this);
}
exports.Class = Class;

function Class__init_fields__() {
    this.id = null;
    this.name = null;
    this.parameters = null;
}
Class.prototype.__init_fields__ = Class__init_fields__;

function Class_getId() {
    return this.id;
}
Class.prototype.getId = Class_getId;

function Class_getName() {
    return this.name;
}
Class.prototype.getName = Class_getName;

function Class_getParameters() {
    return this.parameters;
}
Class.prototype.getParameters = Class_getParameters;

function Class_construct(args) {
    return _construct(this.getId(), args);
}
Class.prototype.construct = Class_construct;

function Class_getFields() {
    return _fields((this).id);
}
Class.prototype.getFields = Class_getFields;

function Class_getField(name) {
    var fields = this.getFields();
    var idx = 0;
    while ((idx) < ((fields).length)) {
        if ((((fields)[idx]).name) === (name)) {
            return (fields)[idx];
        }
        idx = (idx) + (1);
    }
    return null;
}
Class.prototype.getField = Class_getField;

function Class_invoke(object, method, args) {
    return _invoke((this).id, object, method, args);
}
Class.prototype.invoke = Class_invoke;

function Class__getClass() {
    return "Class";
}
Class.prototype._getClass = Class__getClass;

function Class__getField(name) {
    if ((name) === ("id")) {
        return (this).id;
    }
    if ((name) === ("name")) {
        return (this).name;
    }
    if ((name) === ("parameters")) {
        return (this).parameters;
    }
    return null;
}
Class.prototype._getField = Class__getField;

function Class__setField(name, value) {
    if ((name) === ("id")) {
        (this).id = value;
    }
    if ((name) === ("name")) {
        (this).name = value;
    }
    if ((name) === ("parameters")) {
        (this).parameters = value;
    }
}
Class.prototype._setField = Class__setField;
/* END_BUILTIN */

/* BEGIN_BUILTIN */


// CLASS Field

function Field(type, name) {
    this.__init_fields__();
    (this).type = type;
    (this).name = name;
}
exports.Field = Field;

function Field__init_fields__() {
    this.type = null;
    this.name = null;
}
Field.prototype.__init_fields__ = Field__init_fields__;

function Field__getClass() {
    return "Field";
}
Field.prototype._getClass = Field__getClass;

function Field__getField(name) {
    if ((name) === ("type")) {
        return (this).type;
    }
    if ((name) === ("name")) {
        return (this).name;
    }
    return null;
}
Field.prototype._getField = Field__getField;

function Field__setField(name, value) {
    if ((name) === ("type")) {
        (this).type = value;
    }
    if ((name) === ("name")) {
        (this).name = value;
    }
}
Field.prototype._setField = Field__setField;
/* END_BUILTIN */

/* BEGIN_BUILTIN */


function toJSON(obj) {
    var result = new _qrt.JSONObject();
    if ((obj) === (null)) {
        (result).setNull();
        return result;
    }
    var cls = new Class(_qrt._getClass(obj));
    var idx = 0;
    if (((cls).name) === ("String")) {
        (result).setString(obj);
        return result;
    }
    if (((((((cls).name) === ("byte")) || (((cls).name) === ("short"))) || (((cls).name) === ("int"))) || (((cls).name) === ("long"))) || (((cls).name) === ("float"))) {
        (result).setNumber(obj);
        return result;
    }
    if (((cls).name) === ("List")) {
        (result).setList();
        var list = obj;
        while ((idx) < ((list).length)) {
            (result).setListItem(idx, toJSON((list)[idx]));
            idx = (idx) + (1);
        }
        return result;
    }
    if (((cls).name) === ("Map")) {
        (result).setObject();
        var map = obj;
        return result;
    }
    (result).setObjectItem(("$class"), ((new _qrt.JSONObject()).setString((cls).id)));
    var fields = (cls).getFields();
    while ((idx) < ((fields).length)) {
        (result).setObjectItem((((fields)[idx]).name), (toJSON((obj)._getField(((fields)[idx]).name))));
        idx = (idx) + (1);
    }
    return result;
}
exports.toJSON = toJSON;
/* END_BUILTIN */

/* BEGIN_BUILTIN */


function fromJSON(cls, json) {
    if (((json) === (null)) || ((json).isNull())) {
        return null;
    }
    var idx = 0;
    if (((cls).name) === ("List")) {
        var list = (cls).construct([]);
        while ((idx) < ((json).size())) {
            (list).push(fromJSON(((cls).parameters)[0], (json).getListItem(idx)));
            idx = (idx) + (1);
        }
        return list;
    }
    var fields = (cls).getFields();
    var result = (cls).construct([]);
    while ((idx) < ((fields).length)) {
        var f = (fields)[idx];
        idx = (idx) + (1);
        if ((((f).type).name) === ("String")) {
            var s = ((json).getObjectItem((f).name)).getString();
            (result)._setField(((f).name), (s));
            continue;
        }
        if ((((f).type).name) === ("float")) {
            var flt = ((json).getObjectItem((f).name)).getNumber();
            (result)._setField(((f).name), (flt));
            continue;
        }
        if ((((f).type).name) === ("int")) {
            if (!(((json).getObjectItem((f).name)).isNull())) {
                var i = Math.round(((json).getObjectItem((f).name)).getNumber());
                (result)._setField(((f).name), (i));
            }
            continue;
        }
        if ((((f).type).name) === ("bool")) {
            if (!(((json).getObjectItem((f).name)).isNull())) {
                var b = ((json).getObjectItem((f).name)).getBool();
                (result)._setField(((f).name), (b));
            }
            continue;
        }
        (result)._setField(((f).name), (fromJSON((f).type, (json).getObjectItem((f).name))));
    }
    return result;
}
exports.fromJSON = fromJSON;
/* END_BUILTIN */

/* BEGIN_BUILTIN */


// CLASS ResponseHolder
function ResponseHolder() {
    this.__init_fields__();
}
exports.ResponseHolder = ResponseHolder;

function ResponseHolder__init_fields__() {
    this.response = null;
}
ResponseHolder.prototype.__init_fields__ = ResponseHolder__init_fields__;

function ResponseHolder_onHTTPResponse(request, response) {
    (this).response = response;
}
ResponseHolder.prototype.onHTTPResponse = ResponseHolder_onHTTPResponse;

function ResponseHolder__getClass() {
    return "ResponseHolder";
}
ResponseHolder.prototype._getClass = ResponseHolder__getClass;

function ResponseHolder__getField(name) {
    if ((name) === ("response")) {
        return (this).response;
    }
    return null;
}
ResponseHolder.prototype._getField = ResponseHolder__getField;

function ResponseHolder__setField(name, value) {
    if ((name) === ("response")) {
        (this).response = value;
    }
}
ResponseHolder.prototype._setField = ResponseHolder__setField;

function ResponseHolder_onHTTPInit(request) {}
ResponseHolder.prototype.onHTTPInit = ResponseHolder_onHTTPInit;

function ResponseHolder_onHTTPError(request) {}
ResponseHolder.prototype.onHTTPError = ResponseHolder_onHTTPError;

function ResponseHolder_onHTTPFinal(request) {}
ResponseHolder.prototype.onHTTPFinal = ResponseHolder_onHTTPFinal;
/* END_BUILTIN */

/* BEGIN_BUILTIN */


// CLASS Service
function Service() {
    this.__init_fields__();
}
exports.Service = Service;

function Service__init_fields__() {}
Service.prototype.__init_fields__ = Service__init_fields__;

function Service_getURL() { /* interface */ }
Service.prototype.getURL = Service_getURL;

function Service_getRuntime() { /* interface */ }
Service.prototype.getRuntime = Service_getRuntime;

function Service_rpc(name, message) {
    var request = new _qrt.HTTPRequest(this.getURL());
    var json = toJSON(message);
    var envelope = new _qrt.JSONObject();
    (envelope).setObjectItem(("$method"), ((new _qrt.JSONObject()).setString(name)));
    (envelope).setObjectItem(("rpc"), (json));
    (request).setBody((envelope).toString());
    (request).setMethod("POST");
    var rt = (this).getRuntime();
    var rh = new ResponseHolder();
    (rt).acquire();
    (rt).request(request, rh);
    while (((rh).response) === (null)) {
        (rt).wait(3.14);
    }
    var response = (rh).response;
    (rt).release();
    var body = (response).getBody();
    var obj = _qrt.json_from_string(body);
    return fromJSON(new Class(((obj).getObjectItem("$class")).getString()), obj);
}
Service.prototype.rpc = Service_rpc;
/* END_BUILTIN */

/* BEGIN_BUILTIN */


// CLASS Client

function Client(runtime, url) {
    this.__init_fields__();
    (this).runtime = runtime;
    (this).url = url;
}
exports.Client = Client;

function Client__init_fields__() {
    this.runtime = null;
    this.url = null;
}
Client.prototype.__init_fields__ = Client__init_fields__;

function Client_getRuntime() {
    return (this).runtime;
}
Client.prototype.getRuntime = Client_getRuntime;

function Client_getURL() {
    return (this).url;
}
Client.prototype.getURL = Client_getURL;

function Client__getClass() {
    return "Client";
}
Client.prototype._getClass = Client__getClass;

function Client__getField(name) {
    if ((name) === ("runtime")) {
        return (this).runtime;
    }
    if ((name) === ("url")) {
        return (this).url;
    }
    return null;
}
Client.prototype._getField = Client__getField;

function Client__setField(name, value) {
    if ((name) === ("runtime")) {
        (this).runtime = value;
    }
    if ((name) === ("url")) {
        (this).url = value;
    }
}
Client.prototype._setField = Client__setField;
/* END_BUILTIN */

/* BEGIN_BUILTIN */


// CLASS Server

function Server(runtime, impl) {
    this.__init_fields__();
    (this).runtime = runtime;
    (this).impl = impl;
}
exports.Server = Server;

function Server__init_fields__() {
    this.runtime = null;
    this.impl = null;
}
Server.prototype.__init_fields__ = Server__init_fields__;

function Server_getRuntime() {
    return (this).runtime;
}
Server.prototype.getRuntime = Server_getRuntime;

function Server_onHTTPRequest(request, response) {
    var envelope = _qrt.json_from_string((request).getBody());
    var method = ((envelope).getObjectItem("$method")).getString();
    var json = (envelope).getObjectItem("rpc");
    var argument = fromJSON(new Class(((json).getObjectItem("$class")).getString()), json);
    var result = (((new Class(_qrt._getClass(this))).getField("impl")).type).invoke(this.impl, method, [argument]);
    (response).setBody((toJSON(result)).toString());
    (response).setCode(200);
    (this.getRuntime()).respond(request, response);
}
Server.prototype.onHTTPRequest = Server_onHTTPRequest;

function Server__getClass() {
    return "Server<Object>";
}
Server.prototype._getClass = Server__getClass;

function Server__getField(name) {
    if ((name) === ("runtime")) {
        return (this).runtime;
    }
    if ((name) === ("impl")) {
        return (this).impl;
    }
    return null;
}
Server.prototype._getField = Server__getField;

function Server__setField(name, value) {
    if ((name) === ("runtime")) {
        (this).runtime = value;
    }
    if ((name) === ("impl")) {
        (this).impl = value;
    }
}
Server.prototype._setField = Server__setField;

/**
 * called after the servlet is successfully installed. The url will be the actual url used, important especially if ephemeral port was requested
 */
function Server_onServletInit(url, runtime) {}
Server.prototype.onServletInit = Server_onServletInit;

/**
 * called if the servlet could not be installed
 */
function Server_onServletError(url, error) {}
Server.prototype.onServletError = Server_onServletError;

/**
 * called when the servlet is removed
 */
function Server_onServletEnd(url) {}
Server.prototype.onServletEnd = Server_onServletEnd;
/* END_BUILTIN */


// CLASS Test
function Test() {
    this.__init_fields__();
}
exports.Test = Test;

function Test__init_fields__() {}
Test.prototype.__init_fields__ = Test__init_fields__;

function Test_foo(t) {
    return new Test();
}
Test.prototype.foo = Test_foo;

function Test_test() {
    var x = 2;
    var y = 2;
    var z = (x) + (y);
    _qrt.print(z);
    var hello = "hello";
    _qrt.print(hello);
    var t1 = new Test();
    var t2 = (t1).foo(t1);
    if ((t2) !== (t1)) {
        _qrt.print("YAY!");
    }
    var four = (2) + (2);
    _qrt.print(four);
}
Test.prototype.test = Test_test;

function Test__getClass() {
    return "Test";
}
Test.prototype._getClass = Test__getClass;

function Test__getField(name) {
    return null;
}
Test.prototype._getField = Test__getField;

function Test__setField(name, value) {}
Test.prototype._setField = Test__setField;

function main() {
    (new Test()).test();
}
exports.main = main;

function _construct(className, args) {
    if ((className) === ("Class")) {
        return new Class((args)[0]);
    }
    if ((className) === ("Field")) {
        return new Field((args)[0], (args)[1]);
    }
    if ((className) === ("List<Object>")) {
        return new Array();
    }
    if ((className) === ("List<Field>")) {
        return new Array();
    }
    if ((className) === ("List<Class>")) {
        return new Array();
    }
    if ((className) === ("List<String>")) {
        return new Array();
    }
    if ((className) === ("Map<Object,Object>")) {
        return new Map();
    }
    if ((className) === ("Map<String,Object>")) {
        return new Map();
    }
    if ((className) === ("ResponseHolder")) {
        return new ResponseHolder();
    }
    if ((className) === ("Client")) {
        return new Client((args)[0], (args)[1]);
    }
    if ((className) === ("Server<Object>")) {
        return new Server((args)[0], (args)[1]);
    }
    if ((className) === ("Test")) {
        return new Test();
    }
    return null;
}
exports._construct = _construct;

function _fields(className) {
    if ((className) === ("Class")) {
        return [new Field(new Class("String"), "id"), new Field(new Class("String"), "name"), new Field(new Class("List<Class>"), "parameters")];
    }
    if ((className) === ("Field")) {
        return [new Field(new Class("Class"), "type"), new Field(new Class("String"), "name")];
    }
    if ((className) === ("List<Object>")) {
        return [];
    }
    if ((className) === ("List<Field>")) {
        return [];
    }
    if ((className) === ("List<Class>")) {
        return [];
    }
    if ((className) === ("List<String>")) {
        return [];
    }
    if ((className) === ("Map<Object,Object>")) {
        return [];
    }
    if ((className) === ("Map<String,Object>")) {
        return [];
    }
    if ((className) === ("ResponseHolder")) {
        return [new Field(new Class("HTTPResponse"), "response")];
    }
    if ((className) === ("Client")) {
        return [new Field(new Class("Runtime"), "runtime"), new Field(new Class("String"), "url")];
    }
    if ((className) === ("Server<Object>")) {
        return [new Field(new Class("Runtime"), "runtime"), new Field(new Class("Object"), "impl")];
    }
    if ((className) === ("Test")) {
        return [];
    }
    return null;
}
exports._fields = _fields;

function _class(cls) {
    if (((cls).id) === ("Class")) {
        (cls).name = "Class";
        (cls).parameters = [];
        return;
    }
    if (((cls).id) === ("Field")) {
        (cls).name = "Field";
        (cls).parameters = [];
        return;
    }
    if (((cls).id) === ("List<Object>")) {
        (cls).name = "List";
        (cls).parameters = [new Class("Object")];
        return;
    }
    if (((cls).id) === ("List<Field>")) {
        (cls).name = "List";
        (cls).parameters = [new Class("Field")];
        return;
    }
    if (((cls).id) === ("List<Class>")) {
        (cls).name = "List";
        (cls).parameters = [new Class("Class")];
        return;
    }
    if (((cls).id) === ("List<String>")) {
        (cls).name = "List";
        (cls).parameters = [new Class("String")];
        return;
    }
    if (((cls).id) === ("Map<Object,Object>")) {
        (cls).name = "Map";
        (cls).parameters = [new Class("Object"), new Class("Object")];
        return;
    }
    if (((cls).id) === ("Map<String,Object>")) {
        (cls).name = "Map";
        (cls).parameters = [new Class("String"), new Class("Object")];
        return;
    }
    if (((cls).id) === ("ResponseHolder")) {
        (cls).name = "ResponseHolder";
        (cls).parameters = [];
        return;
    }
    if (((cls).id) === ("Service")) {
        (cls).name = "Service";
        (cls).parameters = [];
        return;
    }
    if (((cls).id) === ("Client")) {
        (cls).name = "Client";
        (cls).parameters = [];
        return;
    }
    if (((cls).id) === ("Server<Object>")) {
        (cls).name = "Server";
        (cls).parameters = [new Class("Object")];
        return;
    }
    if (((cls).id) === ("Test")) {
        (cls).name = "Test";
        (cls).parameters = [];
        return;
    }
    (cls).name = (cls).id;
}
exports._class = _class;

function _invoke(className, object, method, args) {
    if ((className) === ("Class")) {
        if ((method) === ("getId")) {
            var tmp_0 = object;
            return (tmp_0).getId();
        }
        if ((method) === ("getName")) {
            var tmp_1 = object;
            return (tmp_1).getName();
        }
        if ((method) === ("getParameters")) {
            var tmp_2 = object;
            return (tmp_2).getParameters();
        }
        if ((method) === ("construct")) {
            var tmp_3 = object;
            return (tmp_3).construct((args)[0]);
        }
        if ((method) === ("getFields")) {
            var tmp_4 = object;
            return (tmp_4).getFields();
        }
        if ((method) === ("getField")) {
            var tmp_5 = object;
            return (tmp_5).getField((args)[0]);
        }
        if ((method) === ("invoke")) {
            var tmp_6 = object;
            return (tmp_6).invoke((args)[0], (args)[1], (args)[2]);
        }
    }
    if ((className) === ("Field")) {}
    if ((className) === ("List<Object>")) {}
    if ((className) === ("List<Field>")) {}
    if ((className) === ("List<Class>")) {}
    if ((className) === ("List<String>")) {}
    if ((className) === ("Map<Object,Object>")) {}
    if ((className) === ("Map<String,Object>")) {}
    if ((className) === ("ResponseHolder")) {
        if ((method) === ("onHTTPResponse")) {
            var tmp_7 = object;
            (tmp_7).onHTTPResponse((args)[0], (args)[1]);
            return null;
        }
    }
    if ((className) === ("Service")) {
        if ((method) === ("getURL")) {
            var tmp_8 = object;
            return (tmp_8).getURL();
        }
        if ((method) === ("getRuntime")) {
            var tmp_9 = object;
            return (tmp_9).getRuntime();
        }
        if ((method) === ("rpc")) {
            var tmp_10 = object;
            return (tmp_10).rpc((args)[0], (args)[1]);
        }
    }
    if ((className) === ("Client")) {
        if ((method) === ("getRuntime")) {
            var tmp_11 = object;
            return (tmp_11).getRuntime();
        }
        if ((method) === ("getURL")) {
            var tmp_12 = object;
            return (tmp_12).getURL();
        }
    }
    if ((className) === ("Server<Object>")) {
        if ((method) === ("getRuntime")) {
            var tmp_13 = object;
            return (tmp_13).getRuntime();
        }
        if ((method) === ("onHTTPRequest")) {
            var tmp_14 = object;
            (tmp_14).onHTTPRequest((args)[0], (args)[1]);
            return null;
        }
    }
    if ((className) === ("Test")) {
        if ((method) === ("foo")) {
            var tmp_15 = object;
            return (tmp_15).foo((args)[0]);
        }
        if ((method) === ("test")) {
            var tmp_16 = object;
            (tmp_16).test();
            return null;
        }
    }
    return null;
}
exports._invoke = _invoke;
