from .badges import Badges
from .utils import snowflake_time
from .billing import Billing
from .http import HTTPClient
from enum import Enum

class BaseUser:
    __slots__ = ('id', 'name', 'discrim', 'avatar', 'created_at', 'badges')

    def __init__(self, raw_data:dict):
        self.id =          raw_data.get('id')
        self.name =        raw_data.get('username')
        self.discrim =     raw_data.get('discriminator')
        self.avatar =      raw_data.get('avatar')
        self.created_at =  snowflake_time(int(self.id))
        self.badges =      Badges.calculate(raw_data.get('public_flags'))

class ForeignUser(BaseUser):
    __slots__ = ('_session')

    def __init__(self, raw_data:dict, session:HTTPClient):
        super().__init__(raw_data)
        self._session = session
    
    def __repr__(self):
        return f'<ForeignUser id={self.id} name={self.name + self.discrim}>'

    # async def message(self):
    #     return await self._session.request("POST", f"channels/{self.id}/channels")


class ClientUser(BaseUser):
    __slots__ = ('billing', 'mfa_enabled', 'email', 'verified', 'phone', 'locale')

    def __init__(self, raw_data:dict, session:HTTPClient):
        super().__init__(raw_data)

        self.billing = Billing(session)
        self.mfa_enabled = raw_data.get('mfa_enabled')
        self.email =       raw_data.get('email')
        self.verified =    raw_data.get('verified')
        self.phone =       raw_data.get('phone')
        self.locale =      raw_data.get('locale')

    def __repr__(self):
        return f'<ClientUser id={self.id} name={self.name + self.discrim} verified={self.verified}>'

class RelationshipType(Enum):
    friends = 1
    blocked = 2
    incoming_friend_requests = 3
    outgoing_friend_requests = 4


class UserRelationships:
    __slots__ = ('friends', 'blocked', 'incoming_friend_requests', 'outgoing_friend_requests')

    def __init__(self):
        self.friends: list[ForeignUser] = []
        self.blocked: list[ForeignUser] = []
        self.incoming_friend_requests: list[ForeignUser] = []
        self.outgoing_friend_requests: list[ForeignUser] = []