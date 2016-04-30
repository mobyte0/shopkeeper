from listeners import StdCommandListener

class OpListener(StdCommandListener):
    def __init__(self):
        super().__init__("op")

    def onCommand(self, bot, message, args):
        # Make sure this user is allowed to be opped
        special = lambda u: bot.getService("admin").validateAdmin(u)
        args = tuple(filter(special, args))

        # Send the command to op as many users as we can
        print("Opping: "+" ".join(args)+" "+message.channel)
        bot.send("MODE {} +o {}".format(message.channel, " ".join(args)))
