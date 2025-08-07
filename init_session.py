# This file is only used to initialize the Telethon session that can then be used by the main app.
# It should be run once to create the session file.

# api_id and api_hash can be obtained from https://my.telegram.org/apps and will be required for the main app to function.
# input them when prompted.

from telethon import TelegramClient
import os
import asyncio
async def init_session(api_id, api_hash, phone):
    client = TelegramClient('telegram_channel_reader', api_id, api_hash)
    await client.start(phone)

    print("Session initialized successfully. You can now run the main app. Remember to keep the session file 'telegram_channel_reader.session' and 'session_info.txt' safe and to put it in the same directory as the main app if you deploy it.")
    await client.disconnect()
if __name__ == '__main__':
    api_id = input("Enter your API ID: ")
    api_hash = input("Enter your API Hash: ")
    phone = input("Enter your phone number (with country code): ")
    #save all 3 inputs to a file so that they can be used by the main app
    with open('session_info.txt', 'w') as f:
        f.write(f"{api_id}\n{api_hash}\n{phone}\n")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(init_session(api_id, api_hash, phone))
    loop.close()