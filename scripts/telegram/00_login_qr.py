"""
Log in to Telegram via QR code (no login code needed).
Run once -> afterwards 01_collect_telegram.py works without logging in again.
  pip install qrcode
Requires the environment variables TG_API_ID and TG_API_HASH (from https://my.telegram.org).
"""
import os
import asyncio
from getpass import getpass
import qrcode
from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

API_ID = int(os.environ["TG_API_ID"])        # never write credentials into the code
API_HASH = os.environ["TG_API_HASH"]
SESSION_NAME = "sitzung"                     # name of the existing session file (sitzung.session) – do not change


async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)   # same session name as in the collection scripts
    await client.connect()

    if await client.is_user_authorized():
        print("Already logged in.")
        await client.disconnect()
        return

    qr_login = await client.qr_login()
    while True:
        qr = qrcode.QRCode()
        qr.add_data(qr_login.url)
        qr.print_ascii(invert=True)
        print("\nPhone: Telegram > Settings > Devices > Link Desktop Device > scan QR code")
        try:
            await qr_login.wait(timeout=60)
            break
        except asyncio.TimeoutError:
            print("QR code expired – new QR code:")
            await qr_login.recreate()
        except SessionPasswordNeededError:
            await client.sign_in(password=getpass("Two-factor password: "))
            break

    me = await client.get_me()
    print(f"Logged in as: {me.first_name}")
    await client.disconnect()


asyncio.run(main())
