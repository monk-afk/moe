# moe/utils/nosj.py
# Copyright © 2026 monk <https://github.com/monk-afk>
# SPDX-License-Identifier: MIT
import json
import asyncio

from pathlib import Path
from cryptography.fernet import Fernet
from utils.conf import config

file_lock = asyncio.Lock()
cipher = Fernet(config.storage_key.encode())
data = {}

# JSON tables are string keys, we need integers
def convert_keys_to_int(d):
    if isinstance(d, dict):
        new = {}
        for k, v in d.items():
            try:
                ik = int(k)
            except ValueError:
                ik = k  # leave non-numeric keys as-is
            new[ik] = convert_keys_to_int(v)
        return new
    elif isinstance(d, list):
        return [convert_keys_to_int(i) for i in d]
    else:
        return d

# File management
async def load_file_data():
    global data
    try:
        async with file_lock:
            with open("moe_data.json", "rb") as f:
                payload = cipher.decrypt(f.read())

            loaded_data = json.loads(payload)

            if isinstance(loaded_data, dict):
                loaded_data = convert_keys_to_int(loaded_data)
                data.update(loaded_data)

    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

async def save_file_data():
    payload = json.dumps(data, separators=(",", ":")).encode()
    async with file_lock:
        with open("moe_data.json", "wb") as f:
            f.write(cipher.encrypt(payload))

async def reset_file_data():
    global data
    data = {}
    await save_file_data()


# Blocked users
async def get_ignore(user):
    return data.get(user, {}).get("ignore", False)

async def set_ignore(user, value):
    if value:
        await drop_user_data(user)
        data[user] = {"ignore": True}
    else:
        data.pop(user, None)


# Reply channel
async def get_reply_channel(guild):
    return data.get(guild, {}).get("reply_channel", None)

async def set_reply_channel(guild, value):
    if guild not in data:
        data[guild] = {"reply_channel": None, "chats": {}}
    data[guild]["reply_channel"] = value
    await save_file_data()


# Saving and fetching message tokens
async def get_input_tokens(guild, user_or_channel):
    return data.get(guild, {}).get("chats", {}).get(user_or_channel, [])

async def set_input_tokens(guild, user_or_channel, value):
    if guild not in data:
        data[guild] = {"reply_channel": None, "chats": {}}
    data[guild]["chats"][user_or_channel] = value


# Drop guild
async def drop_guild(guild):
    if guild in data:
        data.pop(guild)
        await save_file_data()

# drop all user tokens from a single guild, doesn't affect reply channel
async def drop_guild_input_tokens(guild):
    if guild in data and "chats" in data[guild]:
        for user_or_channel in list(data[guild]["chats"].keys()):
            data[guild]["chats"].pop(user_or_channel)
        await save_file_data()

# Drop tokens from one guild, or from every guild when guild is None
async def drop_user_data(user_or_channel, guild=None):
    guilds = [guild] if guild is not None else list(data.keys())

    for guild_id in guilds:
        chats = data.get(guild_id, {}).get("chats", {})
        chats.pop(user_or_channel, None)
    await save_file_data()
