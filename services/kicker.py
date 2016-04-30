from listeners import StdCommandListener
from collections import defaultdict

class KickListener(StdCommandListener):
    def __init__(self):
        super().__init__("addkick")
        self.to_kick = defaultdict(list)

    def saveList(self):
        pass

    def onRecieve(self, bot, message):
        super().onRecieve(bot, message)
        if message.m_type == "join":
            # For some reason joins have a ':' before the channel
            message.channel = message.channel.lstrip(":")

            if message.nick in self.to_kick[message.channel]:
                self.kick(bot, message.channel, message.nick)

    def onCommand(self, bot, message, args):
        "Usage: addkick <nick> | Adds nick to list to kick on join. Same usage to add/remove from list."
        if bot.getService("admin").validateAdmin(message.nick) and len(args) > 0:
            try:
                # Try to remove the user from the kick list
                self.to_kick[message.channel].remove(args[0])
            except ValueError:
                self.to_kick[message.channel].extend(args)
                for nick in args:
                    self.kick(bot, message.channel, nick)

    def kick(self, bot, channel, nick, reason = "GET REKT!"):
        bot.send("KICK {} {} :{}".format(channel, nick, reason))
