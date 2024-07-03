import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from utils.logroll import log
from utils.conf import pgsql_db

# connection pool initialization
try:
    conn_pool = psycopg2.pool.SimpleConnectionPool(
        1, 50,  # min/max pool connections
        dsn=pgsql_db,
        cursor_factory=RealDictCursor
    )
    if conn_pool:
        log.info('Connection pool created successfully')
except Exception as e:
    log.error(f'Error creating connection pool: {e}')
    raise

# get connection from pool
def get_connection():
    try:
        return conn_pool.getconn()
    except Exception as e:
        log.error(f'Error getting connection from pool: {e}')
        raise

# return connection to pool
def return_connection(conn):
    try:
        conn_pool.putconn(conn)
    except Exception as e:
        log.error(f'Error returning connection to pool: {e}')
        raise

# create tables if they don't exist
def create_tables():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS guild_data (
                guild_id BIGINT PRIMARY KEY,
                reply_channel BIGINT
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS channel_data (
                channel_id BIGINT PRIMARY KEY,
                guild_id BIGINT,
                input_ids INTEGER[]
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id BIGINT PRIMARY KEY,
                input_ids INTEGER[]
            )
        """)
        conn.commit()
        log.info('Tables created or verified successfully')
    except Exception as e:
        log.error(f'Error creating tables: {e}')
        raise
    finally:
        cursor.close()
        return_connection(conn)

# Functions to set/update

def set_reply_channel(guild_id, channel_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO guild_data (guild_id, reply_channel)
            VALUES (%s, %s)
            ON CONFLICT (guild_id) DO UPDATE
            SET reply_channel = EXCLUDED.reply_channel
        """, (guild_id, channel_id))
        conn.commit()
        log.info(f"Reply channel in guild {guild_id} set to {channel_id}")
    except Exception as e:
        log.error(f'Error setting reply channel in guild {guild_id}: {e}')
        raise
    finally:
        cursor.close()
        return_connection(conn)

# set/update bot input ids for a channel
def set_channel_bot_input_ids(channel_id, guild_id, input_ids):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO channel_data (channel_id, guild_id, input_ids)
            VALUES (%s, %s, %s)
            ON CONFLICT (channel_id) DO UPDATE
            SET input_ids = EXCLUDED.input_ids
        """, (channel_id, guild_id, input_ids))
        conn.commit()
        log.info(f'Set {guild_id}/{channel_id} input_ids: {input_ids}')
    except Exception as e:
        log.error(f'Error setting {guild_id}/{channel_id} input_ids: {e}')
        raise
    finally:
        cursor.close()
        return_connection(conn)

# set/update bot input ids for a user
def set_user_bot_input_ids(user_id, input_ids):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO user_data (user_id, input_ids)
            VALUES (%s, %s)
            ON CONFLICT (user_id) DO UPDATE
            SET input_ids = EXCLUDED.input_ids
        """, (user_id, input_ids))
        conn.commit()
        log.info(f'Set user {user_id} input_ids: {input_ids}')
    except Exception as e:
        log.error(f'Error setting user {user_id} input_ids: {e}')
        raise
    finally:
        cursor.close()
        return_connection(conn)

# get reply channel for a guild
def get_reply_channel(guild_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT reply_channel
            FROM guild_data
            WHERE guild_id = %s
        """, (guild_id,))
        result = cursor.fetchone()
        log.info(f'Fetched reply channel {guild_id}:{result}')
        return result['reply_channel'] if result else None
    except Exception as e:
        log.error(f'Error fetching reply channel for guild {guild_id}: {e}')
        return None
    finally:
        cursor.close()
        return_connection(conn)

# get bot input ids for a channel
def get_channel_input_ids(channel_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT input_ids
            FROM channel_data
            WHERE channel_id = %s
        """, (channel_id,))
        result = cursor.fetchone()
        input_ids = result['input_ids'] if result and result['input_ids'] else []
        log.info(f'Fetched channel input ids {channel_id}:{input_ids}')
        return input_ids
    except Exception as e:
        log.error(f'Error fetching input_ids for channel {channel_id}: {e}')
        return []
    finally:
        cursor.close()
        return_connection(conn)

# get bot input ids for a user
def get_user_input_ids(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT input_ids
            FROM user_data
            WHERE user_id = %s
        """, (user_id,))
        result = cursor.fetchone()
        input_ids = result['input_ids'] if result and result['input_ids'] else []
        log.info(f'Fetched user input ids {user_id}:{input_ids}')
        return input_ids
    except Exception as e:
        log.error(f'Error fetching input_ids for user {user_id}: {e}')
        return []
    finally:
        cursor.close()
        return_connection(conn)

# drop all tables ONLY FOR TESTING! 
def drop_all_tables():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DROP TABLE IF EXISTS guild_data CASCADE")
        cursor.execute("DROP TABLE IF EXISTS channel_data CASCADE")
        cursor.execute("DROP TABLE IF EXISTS user_data CASCADE")
        conn.commit()
        log.info('Tables dropped successfully')
    except Exception as e:
        log.error(f'Error dropping tables: {e}')
        raise
    finally:
        cursor.close()
        return_connection(conn)

# drop guild reply channel
def drop_guild_reply_channel(guild_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
          DELETE FROM guild_data
          WHERE guild_id = %s
        """, (guild_id,))
        conn.commit()
        log.info(f'Cleared guild reply_channel {guild_id}')
    except Exception as e:
        log.error(f'Error clearing guild reply_channel {guild_id}: {e}')
        raise
    finally:
        cursor.close()
        return_connection(conn)

# drop channel input ids
def drop_channel_input_ids(channel_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
          DELETE FROM channel_data
          WHERE channel_id = %s
        """, (channel_id,))
        conn.commit()
        log.info(f'Cleared channel input_ids {channel_id}')
    except Exception as e:
        log.error(f'Error clearing channel input_ids {channel_id}: {e}')
        raise
    finally:
        cursor.close()
        return_connection(conn)

# drop user input ids
def drop_user_input_ids(user_id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
          DELETE FROM user_data
          WHERE user_id = %s
        """, (user_id,))
        conn.commit()
        log.info(f'Cleared user input_ids {user_id}')
    except Exception as e:
        log.error(f'Error clearing user input_ids {user_id}: {e}')
        raise
    finally:
        cursor.close()
        return_connection(conn)

# Main execute setup or teardown
if __name__ == "__main__":
    try:
        create_tables()  # Create tables if they don't exist
        # drop_all_tables()   # Uncomment to drop tables (use with caution!)
    except Exception as e:
        log.error(f'Error setting up tables: {e}')
    finally:
        if conn_pool:
            conn_pool.closeall()
            log.info('Connection pool closed')