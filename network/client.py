import os
import aiohttp
import json

class NetworkError(Exception):
    pass

class NetworkClient:

    def __init__(self):
        self.base_url = os.getenv("SERVER_URL")

    async def get_available_networks(self) -> list[str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + "/account/availableNetworks") as response:
                if response.status == 200:
                    return json.loads(await response.text())
                else:
                    raise NetworkError()

