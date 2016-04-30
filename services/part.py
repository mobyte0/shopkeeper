from listeners import StdCommandListener

class PartListener(StdCommandListener):
    def __init__(self):
        super().__init__("part")

    def onCommand(self, bot, message, args):
        if bot.getService("admin").validateAdmin(message.nick):
            if len(args) > 0:
                chan = args[0]
            else:
                chan = message.channel

            try:
                auto_join_service = bot.getService("autojoin")
                if auto_join_service:
                    auto_join_service.joined_channels.remove(chan)
            except:
                pass

            bot.part(chan)
