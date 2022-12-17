from .badges import Badges
from .utils import snowflake_time
from .billing import Billing
from .http import HTTPClient

class BaseUser:
    def __init__(self, raw_data:dict):
        self.id =          raw_data.get('id')
        self.username =    raw_data.get('username')
        self.discrim =     raw_data.get('discriminator')
        self.avatar =      raw_data.get('avatar')
        self.created_at =  snowflake_time(int(self.id))
        self.badges =      Badges.calculate(raw_data.get('public_flags'))

class ForeignUser(BaseUser):
    def __init__(self, raw_data:dict, session:HTTPClient):
        super().__init__(raw_data)
        self._session = session

    # async def message(self):
    #     return await self._session.request("POST", f"channels/{self.id}/channels")


class ClientUser(BaseUser):
    def __init__(self, raw_data:dict, session:HTTPClient):
        super().__init__(raw_data)

        self.billing = Billing(session)
        self.mfa_enabled = raw_data.get('mfa_enabled')
        self.email =       raw_data.get('email')
        self.verified =    raw_data.get('verified')
        self.phone =       raw_data.get('phone')
        self.locale =      raw_data.get('locale')