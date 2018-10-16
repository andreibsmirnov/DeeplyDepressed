import aiohttp
import asyncio
from vk import VK


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    client = aiohttp.ClientSession(loop=loop)
    vk = VK(client)
    loop.run_until_complete(vk.track_user(36))
    client.close()
