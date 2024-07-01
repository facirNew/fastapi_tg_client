from fastapi import APIRouter
from fastapi.responses import JSONResponse
from loguru import logger
from models.fastapi_models import MessageModel, PhoneNumberModel
from tg import check_auth, fetch_messages, generate_qr_code, send_tg_message, user_logout

root_router = APIRouter(
    prefix='',
    tags=['root'],
    responses={404: {'description': 'Not found'}},
)


@root_router.post('/login')
async def login(user_phone: PhoneNumberModel) -> JSONResponse:
    """
    Send link for user login
    :param user_phone: PhoneNumberModel with number of the user being login
    """
    qrcode = await generate_qr_code(user_phone.phone)
    return JSONResponse({'qr_link_url': qrcode})


@root_router.post('/logout')
async def logout(user_phone: PhoneNumberModel) -> JSONResponse:
    """
    Logout user from current session
    :param user_phone: PhoneNumberModel with number of the user being logout
    """
    try:
        await user_logout(user_phone.phone)
        return JSONResponse({'status': 'logged out'})
    except Exception as e:
        return JSONResponse({'error': e})


@root_router.get('/check/login')
async def login_status(phone: str) -> JSONResponse:
    """
    Check user login status
    :param phone: number of the user being checked
    """
    status = await check_auth(phone)
    return JSONResponse({'status': status})


@root_router.get('/messages')
async def get_messages(phone: str, uname: str | None = None) -> JSONResponse:
    """
    Get last 50 messages from uname chat
    :param phone: loggined phone
    :param uname: name of chat or user from whom messages are taken
    """
    messages = await fetch_messages(phone, uname)
    return JSONResponse(messages)


@root_router.post('/messages')
async def send_messages_to_tg(message: MessageModel) -> JSONResponse:
    """
    Send text message
    :param message: MessageModel instance
    """
    try:
        await send_tg_message(phone=message.from_phone,
                              username=message.username,
                              message_text=message.message_text)
        return JSONResponse({'status': 'ok'})
    except Exception as e:
        logger.error(e)
        return JSONResponse({'status': 'error'})
