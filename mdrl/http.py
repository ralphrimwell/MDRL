import aiohttp
import os 
from dataclasses import dataclass

class Unauthorized(Exception):
    pass  

class Forbidden(Exception):
    pass  

@dataclass
class ResponseValue:
    status_code: int = None
    json: dict = None

class HTTPClient:
    def __init__(self, token, proxy=None):
        self.token = token
        self._session = aiohttp.ClientSession(headers=self._generate_headers())
        self.proxy = proxy
        self._baseurl = 'https://discordapp.com/api/'

    
    def _generate_headers(self):
        headers = {
            "Authorization": self.token,
            "accept": "*/*",
            "accept-language": "en-US",
            "connection": "keep-alive",
            "cookie": "__cfduid=%s; __dcfduid=%s; locale=en-US" % (os.urandom(43).hex(), os.urandom(32).hex()),
            "DNT": "1",
            "origin": "https://discord.com",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "referer": "https://discord.com/channels/@me",
            "TE": "Trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.9001 Chrome/83.0.4103.122 Electron/9.3.5 Safari/537.36",
            "X-Super-Properties": "eyJvcyI6IldpbmRvd3MiLCJicm93c2VyIjoiRGlzY29yZCBDbGllbnQiLCJyZWxlYXNlX2NoYW5uZWwiOiJzdGFibGUiLCJjbGllbnRfdmVyc2lvbiI6IjEuMC45MDAxIiwib3NfdmVyc2lvbiI6IjEwLjAuMTkwNDIiLCJvc19hcmNoIjoieDY0Iiwic3lzdGVtX2xvY2FsZSI6ImVuLVVTIiwiY2xpZW50X2J1aWxkX251bWJlciI6ODMwNDAsImNsaWVudF9ldmVudF9zb3VyY2UiOm51bGx9"
        }
        return headers

    async def request(self, method:str, path:str, payload:any=None) -> ResponseValue:
        kwargs={}
        if self.proxy:
            kwargs['proxy'] = 'http://' + self.proxy
        if payload:
            kwargs['json'] = payload
        async with self._session.request(method, self._baseurl + path, **kwargs) as resp:

            if resp.status == 200:
                return await resp.json()
            elif resp.status == 403:
                raise Forbidden()
            elif resp.status == 401: 
                raise Unauthorized("Token invalid")
            elif resp.status == 429:
                pass

