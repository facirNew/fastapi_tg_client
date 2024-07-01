import asyncio

from telethon import TelegramClient
from telethon.tl.types import Message, PeerChannel, PeerChat, User


async def message_from_chat_to_dict(client: TelegramClient, messages: list[Message]) -> list:
    """
    Get messages data from Message instances list
    :param client: current telegram client
    :param messages: Message instances list
    :return: list of messages data with 'username', 'is_self', 'message_text' keys
    """
    result = []
    chat_info = await client.get_entity(messages[0].peer_id)
    if type(chat_info) is User:
        chat_title = chat_info.username
    else:
        chat_title = chat_info.title
    tasks = [client.get_entity(message.from_id) if message.from_id else
             client.get_entity(message.peer_id) for message in messages]
    users_info = await asyncio.gather(*tasks)
    for message, user in zip(messages, users_info):
        if message.from_id is None:
            add_message = {'username': chat_title,
                           'is_self': message.out,
                           'message_text': message.text,
                           }
        else:
            add_message = {'username': user.username,
                           'is_self': message.out,
                           'message_text': message.text,
                           }
        result.append(add_message)
    return result


async def sort_by_chats(client: TelegramClient, messages: list[Message]) -> dict:
    """
    Distribute messages among chats
    :param client: current telegram client
    :param messages: Message instances list
    :return: message data distributed across chats
    """
    messages_by_chats = {}
    tasks = [client.get_entity(message.peer_id) for message in messages]
    peer_info = await asyncio.gather(*tasks)
    tasks = [client.get_entity(message.from_id) if message.from_id else
             client.get_entity(message.peer_id) for message in messages]
    user_info = await asyncio.gather(*tasks)
    for message, peer, user in zip(messages, peer_info, user_info):
        if type(message.peer_id) in (PeerChannel, PeerChat):
            if str(message.peer_id) not in messages_by_chats:
                messages_by_chats[str(message.peer_id)] = {'chat_name': peer.title,
                                                           'messages': []}
            if message.from_id is None:
                add_message = {'username': peer.title,
                               'is_self': message.out,
                               'message_text': message.text,
                               }
            else:
                add_message = {'username': user.username,
                               'is_self': message.out,
                               'message_text': message.text,
                               }
            messages_by_chats[str(message.peer_id)]['messages'].append(add_message)
        else:
            if str(message.peer_id) not in messages_by_chats:
                messages_by_chats[str(message.peer_id)] = []
            add_message = {'username': peer.username,
                           'is_self': message.out,
                           'message_text': message.text,
                           }
            messages_by_chats[str(message.peer_id)].append(add_message)
    return messages_by_chats
