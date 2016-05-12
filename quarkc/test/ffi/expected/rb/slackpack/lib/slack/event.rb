module Quark
require "quark"
def self.slack; Slack; end
module Slack
def self.event; Event; end
module Event
require 'quark' # .../reflect slack/event
require_relative '../slack' # 0 () ('slack',)
require_relative '../slackpack_md' # 0 () ('slack',)


def self.SlackEvent; SlackEvent; end
class SlackEvent < ::DatawireQuarkCore::QuarkObject
    attr_accessor :type, :user, :channel, :timestamp
    extend ::DatawireQuarkCore::Static

    static slack_event_SlackEvent_ref: -> { nil }



    def initialize()
        self.__init_fields__

        nil
    end




    def load(client, obj)
        
        nil

        nil
    end

    def dispatch(handler)
        
        nil

        nil
    end

    def _getClass()
        
        return "slack.event.SlackEvent"

        nil
    end

    def _getField(name)
        
        if ((name) == ("type"))
            return (self).type
        end
        if ((name) == ("user"))
            return (self).user
        end
        if ((name) == ("channel"))
            return (self).channel
        end
        if ((name) == ("timestamp"))
            return (self).timestamp
        end
        return nil

        nil
    end

    def _setField(name, value)
        
        if ((name) == ("type"))
            (self).type = value
        end
        if ((name) == ("user"))
            (self).user = value
        end
        if ((name) == ("channel"))
            (self).channel = value
        end
        if ((name) == ("timestamp"))
            (self).timestamp = value
        end

        nil
    end

    def __init_fields__()
        
        self.type = nil
        self.user = nil
        self.channel = nil
        self.timestamp = nil

        nil
    end


end
SlackEvent.unlazy_statics

def self.SlackError; SlackError; end
class SlackError < ::Quark.slack.event.SlackEvent
    attr_accessor :code, :text
    extend ::DatawireQuarkCore::Static

    static slack_event_SlackError_ref: -> { nil }



    def initialize()
        
        super()

        nil
    end




    def load(client, obj)
        
        nil

        nil
    end

    def dispatch(handler)
        
        nil

        nil
    end

    def _getClass()
        
        return "slack.event.SlackError"

        nil
    end

    def _getField(name)
        
        if ((name) == ("type"))
            return (self).type
        end
        if ((name) == ("user"))
            return (self).user
        end
        if ((name) == ("channel"))
            return (self).channel
        end
        if ((name) == ("timestamp"))
            return (self).timestamp
        end
        if ((name) == ("code"))
            return (self).code
        end
        if ((name) == ("text"))
            return (self).text
        end
        return nil

        nil
    end

    def _setField(name, value)
        
        if ((name) == ("type"))
            (self).type = value
        end
        if ((name) == ("user"))
            (self).user = value
        end
        if ((name) == ("channel"))
            (self).channel = value
        end
        if ((name) == ("timestamp"))
            (self).timestamp = value
        end
        if ((name) == ("code"))
            (self).code = value
        end
        if ((name) == ("text"))
            (self).text = value
        end

        nil
    end

    def __init_fields__()
        
        super
        self.code = nil
        self.text = nil

        nil
    end


end
SlackError.unlazy_statics

def self.Hello; Hello; end
class Hello < ::Quark.slack.event.SlackEvent
    extend ::DatawireQuarkCore::Static

    static slack_event_Hello_ref: -> { nil }



    def initialize()
        
        super()

        nil
    end




    def dispatch(handler)
        
        nil

        nil
    end

    def _getClass()
        
        return "slack.event.Hello"

        nil
    end

    def _getField(name)
        
        if ((name) == ("type"))
            return (self).type
        end
        if ((name) == ("user"))
            return (self).user
        end
        if ((name) == ("channel"))
            return (self).channel
        end
        if ((name) == ("timestamp"))
            return (self).timestamp
        end
        return nil

        nil
    end

    def _setField(name, value)
        
        if ((name) == ("type"))
            (self).type = value
        end
        if ((name) == ("user"))
            (self).user = value
        end
        if ((name) == ("channel"))
            (self).channel = value
        end
        if ((name) == ("timestamp"))
            (self).timestamp = value
        end

        nil
    end

    def __init_fields__()
        
        super

        nil
    end


end
Hello.unlazy_statics

def self.Message; Message; end
class Message < ::Quark.slack.event.SlackEvent
    attr_accessor :subtype, :hidden, :text, :edited
    extend ::DatawireQuarkCore::Static

    static slack_event_Message_ref: -> { nil }



    def initialize()
        
        super()

        nil
    end




    def load(client, obj)
        
        nil

        nil
    end

    def dispatch(handler)
        
        nil

        nil
    end

    def _getClass()
        
        return "slack.event.Message"

        nil
    end

    def _getField(name)
        
        if ((name) == ("type"))
            return (self).type
        end
        if ((name) == ("user"))
            return (self).user
        end
        if ((name) == ("channel"))
            return (self).channel
        end
        if ((name) == ("timestamp"))
            return (self).timestamp
        end
        if ((name) == ("subtype"))
            return (self).subtype
        end
        if ((name) == ("hidden"))
            return (self).hidden
        end
        if ((name) == ("text"))
            return (self).text
        end
        if ((name) == ("edited"))
            return (self).edited
        end
        return nil

        nil
    end

    def _setField(name, value)
        
        if ((name) == ("type"))
            (self).type = value
        end
        if ((name) == ("user"))
            (self).user = value
        end
        if ((name) == ("channel"))
            (self).channel = value
        end
        if ((name) == ("timestamp"))
            (self).timestamp = value
        end
        if ((name) == ("subtype"))
            (self).subtype = value
        end
        if ((name) == ("hidden"))
            (self).hidden = value
        end
        if ((name) == ("text"))
            (self).text = value
        end
        if ((name) == ("edited"))
            (self).edited = value
        end

        nil
    end

    def __init_fields__()
        
        super
        self.subtype = nil
        self.hidden = nil
        self.text = nil
        self.edited = nil

        nil
    end


end
Message.unlazy_statics

def self.Edited; Edited; end
class Edited < ::DatawireQuarkCore::QuarkObject
    attr_accessor :user, :timestamp
    extend ::DatawireQuarkCore::Static

    static slack_event_Edited_ref: -> { nil }



    def initialize()
        self.__init_fields__

        nil
    end




    def _getClass()
        
        return "slack.event.Edited"

        nil
    end

    def _getField(name)
        
        if ((name) == ("user"))
            return (self).user
        end
        if ((name) == ("timestamp"))
            return (self).timestamp
        end
        return nil

        nil
    end

    def _setField(name, value)
        
        if ((name) == ("user"))
            (self).user = value
        end
        if ((name) == ("timestamp"))
            (self).timestamp = value
        end

        nil
    end

    def __init_fields__()
        
        self.user = nil
        self.timestamp = nil

        nil
    end


end
Edited.unlazy_statics
end # module Event
end # module Slack
end # module Quark
