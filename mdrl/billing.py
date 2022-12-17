class Billing:
    def __init__(self, session):
        self._session = session
        self.payment_methods = None
        
    async def get_payment_methods(self) -> dict:
        return await self._session.request("GET", "users/@me/billing/payment-sources")

    async def get_payment_history(self, limit: int = 20) -> dict:
        return await self._session.request("GET", f"users/@me/billing/payments?limit={limit}")