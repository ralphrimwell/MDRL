import asyncio
import mdrl
from dotenv import load_dotenv
import os

async def main():
    """ fetch all dms/private channels and iteratively send message of choice """

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
        
        dms = await client.get_private_channels()
        for dm in dms:
            print('======================================================')
            print('Recipients:')
            for recipient in dm.recipients:
                print(f"    {recipient.name}")
            print('')
            content = input('What message do you want to send? Leave blank to skip. ')
            if content:
                await dm.message(content)

            
if __name__ == "__main__":
    load_dotenv()
    asyncio.run(main())