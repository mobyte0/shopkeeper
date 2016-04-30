from listeners import StdCommandListener

class EchoListener(StdCommandListener):
    def __init__(self):
        super().__init__("echo")

    def onCommand(self, bot, message, args):
        bot.respond(message, message.nick + ": " + " ".join(args))
