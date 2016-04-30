import os
import pickle

class Persistence:
    def __init__(self):
        self.config_dir = "configs"
        if not os.path.exists(self.config_dir):
            os.mkdir(self.config_dir)

    def save(self, key, value):
        try:
            pickle.dump(value, open(self.config_dir+os.sep+key, "wb"))
        except IOError:
            print("Could not save:\n\t{}\n\t{}".format(key, value))

    def load(self, key):
        try:
            return pickle.load(open(self.config_dir+os.sep+key, "rb"))
        except IOError:
            print("Could not load:\n\t{}".format(key))
            return None

    # Required because this is a service
    def onRecieve(self, bot, message): pass
