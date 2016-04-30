from listeners import StdCommandListener
from copy import copy

class InspectorService(StdCommandListener):
    def __init__(self):
        super().__init__("inspect");

    def onCommand(self, bot, message, args):
        "Usage: inspect <service name> | Displays internal state of services."
        if not bot.getService("admin").validateAdmin(message.nick):
            return

        try:
            if len(args) >= 1:
                service = bot.getService(args[0])

            if len(args) == 2:
                response = getattr(service, args[1])

            else:
                try:
                    response = copy(vars(service))
                    for key in response.keys():
                        print(key)
                        if key.startswith("_"):
                            del response[key]

                    ignore = ("leader", "command")
                    for key in ignore:
                        try:
                            del response[key]
                        except KeyError:
                            pass
                except Exception as e:
                    response = "The %s service does not support inspection."%args[0]
                    print(e)

            bot.respond(message, str(response))
        except Exception as e:
            print(e)
