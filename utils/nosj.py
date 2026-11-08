# moe/utils/nosj.py
# Copyright © 2026 monk <https://github.com/monk-afk>
# SPDX-License-Identifier: MIT
import json
import asyncio
file_lock = asyncio.Lock()
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
            with open("moe_data.json", "r") as f:
                loaded_data = json.load(f)
                if isinstance(loaded_data, dict):
                    loaded_data = convert_keys_to_int(loaded_data)
                    data.update(loaded_data)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

async def save_file_data():
    async with file_lock:
        with open("moe_data.json", "w") as f:
            json.dump(data, f, indent=None, separators=(",", ":"))

async def reset_file_data():
    global data
    data = {}
    await save_file_data()


async def get_ignore(user):
    return data.get(user, {}).get("ignore", False)

async def set_ignore(user, value):
    if value:
        data[user] = {"ignore": True}
    else:
        data.pop(user, None)


# These could be like set_key,
async def get_reply_channel(guild):
    return data.get(guild, {}).get("reply_channel", None)

async def set_reply_channel(guild, value):
    if guild not in data:
        data[guild] = {"reply_channel": None, "chats": {}}
    data[guild]["reply_channel"] = value


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

# drop user tokens across all guilds
async def drop_user_data(user_or_channel):
    for guild in list(data.keys()):
        if "chats" in data[guild] and user_or_channel in data[guild]["chats"]:
            data[guild]["chats"].pop(user_or_channel)
