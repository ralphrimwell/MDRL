import asyncio
import aiohttp
import os
from .badges import Badges
from .guild import Guild
from .channel import Channel, PrivateChannel
from .utils import snowflake_time
from .user import ForeignUser, ClientUser, UserRelationships, RelationshipType, GuildUser
from .http import HTTPClient

    
class DiscordClient:
    def __repr__(self):
        if self.user:
            return self.user.__repr__()

    async def login(self, token: str, proxy=None):
        self.locale = 'en-GB' 
        self.token = token
        self._session = HTTPClient(token, proxy)

        self.user = await self._check_token()
        # for some reason discord doesnt return forbidden on login
        self.user.billing.payment_methods = await self.user.billing.get_payment_methods()

    async def __aenter__(self):
        return self

    async def __aexit__(self, *excinfo):
        await self._session._session.close()
        pass

    async def _check_token(self) -> ClientUser:
        resp = await self._session.request("GET", "v9/users/@me")
        return ClientUser(resp, self._session)

    async def get_guilds(self) -> list[Guild]:
        raw_guilds = await self._session.request("GET", "users/@me/guilds")
        guilds = []
        for guild in raw_guilds:
            # me = await self._session.request("GET", f"/users/@me/guilds/{guild['id']}/member")
            # if not me:
            #     print('bp')
            guilds.append(Guild(self._session, guild))

        return guilds
    
    async def get_private_channels(self) -> list[PrivateChannel]:
        raw_channels = await self._session.request("GET", "users/@me/channels")
        channels = []
        for channel in raw_channels:
            channels.append(PrivateChannel(self._session, channel))

        return channels
    
    async def get_relationships(self) -> UserRelationships:
        raw_relationships = await self._session.request("GET", "users/@me/relationships")
        relationships = UserRelationships()
        for relationship in raw_relationships:
            relationship_type = getattr(relationships, RelationshipType(relationship.get('type')).name)
            relationship_type.append(ForeignUser(relationship.get('user'), self._session))

        return relationships
    
    async def create_private_channel(self, recipients: list[str]):
        payload = {"recipients": recipients}
        return PrivateChannel(self._session, await self._session.request("POST", "users/@me/channels", payload=payload))

    async def delete_private_channel(self, id: str):
        return await self._session.request("DELETE", f"users/@me/channels/{id}")
