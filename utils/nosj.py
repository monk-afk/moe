# moe/utils/nosj.py
# Copyright © 2026 monk <https://github.com/monk-afk>
# SPDX-License-Identifier: MIT
import json
import asyncio
from utils.logroll import logging
log = logging.getLogger(__name__)
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
                log.info("Loaded data from file.")
    except (FileNotFoundError, json.JSONDecodeError):
        log.warning("Creating new data file.")
        data = {}

async def save_file_data():
    async with file_lock:
        with open("moe_data.json", "w") as f:
            json.dump(data, f, indent=None, separators=(",", ":"))
        log.info("OK saved data to file")

async def reset_file_data():
    global data
    log.info("Reset global data file.")
    data = {}
    await save_file_data()

# Set or remove keys from table
async def set_key(guild, user, key, value):
    """
        set_key(guild, user, "input_tokens", [1234])  # set input_token
        set_key(guild, user, "input_tokens", [])      # clear input_token
        set_key(guild, user, "ignore", True)          # set ignore
        set_key(guild, user, "ignore", False)         # unset ignore
        set_key(guild, None, "reply_channel", None)   # unset reply_channel
        set_key(guild, None, "reply_channel", 1234)   # set reply_channel
    """
    if guild not in data:
        data[guild] = {"reply_channel": None, "users": {}}

    if user is None:  # To set reply channel
        data[guild][key] = value

    else:
        if user not in data[guild]["users"]:
            data[guild]["users"][user] = {"ignore": False, "input_tokens": []}
        data[guild]["users"][user][key] = value

    await save_file_data()


# These could be like set_key,
async def get_reply_channel(guild):
    return data.get(guild, {}).get("reply_channel", None)

async def get_input_tokens(guild, user):
    return data.get(guild, {}).get("users", {}).get(user, {}).get("input_tokens", [])

async def is_ignored(guild, user):
    return data.get(guild, {}).get("users", {}).get(user, {}).get("ignore", False)

# Drop guild
async def drop_guild(guild):
    if guild in data:
        data.pop(guild)
        await save_file_data()
        log.info(f"OK drop_data({guild})")

# drop all user tokens in a single guild
async def drop_guild_input_tokens(guild):
    if guild in data and "users" in data[guild]:
        for user in list(data[guild]["users"].keys()):
            await set_key(guild, user, "input_tokens", [])
        log.info(f"OK drop_guild_input_tokens({guild})")

# drop user tokens across all guilds (not implemented yet)
async def drop_user_input_tokens(user):
    for guild in list(data.keys()):
        if "users" in data[guild] and user in data[guild]["users"]:
            await set_key(guild, user, tokens=None)
    log.info(f"OK drop_user_input_tokens({user})")
