import os
import aiohttp
import json
import network.endpoint as endpoint
from typing import Optional, Union

class NetworkError(Exception):
    pass

class NetworkClient:

    def __init__(self):
        self.base_url = os.getenv("SERVER_URL")

    async def get_available_networks(self) -> list[str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + endpoint.available_networks) as response:
                if response.status == 200:
                    return json.loads(await response.text())
                else:
                    raise NetworkError()

    async def get_address_tracking_networks(self) -> list[str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + endpoint.address_tracking_networks) as response:
                if response.status == 200:
                    return json.loads(await response.text())
                else:
                    raise NetworkError()

    async def create_account(
            self,
            network_name: str,
            address: Optional[str],
            initial_balance: Optional[int]
    ) -> Optional[str]:
        async with aiohttp.ClientSession() as session:
            request_body = {
                'network_name': network_name,
                'balance': initial_balance,
                'address': address
            }
            request = session.post(
                url=self.base_url + endpoint.account_add,
                json=request_body
            )
            async with request as re:
                response: dict = json.loads(await re.text())
                return response['error'] if response.__contains__('error') else None

    async def get_all_accounts(self) -> Union[str, list]:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url + endpoint.account_all) as response:
                resp: Union[list[dict], dict] = json.loads(await response.text())
                return resp if not resp.__contains__('error') else resp['error']




