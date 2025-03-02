# pgsql_tables.py
# make sure this is in the project root
import os
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from utils.pgsql import (
    create_tables,
    drop_all_tables,
    set_reply_channel,
    get_reply_channel,
    drop_reply_channel,
    drop_guild_data,
    set_input_ids,
    get_input_ids,
    drop_input_ids,
    set_reply_to,
    check_reply_to
)

def test_create_drop_tables():
    guild_id = 9876543210
    user_id = 1234567890
    channel_id = 6758493021
    input_ids = [1, 2, 3, 4, 5]

    try:
        drop_all_tables()
        create_tables()
        test_input_ids(guild_id, user_id, input_ids)
        test_reply_channel(guild_id, channel_id)
        test_reply_to(guild_id, user_id)
        drop_guild_data(guild_id)
        drop_all_tables()

    except Exception as e:
        print(f"Error in create/drop tables: {e}")

def test_reply_channel(guild_id, channel_id):
    try:
        set_reply_channel(guild_id, channel_id)
        reply_channel = get_reply_channel(guild_id)
        if reply_channel == channel_id:
            drop_reply_channel(channel_id)
        else:
            print(f"ERROR {reply_channel} == {channel_id}")
    except Exception as e:
        print(f"CAUGHT EXCEPTION {e}")

def test_input_ids(guild_id, user_id, input_ids):
    try:
        set_input_ids(guild_id, user_id, input_ids)
        received = get_input_ids(guild_id, user_id)
        if received == input_ids:
            drop_input_ids(user_id)
        else:
            print(f"ERROR {received} == {input_ids}")
    except Exception as e:
        print(f"Error in set/get input IDs: {e}")

def test_reply_to(guild_id, user_id):
    try:
        set_reply_to(guild_id, user_id, True)
        reply_to = check_reply_to(guild_id, user_id)
        if reply_to is True:
            set_reply_to(guild_id, user_id, False)
        else:
            print(f"ERROR reply_to is True")
    except Exception as e:
        print(f"CAUGHT {e}")

if __name__ == "__main__":
    test_create_drop_tables()


####################################################################################
# MIT License                                                                      #
#                                                                                  #
# Copyright (c) 2024 monk                                                          #
#                                                                                  #
# Permission is hereby granted, free of charge, to any person obtaining a copy     #
# of this software and associated documentation files (the "Software"), to deal    #
# in the Software without restriction, including without limitation the rights     #
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell        #
# copies of the Software, and to permit persons to whom the Software is            #
# furnished to do so, subject to the following conditions:                         #
#                                                                                  #
# The above copyright notice and this permission notice shall be included in all   #
# copies or substantial portions of the Software.                                  #
#                                                                                  #
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR       #
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,         #
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE      #
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER           #
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,    #
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE    #
# SOFTWARE.                                                                        #
####################################################################################