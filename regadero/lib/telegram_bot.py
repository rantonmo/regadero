import json
import requests

from logger import Logger


class TelegramBot():

    base_url = None
    logger = None

    main_chat = None  # chat to send updates

    username = None
    first_name = None
    id = None

    def __init__(self, token):

        self.base_url = f"https://api.telegram.org/bot{token}"
        self.logger = Logger(name='bot')
        (self.username, self.first_name, self.id) = self.get_me()


    def _do_get(self, path):
        # OSError: -202 --> no wlan connected
        self.logger.info(f"doing get to {path}")
        resp = requests.get(f"{self.base_url}/{path}")
        if resp.status_code != 200:
            self.logger.error(f"Error doing get: {resp.content}")
            return
        return resp.json().get('result')

    def _do_post(self, path, data=None):
        self.logger.info(f"doing post to {path} - {data}")
        resp = requests.post(f"{self.base_url}/{path}", json=data)
        if resp.status_code != 200:
            self.logger.error(f"Error doing post: {resp.content}")
            return False
        return resp.json().get('result')

    def get_me(self):
        data = self._do_get('getMe')
        self.logger.info(f"bot {data['first_name']} started successfull")
        return data['username'], data['first_name'], data['id']


    def get_updates(self):
        # we should grab the last data here
        return self._do_get('getUpdates')

    def ok_to_last_message(self):

        updates = self.get_updates()

        if len(updates) == 0:
            return

        last_mesage = updates.pop().get('message')
        data = {
            "chat_id": last_mesage['chat']['id'],
            "message_id": last_mesage['message_id'],
            "reaction": [{"type": 'emoji', "emoji": "👍"}],
            "is_big": True
        }

        return self._do_post('setMessageReaction', data)

