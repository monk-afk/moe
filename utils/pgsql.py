# utils/pgsql.py
import psycopg2
from psycopg2 import pool
from psycopg2 import sql
from psycopg2.extras import RealDictCursor
from utils.logroll import logging
log = logging.getLogger(__name__)
from utils.conf import pgsql_db

# Connection pool
def get_connection():
    try:
        return conn_pool.getconn()
    except Exception as e:
        log.error(f"Error get_connection(): {e}")
        raise

def return_connection(conn):
    if conn:
        try:
            conn_pool.putconn(conn)
        except Exception as e:
            log.error(f"Error return_connection(): {e}")
            raise

# Table management
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
            CREATE TABLE IF NOT EXISTS user_data (
                user_id BIGINT,
                guild_id BIGINT,
                reply_to BOOLEAN DEFAULT FALSE,
                input_ids INTEGER[],
                PRIMARY KEY (user_id, guild_id)
            )
        """)

        conn.commit()
        log.info("OK create_tables()")

    except Exception as e:
        log.error(f"Error create_tables(): {e}")
        raise

    finally:
        cursor.close()
        return_connection(conn)

def drop_all_tables():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT current_user")
        current_user = cursor.fetchone()["current_user"]

        if not current_user:
            log.error(f"ERROR current_user = {current_user}")
            return

        log.info(f"OK current_user = {current_user}")

        cursor.execute("""
            SELECT tablename
            FROM pg_tables
            WHERE tableowner = %s and schemaname = 'public';
        """, (current_user,))

        tables = cursor.fetchall()

        if not tables:
            log.warning("OK drop_all_tables(): None")

        else:
            for user_table in tables:
                table_name = user_table["tablename"]
                cursor.execute(sql.SQL("DROP TABLE IF EXISTS {} CASCADE").format(sql.Identifier(table_name)))
                log.info(f"OK drop_all_tables(): {table_name}")

        conn.commit()

    except Exception as e:
        log.error(f"ERROR drop_all_tables(): {e}")
        conn.rollback()
        raise

    finally:
        cursor.close()
        return_connection(conn)

# Manage designated reply channel
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
        log.info(f"OK set_reply_channel({guild_id}, {channel_id})")

    except Exception as e:
        log.error(f"Error set_reply_channel({guild_id}, {channel_id}): {e}")
        raise

    finally:
        cursor.close()
        return_connection(conn)

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
        channel_id = result["reply_channel"] if result else None

        log.info(f"OK get_reply_channel({guild_id}): {channel_id}")
        return channel_id

    except Exception as e:
        log.error(f"Error get_reply_channel({guild_id}): {e}")
        return None

    finally:
        cursor.close()
        return_connection(conn)

def drop_reply_channel(guild_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
          DELETE FROM guild_data
          WHERE guild_id = %s
        """, (guild_id,))
        conn.commit()
        log.info(f"OK drop_reply_channel({guild_id})")

    except Exception as e:
        log.error(f"Error drop_reply_channel({guild_id}): {e}")
        raise

    finally:
        cursor.close()
        return_connection(conn)

# Drop all guild data
def drop_guild_data(guild_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            DELETE FROM user_data
            WHERE guild_id = %s
        """, (guild_id,))

        cursor.execute("""
            DELETE FROM guild_data
            WHERE guild_id = %s
        """, (guild_id,))
        conn.commit()
        log.info(f"OK drop_guild_data({guild_id})")

    except Exception as e:
        log.error(f"Error drop_guild_data({guild_id}): {e}")
        raise

    finally:
        cursor.close()
        return_connection(conn)

# Manage input ids (tokens)
def set_input_ids(guild_id, user_id, input_ids):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO user_data (user_id, guild_id, input_ids)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, guild_id) DO UPDATE
            SET input_ids = EXCLUDED.input_ids
        """, (user_id, guild_id, input_ids))
        conn.commit()
        log.info(f"OK set_input_ids({guild_id}, {user_id}, {input_ids})")

    except Exception as e:
        log.error(f"Error set_input_ids({guild_id}, {user_id}, {input_ids}): {e}")
        raise

    finally:
        cursor.close()
        return_connection(conn)

def get_input_ids(guild_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT input_ids
            FROM user_data
            WHERE user_id = %s
            AND guild_id = %s
        """, (user_id, guild_id))
        result = cursor.fetchone()
        input_ids = result["input_ids"] if result else None
        log.info(f"OK get_input_ids({guild_id}, {user_id}): {input_ids}")
        return input_ids

    except Exception as e:
        log.error(f"Error get_input_ids({guild_id}, {user_id}): {e}")
        return []

    finally:
        cursor.close()
        return_connection(conn)

def drop_user_input_ids(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
          DELETE FROM user_data
          WHERE user_id = %s
        """, (user_id,))
        conn.commit()
        log.info(f"OK drop_user_input_ids({user_id})")

    except Exception as e:
        log.error(f"Error drop_user_input_ids({user_id}): {e}")
        raise

    finally:
        cursor.close()
        return_connection(conn)

def drop_guild_input_ids(guild_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
          DELETE FROM user_data
          WHERE guild_id = %s
        """, (guild_id,))
        conn.commit()
        log.info(f"OK drop_guild_input_ids({guild_id})")

    except Exception as e:
        log.error(f"Error drop_guild_input_ids({guild_id}): {e}")
        raise

    finally:
        cursor.close()
        return_connection(conn)

# Manage reply-to user
def set_reply_to(guild_id, user_id, reply_to):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            INSERT INTO user_data (user_id, guild_id, reply_to)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, guild_id) DO UPDATE
            SET reply_to = EXCLUDED.reply_to
        """, (user_id, guild_id, reply_to))
        conn.commit()
        log.info(f"OK set_reply_to({guild_id}, {user_id}, {reply_to})")

    except Exception as e:
        log.error(f"Error set_reply_to({guild_id}, {user_id}, {reply_to}): {e}")
        raise

    finally:
        cursor.close()
        return_connection(conn)

def check_reply_to(guild_id, user_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT reply_to
            FROM user_data
            WHERE user_id = %s
            AND guild_id = %s
        """, (user_id, guild_id))
        result = cursor.fetchone()
        reply_to = result["reply_to"] if result else False
        log.info(f"OK check_reply_to({guild_id}, {user_id}): {reply_to}")
        return reply_to

    except Exception as e:
        log.error(f"Error check_reply_to({guild_id}, {user_id}): {e}")
        return False

    finally:
        cursor.close()
        return_connection(conn)

# Initialize connection pool
try:
    conn_pool = psycopg2.pool.SimpleConnectionPool(
        1, 50,  # min/max pool connections
        dsn=pgsql_db,
        cursor_factory=RealDictCursor
    )
    if conn_pool:
        log.info(f"OK psycopg2.pool.SimpleConnectionPool: {conn_pool}")
        create_tables()

except Exception as e:
    log.error(f"Error psycopg2.pool.SimpleConnectionPool: {e}")
    raise



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