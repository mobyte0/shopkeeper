from listeners import StdCommandListener

class JoinListener(StdCommandListener):
    def __init__(self):
        super().__init__("join")

    def onCommand(self, bot, message, args):
        "Usage: join <#channel> | N.B. Requires admin privs."
        if bot.getService("admin").validateAdmin(message.nick):
            bot.join(args[0])
