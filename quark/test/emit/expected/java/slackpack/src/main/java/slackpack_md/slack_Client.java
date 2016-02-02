package slackpack_md;

public class slack_Client extends builtin.reflect.Class implements io.datawire.quark.runtime.QObject {
    public static builtin.reflect.Class singleton = new slack_Client();
    public slack_Client() {
        super("slack.Client");
        (this).name = "slack.Client";
        (this).parameters = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{}));
        (this).fields = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new builtin.reflect.Field("builtin.Runtime", "runtime"), new builtin.reflect.Field("builtin.String", "token"), new builtin.reflect.Field("slack.SlackHandler", "handler"), new builtin.reflect.Field("builtin.int", "event_id"), new builtin.reflect.Field("builtin.WebSocket", "socket")}));
        (this).methods = new java.util.ArrayList(java.util.Arrays.asList(new Object[]{new slack_Client_connect_Method(), new slack_Client_request_Method(), new slack_Client_ws_connect_Method(), new slack_Client_ws_send_Method(), new slack_Client_onWSConnected_Method(), new slack_Client_onWSClose_Method(), new slack_Client_onWSError_Method(), new slack_Client_construct_Method(), new slack_Client_onWSMessage_Method(), new slack_Client_onHTTPResponse_Method()}));
    }
    public Object construct(java.util.ArrayList<Object> args) {
        return new slack.Client((io.datawire.quark.runtime.Runtime) ((args).get(0)), (String) ((args).get(1)), (slack.SlackHandler) ((args).get(2)));
    }
    public String _getClass() {
        return (String) (null);
    }
    public Object _getField(String name) {
        return null;
    }
    public void _setField(String name, Object value) {}
}
