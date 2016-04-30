from listeners import StdCommandListener

OVERLORD = "mobyte"

class AdminListener(StdCommandListener):
    def __init__(self):
        super().__init__("admin")
        self.admins = [OVERLORD]

    def validateAdmin(self, user):
        return user.lower() in self.admins

    def onCommand(self, bot, message, args):
        if self.validateAdmin(message.nick) and len(args) > 0:
            try:
                if args[0] != OVERLORD:
                    self.admins.remove(args[0])
            except ValueError:
                self.admins.extend(map(str.lower, args))
                print("Admins: "+", ".join(self.admins))

    def onLoad(self, bot):
        self.admins = bot.getService("persistence").load("admins") or [OVERLORD]

    def onDestroy(self, bot):
        bot.getService("persistence").save("admins", self.admins)
