from listeners import StdCommandListener

class ServicesListener(StdCommandListener):
    def __init__(self):
        super().__init__("services")

    def onCommand(self, bot, message, args):
        services = bot.getServices()

        if len(args) > 0:
            if args[0] == "commands":
                commands = []
                for s in services:
                    try:
                        commands.append(bot.getService(s).command)
                    except:
                        pass

                bot.respond(message, ", ".join(commands))
        else:
            bot.respond(message, ", ".join(services))
