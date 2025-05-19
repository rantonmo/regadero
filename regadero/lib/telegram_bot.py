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

    last_update_id = None

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
            resp.close()
            return
        result = resp.json().get('result')
        resp.close()
        return result

    def _do_post(self, path, data=None):

        self.logger.info(f"doing post to {path} - {data}")
        resp = requests.post(f"{self.base_url}/{path}",
                             json=data,
                             headers=self.headers, timeout=self.timeout)
        if resp.status_code != 200:
            self.logger.error(f"Error doing post: {resp.content}")
            resp.close()
            return False
        result = resp.json().get('result')
        resp.close()
        return result

    def get_me(self):
        data = self._do_get('getMe')
        return '@' + data['username'], data['first_name'], data['id']

    def get_updates(self, offset=None):
        # we should grab the last date here
        data = {}
        if offset:
            data.update({"offset": offset})
        updates = self._do_post('getUpdates', data)

        if len(updates) > 0:
            self.last_update_id = updates[-1]['update_id']
            self.logger.info(f"last date is now {self.last_update_id}")
        return updates

    def get_refered_updates(self):
        "get messates containin the bot username in its text"
        return [msg for msg in self.get_updates() if self.username in msg.get('text', '')]

    def get_commands(self):
        updates = self.get_updates(
            self.last_update_id + 1 if self.last_update_id else None)

        return [
            x['message']['text'] for x in updates
              if 'text' in x['message'] and 'loli' in x['message']['text'].lower()
        ]

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
