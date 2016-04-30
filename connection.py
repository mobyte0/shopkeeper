import socket
import logging
import copy
import re

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class Connection:
    def __init__(self, nick, host, port=6667):
        self.nick=nick
        self.host=host
        self.port=port

        self.socket = socket.socket()
        log.info("Connecting to {}:{} as {}".format(host, port, nick))
        self.socket.connect((host, port))
        log.info("Connected")

        self.setNick(self.nick)
        self.__services = {}

    def send(self,message):
        # TODO: break message up based on maximum message size
        log.info("[>] {}".format(message))
        self.socket.send("{}\r\n".format(message).encode("utf-8"))

    def recv(self):
        # TODO: buffer until one line
        message = self.socket.recv(2048).decode("utf-8").strip()
        log.info("[<] {}".format(message))
        return message

    def register(self):
        ident = self.nick
        real_name = self.nick
        self.send("USER {} {} bla :{}".format(ident, self.host, real_name))

    def setNick(self, nick):
        self.send("NICK " + nick)

    def join(self, channel):
        self.send("JOIN " + channel)

    def part(self, channel):
        self.send("PART " + channel)

    def say(self, channel, message):
        self.send("PRIVMSG {} :{}".format(channel, message))

    def respond(self, m, response_text):
        # m == message
        respond_channel = (m.channel == self.nick and m.nick) or m.channel
        self.say(respond_channel, response_text)

    def registerService(self, name, service, *args):
        self.__services[name] = service(*args)

    def clearServices(self):
        self.__services = {}

    def getServices(self):
        return self.__services.keys()

    def getService(self, name):
        try:
            return self.__services[name]
        except KeyError:
            return None

    def processListeners(self, message):
        for k,s in self.__services.items():
            try:
                s.onRecieve(self, copy.copy(message))
            except Exception as e:
                self.respond(message, k+": "+str(e))


class Message:
                           # nick!uname@host  mtype     chan    message
    msg_patt = re.compile(":(.+?)!(.+?)@(.+?) (.+?) ([^ \r\n]+)(?: :(.+))?")

    def __init__(self, nick, username, host, m_type, channel, body):
        self.nick = nick
        self.username = username
        self.host = host
        self.m_type = m_type.lower() #join, part, mode, privmsg
        self.channel = channel
        self.body = body

    def __str__(self):
        return "{}!{}@{} {} {} {}".format(self.nick,
                                          self.username,
                                          self.host,
                                          self.m_type,
                                          self.channel,
                                          self.body)

    @staticmethod
    def parse(data):
        return map(lambda x: Message(*x), Message.msg_patt.findall(data))
