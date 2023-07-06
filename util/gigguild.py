#!/usr/bin/env python
import gigdb

guilds = {}

class Guild:
    def __init__(self, id, mod_log_channel_id=None):
        self.id = id
        self.mod_log_channel_id = mod_log_channel_id
        self.save()

    def save(self):
        gigdb.save_guild(self.id, self.mod_log_channel_id)

    def set_mod_log_channel_id(self, mod_log_channel_id):
        self.mod_log_channel_id = mod_log_channel_id
        self.save()

def load_guilds():
    pass
#    for row in gigdb.get_all("guilds"):
#        guilds[row[0]] = Guild(row[0], row[1])
