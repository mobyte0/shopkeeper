#!/usr/bin/env python3

import os
import sys
import logging
import datetime
import signal

from connection import Connection, Message
from listeners import *
from services import reload

logging.basicConfig(filename='data.log',level=logging.DEBUG)

log = logging.getLogger(__name__)
#log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.DEBUG)

bot=Connection("shopkeeper", "localhost")
bot.register()

StdCommandListener.leader = "^[ ]*"+bot.nick+"(?:(?:: ?)| )(.+)"

reload.ReloadListener.reloadCommands(bot)


def SignalHandler(signal, frame):
    # Let all the services know they're going down
    for service_name in bot.getServices():
        try:
            bot.getService(service_name).onDestroy(bot)
        except AttributeError:
            # Don't worry about it since this is optional
            pass
    sys.exit()


# Register signal handler for ctrl-c to allow bot services to know about their
# impending doom.
signal.signal(signal.SIGINT, SignalHandler)


# Implement the "bot" mainloop
while True:
    try:
        data = bot.recv()
        print(data)
    except UnicodeDecodeError:
        print("Some unicode!!")

    # Stay alive
    if data.startswith("PING"):
        bot.send("PONG " + data.split()[1])

    else:
        # TODO: Might be better to put the listeners in their own group apart
        # from the "bot".
        for m in Message.parse(data):
            bot.processListeners(m)
