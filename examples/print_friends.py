import asyncio
import mdrl
from dotenv import load_dotenv
import os

async def main():
    token = os.getenv('DISCORD_TOKEN')

    async with mdrl.DiscordClient() as client:
        try:
            await client.login(token=token)
        except mdrl.Unauthorized:
            print('Token incorrect')
            exit()
        except mdrl.Forbidden:
            print('Account Locked')
            exit()
        
        relationships = await client.get_relationships()

        for friend in relationships.friends:
            print(friend.username)
            
if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())