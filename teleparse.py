import configparser
from telethon.sync import TelegramClient
from telethon.sync import TelegramClient, events
import asyncio
import json
from asgiref.sync import sync_to_async
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.types import PeerChannel
from telethon.tl.types.messages import ChannelMessages
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.messages import GetDialogsRequest
import telethon.tl.types as chattype
from telethon.errors import *
import info_parse
import datetime

config = configparser.ConfigParser()
config.read("config.ini")

api_id = config['Telegram']['api_id']
api_hash = config['Telegram']['api_hash']
api_hash = str(api_hash)


phone = config['Telegram']['phone']
username = config['Telegram']['username']

client = TelegramClient(phone, api_id, api_hash)


async def join_group(group_link):
    await client(JoinChannelRequest(group_link))


async def run_client():
    await client.start()


async def get_all_groups():
    chats = []
    last_date = None
    size_chats = 100
    groups = []
    result = await client(GetDialogsRequest(
        offset_date=last_date,
        offset_id=0,
        offset_peer=InputPeerEmpty(),
        limit=size_chats,
        hash=0
    ))
    chats.extend(result.chats)
    for chat in chats:
        if not isinstance(chat, chattype.ChatForbidden):
            groups.append(chat)
    # print(groups)
    return groups


async def get_new_messages(chat):
    offset_id = 0
    limit = 10
    try:
        history = await client(GetHistoryRequest(
            peer=chat,
            offset_id=offset_id,
            offset_date=None,
            add_offset=0,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ))
    except ChannelInvalidError:
        print(1)
    except ChannelPrivateError:
        print(2)
    except ChatIdInvalidError:
        print(3)
    except PeerIdInvalidError:
        print(4)
    except TimeoutError:
        print(5)

    data = history.to_dict()
    try:
        res = info_parse.get_data(data)
    except:
        pass
        return
    return res
