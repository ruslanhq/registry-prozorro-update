import httpx
import requests


class MakeRequest:

    def __init__(self, uri, method='GET', data=None, params=None, auth=None, ):
        self.uri = uri
        self.data = data
        self.params = params
        self.method = method
        self.auth = auth

    async def do_request(self):
        async with httpx.AsyncClient(
                http2=False, verify=False, max_redirects=3
        ) as client:  # type: httpx.AsyncClient
            response = await client.request(
                self.method, self.uri, json=self.data, params=self.params,
                auth=self.auth
            )
            response.raise_for_status()

            return response.json()

    def do_sync_request(self):
        with requests.Session() as session:
            response = session.request(
                self.method, self.uri, json=self.data, params=self.params,
                auth=self.auth
            )
            # response.raise_for_status()

            return response.json()
