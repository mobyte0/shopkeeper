import re


__all__ = ["LeaderListener", "CommandListener", "StdCommandListener"]


class LeaderListener:
    def __init__(self, leader):
        self.leader = leader

    def onRecieve(self, bot, message):
        if message.m_type == "privmsg":
            matches = re.match(self.leader, message.body)
            if matches:
                message.body = matches.group(1)
                self.onLeader(bot, message)

            # If addressing via PM
            elif message.channel == bot.nick:
                self.onLeader(bot, message)

    def onLeader(self, message):
        pass


class CommandListener(LeaderListener):
    def __init__(self, leader, command):
        super().__init__(leader)
        self.command = command

    def onLeader(self, bot, message):
        message.body = message.body.strip()

        if message.body.startswith(self.command):
            args = tuple(filter(lambda x: x,
                                message.body[len(self.command):].strip().split(" ")))
            self.onCommand(bot, message, args)

    def onCommand(self, args):
        pass


class StdCommandListener(CommandListener):
    leader = "^[ ]*data(?:(?:: ?)| )(.+)"
    def __init__(self, command):
        super().__init__(StdCommandListener.leader, command)
