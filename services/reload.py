import os
import traceback
from listeners import StdCommandListener

class ReloadListener(StdCommandListener):
    def __init__(self):
        super().__init__("reload")

    def onCommand(self, bot, message, args):
        # Let all the services know they're going down
        for service_name in bot.getServices():
            try:
                bot.getService(service_name).onDestroy(bot)
            except AttributeError:
                # Don't worry about it since this is optional
                pass

        # Clear the services
        bot.clearServices()

        ReloadListener.reloadCommands(bot)

        # Re-add this service if somehow it didn't get reloaded
        if not bot.getService("reload"):
            print("Apparently something bad happened. Re-registering self.")
            bot.registerService("reload", ReloadListener)


    @staticmethod
    def reloadCommands(bot, directory = "services"):
        for fname in os.listdir(directory):
            try:
                if fname.endswith(".py"):
                    service_name = fname.split(".")[0]
                    g = {}
                    print("Loading {}".format(fname))
                    with open(directory + os.sep + fname) as f:
                        exec(compile(f.read(), fname, "exec"), g)

                    for key, value in g.items():
                        try:
                            if hasattr(value, "__module__") and\
                               value.__module__ == "builtins":
                                print("\tRegistering " + key)
                                bot.registerService(service_name, value)


                        except AttributeError as e:
                            if key != "__builtins__":
                                print("\tCould not register " + key)
                                traceback.print_exc()
            except:
                # Print the traceback, but keep on goin'
                traceback.print_exc()

        # Allow services to do any initialization necessary
        for service_name in bot.getServices() :
            try:
                bot.getService(service_name).onLoad(bot)
            except AttributeError:
                # Don't worry about it since this is optional
                pass
