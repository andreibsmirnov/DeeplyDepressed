import json
import logging
import os
from time import sleep
from datetime import datetime

logger = logging.getLogger(__name__)
VK_URL = 'https://api.vk.com'
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")


class UserLastSeen:
    def __init__(self, vk_response):
        self.id = None
        self.first_name = None
        self.last_name = None
        self.last_seen_time = None
        try:
            response = json.loads(vk_response)['response'][0]
            self.id = response['id']
            self.first_name = response['first_name']
            self.last_name = response['first_name']
            self.last_seen_time = datetime.fromtimestamp(
                response['last_seen']['time'])
            self.current_time = datetime.now()
        except (KeyError, IndexError):
            logger.error('Incorrect response format %s' % vk_response)

    def __repr__(self):
        return f"id: {self.id}, " \
               f"name: {self.first_name} {self.last_name}, " \
               f"last seen: {self.last_seen_time}, " \
               f"taken at: {self.current_time}"


class VK:
    def __init__(self, client):
        self.url = VK_URL
        self.client = client

    async def get_users_last_seen_time(self, user_id):
        url = f'{VK_URL}/method/users.get?user_id={user_id}' \
              f'&fields=last_seen&access_token={ACCESS_TOKEN}&v=5.52'
        logger.info(f'Going to send request {url}')
        async with self.client.get(url) as response:
            response = await response.read()
            user_last_seen = UserLastSeen(response)
            print(user_last_seen)
            return user_last_seen

    async def track_user(self, user_id):
        while True:
            await self.get_users_last_seen_time(user_id)
            sleep(5)
