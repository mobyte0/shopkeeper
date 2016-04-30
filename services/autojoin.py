class AutoJoinService:
    "Manages auto joining bot to channels on kick or restart."
    def __init__(self):
        self.joined_channels = set()

    def onRecieve(self, bot, message):
        if message.nick == bot.nick:
            if message.m_type == "join":
                self.joined_channels.add(message.channel.lstrip(":"))

            elif message.m_type == "part":
                self.joined_channels.remove(message.channel)

        if message.m_type in ("kick",) and\
           message.channel in self.joined_channels:
            bot.join(message.channel.lstrip(":"))

    def onLoad(self, bot):
        self.joined_channels =\
                bot.getService("persistence").load("joined_channels") or set()

        # Join all the channels bot was in
        for c in self.joined_channels:
            bot.join(c)

    def onDestroy(self, bot):
        bot.getService("persistence").save("joined_channels",
                                           self.joined_channels)
