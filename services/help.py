from listeners import StdCommandListener

class HelpService(StdCommandListener):
    def __init__(self):
        super().__init__("help")

    def onCommand(self, bot, message, args):
        "Usage: help <service name>"
        if not args:
            bot.respond(message, self.onCommand.__doc__)
            return

        service = bot.getService(args[0])

        if not service:
            bot.respond(message, "Service \"%s\" does not exist."%args[0])
            return

        try:
            bot.respond(message, service.onCommand.__doc__)
        except AttributeError:
            if service.__doc__:
                bot.respond(message, "(Service) " + service.__doc__)
            else:
                bot.respond(message,
                            "Service \"%s\" has no documentation."%args[0])
        except Exception as e:
            print(e)
