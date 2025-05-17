import json
import requests

from logger import Logger

EMOJIS = {
    'ok': "👍",
    'nooo': "😱",
    'cry': "😭"
}

class TelegramBot():

    base_url = None
    chat_id = None  # chat to send messages
    headers = None

    logger = None

    username = None
    first_name = None
    id = None

    timeout = 15

    last_update_date = None

    def __init__(self, token, chat_id=None):

        self.base_url = f"https://api.telegram.org/bot{token}"
        self.chat_id = chat_id
        self.headers = {'Content-Type': 'application/json'}

        self.logger = Logger(name='bot')

        (self.username, self.first_name, self.id) = self.get_me()

        self.logger.info(f"bot initialized with name: {self.first_name} "
                         f"- username: {self.username}")


    def _do_get(self, path):
        # OSError: -202 --> no wlan connected
        self.logger.info(f"doing get to {path}")
        resp = requests.get(f"{self.base_url}/{path}", timeout=self.timeout)
        if resp.status_code != 200:
            self.logger.error(f"Error doing get: {resp.content}")
            return
        return resp.json().get('result')

    def _do_post(self, path, data=None):

        self.logger.info(f"doing post to {path} - {data}")
        resp = requests.post(f"{self.base_url}/{path}",
                             json=data,
                             headers=self.headers, timeout=self.timeout)
        if resp.status_code != 200:
            self.logger.error(f"Error doing post: {resp.content}")
            return False
        return resp.json().get('result')

    def get_me(self):
        data = self._do_get('getMe')
        return '@' + data['username'], data['first_name'], data['id']

    def get_updates(self):
        # we should grab the last date here
        updates = self._do_get('getUpdates')
        if len(updates) > 0:
            self.last_update_date = updates[-1]['message']['date']
            self.logger.info(f"last date is now {self.last_update_date}")
        return self._do_get('getUpdates')

    def get_refered_updates(self):
        "get messates containin the bot username in its text"
        return [msg for msg in self.get_updates() if self.username in msg.get('text', '')]

    def get_last_update(self):

        self.logger.info(f"getting last update from chat {self.chat_id}")

        updates = self.get_updates()

        while len(updates > 0):
            update = updates.pop()
            if not 'message' in update:
                self.logger.error("no message in last update!!")
                return None

            self.logger.info(f"last update from {update['message']['from']['first_name']} "
                             f"on chat {update['message']['chat']['title']}")

        return update


    def ok_to_last_message(self):

        updates = self.get_refered_updates()

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

    def send_message(self, message, notify=False):
        if not self.chat_id:
            self.logger.error("No default chat configured. Aborting...")
            return
        data = {
            "chat_id": self.chat_id,
            "text": message,
            "disable_notification": not notify
        }
        return self._do_post('sendMessage', data)
