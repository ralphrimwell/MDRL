from enum import Enum
from .channel import Channel

class GuildUser:
    def __init__(self, raw_data:dict):
        self.roles = raw_data.get('roles')
        self.id = raw_data['user'].get('id')
        
class Guild:
    def __init__(self, session, raw_data:dict, user:GuildUser):
        self._session = session
        self.me = user
        self.id = raw_data.get('id')
        self.name = raw_data.get('name')
        self.permissions = raw_data.get('permissions')

    async def get_channels(self):
        raw_channels = await self._session.request("GET", f"guilds/{self.id}/channels")
        channels = []

        for channel in raw_channels:
            channels.append(Channel(self._session, channel, self))

        return channels