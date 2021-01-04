import re

import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType

from SDK import (database, jsonExtension, user, imports)

config = jsonExtension.load("config.json")
imports.ImportTools()


class Main(object):
    def __init__(self):
        self.config = config
        self.database = database.Database(config["db_file"], config["db_backups_folder"], self)
        generated_struct = database.Player(self.database, money=600, hi='notx')
        generated_struct.money = 1000000
        self.vk_session = vk_api.VkApi(token=self.config["vk_api_key"])
        self.longpoll = VkLongPoll(self.vk_session)
        self.vk = self.vk_session.get_api()
        self.group_id = "-" + re.findall(r'\d+', self.longpoll.server)[0]
        self.poll()

    def poll(self):
        for event in self.longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.user = user.User(self.vk, event.user_id)


Main()