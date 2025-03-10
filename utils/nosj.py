# utils/nosj.py
import json
import asyncio
from utils.logroll import logging
log = logging.getLogger(__name__)
file_lock = asyncio.Lock()
data = {}

# File management
async def load_file_data():
    global data
    try:
        async with file_lock:
            with open("moe_data.json", "r") as f:
                loaded_data = json.load(f)
                if isinstance(loaded_data, dict):
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

async def show_file_data():
    return json.dumps(data, indent=None, separators=(",", ":"))

async def reset_file_data():
    global data
    log.info("Reset global data file.")
    data = {}
    await save_file_data()

# to create non-existing tables
def create_table_not_in_data(guild, user=None):
    if guild not in data:
        data[guild] = {"reply_channel": None, "users": {}}

    if user is not None and user not in data[guild]["users"]:
        data[guild]["users"][user] = {"reply_to": False, "input_tokens": []}

# Set or remove keys from table
async def set_key(guild, user, key, value):
    """ 
        set_key(guild, user, "input_tokens", [1234])  # set input token
        set_key(guild, user, "input_tokens", [])      # clear input token
        set_key(guild, user, "reply_to", True)        # set reply_to
        set_key(guild, user, "reply_to", False)       # unset reply_to
        set_key(guild, None, "reply_channel", None)   # unset reply_channel
        set_key(guild, None, "reply_channel", 1234)   # set reply_channel
    """
    if guild not in data:
        data[guild] = {"reply_channel": None, "users": {}}

    if user is None:  # To set reply channel
        data[guild][key] = value

    else:
        if user not in data[guild]["users"]:
            data[guild]["users"][user] = {"reply_to": False, "input_tokens": []}
        data[guild]["users"][user][key] = value

# These could be like set_key,
async def get_reply_channel(guild):
    return data.get(guild, {}).get("reply_channel", None)

async def get_input_tokens(guild, user):
    return data.get(guild, {}).get("users", {}).get(user, {}).get("input_tokens", [])

async def get_reply_to(guild, user):
    return data.get(guild, {}).get("users", {}).get(user, {}).get("reply_to", False)

# Drop guild
async def drop_guild(guild):
    if guild in data:
        data.pop(guild)
        log.info(f"OK drop_data({guild})")
    await save_file_data()

# drop all user tokens in a single guild
async def drop_guild_input_tokens(guild):
    if guild in data and "users" in data[guild]:
        for user in list(data[guild]["users"].keys()):
            await set_input_tokens(guild, user, "input_tokens", [])
        log.info(f"OK drop_guild_input_tokens({guild})")

# drop user tokens across all guilds (not implemented yet)
async def drop_user_input_tokens(user): 
    for guild in list(data.keys()):
        if "users" in data[guild] and user in data[guild]["users"]:
            await set_input_tokens(guild, user, tokens=None)
    log.info(f"OK drop_user_input_tokens({user})")



######################################################################################
##  MIT License                                                                     ##
##                                                                                  ##
##  Copyright © 2024-2025 monk (Discord ID: 699370563235479624)                     ##
##                                                                                  ##
##  Permission is hereby granted, free of charge, to any person obtaining a copy    ##
##  of this software and associated documentation files (the "Software"), to deal   ##
##  in the Software without restriction, including without limitation the rights    ##
##  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell       ##
##  copies of the Software, and to permit persons to whom the Software is           ##
##  furnished to do so, subject to the following conditions:                        ##
##                                                                                  ##
##  The above copyright notice and this permission notice shall be included in all  ##
##  copies or substantial portions of the Software.                                 ##
##                                                                                  ##
##  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR      ##
##  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,        ##
##  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE     ##
##  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER          ##
##  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,   ##
##  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE   ##
##  SOFTWARE.                                                                       ##
######################################################################################