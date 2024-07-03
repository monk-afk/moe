import os
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from utils.pgsql import (
    create_tables,
    drop_all_tables,
    set_reply_channel,
    set_channel_bot_input_ids,
    set_user_bot_input_ids,
    get_reply_channel,
    get_channel_input_ids,
    get_user_input_ids,
    drop_channel_input_ids,
    drop_user_input_ids,
    drop_guild_reply_channel
)

def test_create_drop_tables():
    try:
        drop_all_tables()
        print("Tables dropped")
        create_tables()
        print("Tables created")

        test_set_get_reply_channel()
        test_set_get_channel_bot_input_ids()
        test_set_get_user_bot_input_ids()

        drop_all_tables()
        print("Tables dropped")
    except Exception as e:
        print(f"Error in create/drop tables: {e}")

def test_set_get_reply_channel():
    try:
        set_reply_channel(123456789, 987654321)
        reply_channel = get_reply_channel(123456789)
        if reply_channel == 987654321:
            print("Set and fetched reply channel")
            drop_guild_reply_channel(123456789)
            print("Dropped reply channel")
        else:
            print("Mismatch in set and fetched reply channel")
    except Exception as e:
        print(f"Error in set/get reply channel: {e}")

def test_set_get_channel_bot_input_ids():
    try:
        set_channel_bot_input_ids(987654321, 123456789, [1, 2, 3, 4, 5])
        input_ids = get_channel_input_ids(987654321)
        if input_ids == [1, 2, 3, 4, 5]:
            print("Set and fetched channel bot input IDs")
            drop_channel_input_ids(987654321)
            print("Dropped channel bot input IDs")
        else:
            print("Mismatch in set and fetched channel bot input IDs")
    except Exception as e:
        print(f"Error in set/get channel bot input IDs: {e}")

def test_set_get_user_bot_input_ids():
    try:
        set_user_bot_input_ids(111222333, [10, 20, 30])
        input_ids = get_user_input_ids(111222333)
        if input_ids == [10, 20, 30]:
            print("Set and fetched user bot input IDs")
            drop_user_input_ids(111222333)
            print("Dropped user bot input IDs")
        else:
            print("Mismatch in set and fetched user bot input IDs")
    except Exception as e:
        print(f"Error in set/get user bot input IDs: {e}")

if __name__ == "__main__":
    test_create_drop_tables()
