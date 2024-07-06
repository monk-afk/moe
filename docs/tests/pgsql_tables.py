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
    get_channel_input_ids,
    set_channel_input_ids,
    drop_channel_input_ids
    # get_user_input_ids,
    # set_user_input_ids,
    # drop_user_input_ids,
)

def test_create_drop_tables():
    try:
        drop_all_tables()
        print("Tables dropped")
        create_tables()
        print("Tables created")

        test_reply_channel()
        test_channel_input_ids()
        # test_user_input_ids()

        drop_all_tables()
        print("Tables dropped")
    except Exception as e:
        print(f"Error in create/drop tables: {e}")

def test_reply_channel():
    try:
        set_reply_channel(123456789, 987654321)
        reply_channel = get_reply_channel(123456789)
        if reply_channel == 987654321:
            print("Set and fetched reply channel")
            drop_reply_channel(123456789)
            print("Dropped reply channel")
        else:
            print("Mismatch in set and fetched reply channel")
    except Exception as e:
        print(f"Error in set/get reply channel: {e}")

def test_channel_input_ids():
    try:
        set_channel_input_ids(987654321, 123456789, [1, 2, 3, 4, 5])
        input_ids = get_channel_input_ids(987654321)
        if input_ids == [1, 2, 3, 4, 5]:
            print("Set and fetched channel bot input IDs")
            drop_channel_input_ids(987654321)
            print("Dropped channel bot input IDs")
        else:
            print("Mismatch in set and fetched channel bot input IDs")
    except Exception as e:
        print(f"Error in set/get channel bot input IDs: {e}")

# def test_user_input_ids():
#     try:
#         set_user_input_ids(111222333, [10, 20, 30])
#         input_ids = get_user_input_ids(111222333)
#         if input_ids == [10, 20, 30]:
#             print("Set and fetched user bot input IDs")
#             drop_user_input_ids(111222333)
#             print("Dropped user bot input IDs")
#         else:
#             print("Mismatch in set and fetched user bot input IDs")
#     except Exception as e:
#         print(f"Error in set/get user bot input IDs: {e}")

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