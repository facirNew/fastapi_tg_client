import io

import qrcode
from config import settings
from database.connect import minio_connection, mongo_connection
from loguru import logger
from telethon.sync import TelegramClient
from utils.tg_utils import message_from_chat_to_dict, sort_by_chats


async def get_client() -> TelegramClient:
    """
    Create telegram client and connect them
    """
    client = TelegramClient(mongo_connection.session,
                            settings.API_ID,
                            settings.API_HASH,
                            system_version='4.16.30-vxCUSTOM')
    if not client.is_connected():
        await client.connect()
    return client


async def check_auth(phone) -> str | bool:
    """
    Check authorisation status
    :param phone: user phone number for check
    """
    try:
        client = await get_client()
        is_auth = await client.is_user_authorized()
        if not is_auth:
            return 'waiting_qr_login'
        same_user = await check_user(phone)
        if not same_user:
            return 'waiting_qr_login'
        logger.info(is_auth)
    except Exception as e:
        logger.error(e)
        return 'error'
    return 'logined'


async def generate_qr_code(phone: str) -> str:
    """
    Generate qr code for login
    :param phone: user phone number for login
    :return: link on qr code
    """
    client = await get_client()

    if await client.is_user_authorized() and not await check_user(phone):
        await client.log_out()
    if not await client.is_user_authorized():
        qr_login = await client.qr_login()
        qr = qrcode.make(qr_login.url)
        img_io = io.BytesIO()
        qr.save(img_io, 'PNG')
        img_io.seek(0)
        filename = f'{str(hash(qr_login.token))}.png'
        minio_connection.upload_file(img_io, filename, 'qrcode')
        return minio_connection.get_file_link(filename, 'qrcode')


async def user_logout(phone: str) -> None:
    """
    Logout user
    :param phone: user phone number for logout
    """
    client = await get_client()
    if await check_user(phone):
        await client.log_out()


async def check_user(phone: str) -> bool:
    """
    Check if the user is logged-in
    :param phone: user phone for check
    :return: True if logged-in user with input phone
    """
    client = await get_client()
    user = await client.get_me()
    if not user:
        return False
    if user.phone != phone:
        return False
    return True


async def fetch_messages(phone: str, uname: str | None = None) -> dict:
    """
    Receive 50 messages from all sources or one chat
    :param phone: login user phone
    :param uname: name of user or chat
    """
    client = await get_client()
    if not await check_user(phone):
        return {'error': 'user not authorized'}
    try:
        messages = await client.get_messages(uname, limit=50)
    except Exception as e:
        logger.error(e)
        return {'error': str(e)}
    if not messages:
        return {'messages': []}
    if not uname:
        result = await sort_by_chats(client=client, messages=messages)
    else:
        result = await message_from_chat_to_dict(client=client, messages=messages)
    return result


async def send_tg_message(phone: str,
                          username: str,
                          message_text: str | None = None) -> None:
    """
    Send message
    :param phone: current user phone number
    :param username: receiver name
    :param message_text: message text
    """
    client = await get_client()
    if not await check_user(phone):
        raise PermissionError('user not authorized')
    await client.send_message(username, message=message_text)
