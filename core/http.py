from typing import Type

from httpx import AsyncClient


class ApiClient:
    def __init__(self, host: str, port: int, token: str, client: Type[AsyncClient] = AsyncClient):
        self._host = host
        self._port = port
        self._client = client
        self.headers = {
            'Authorization': f'Basic {token}',
        }

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    def get_uri(self, endpoint: str) -> str:
        host = self.host.rstrip('/')
        endpoint = endpoint.lstrip('/')
        return f'{host}:{self.port}/api/v1/{endpoint}'

    async def post(self, endpoint: str, data=None):
        uri = self.get_uri(endpoint)
        print(uri)
        async with self._client() as client:
            return await client.post(uri, data=data, headers=self.headers)
