import psycopg2

from user import User
from base import Session
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def get_user_discord_id(id_user_discord):
    """ query data from the vendors table """
    conn = None
    user = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(f"SELECT user_discord_id FROM users WHERE user_discord_id = '{id_user_discord}'")
        user = cur.fetchone()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return user

async def get_user_id(id_user_discord):
    """ query data from the vendors table """
    conn = None
    user = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(f"SELECT user_id FROM users WHERE user_discord_id = '{id_user_discord}'")
        user = cur.fetchone()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return user

async def register_user(id_user_discord):
    """ insert a new user into the users table """
    sql = f"INSERT INTO users(user_discord_id,superballs,ultraballs,masterballs) VALUES({id_user_discord},50,25,1) RETURNING user_id;"

    conn = None
    user_id = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # get the generated id back
        user_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return user_id


async def set_active_pokemon(pokemon_id):
    sql = f"UPDATE sys_vars SET var_value= {str(pokemon_id)}, updated_at = current_timestamp WHERE var_name = " \
          f"'ACTIVE_POKEMON'; "

    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

async def insert_pokemon_captured(id_user_discord,id_pokemon):
    user_id = await get_user_id(id_user_discord)
    sql = f"INSERT INTO user_pokemon(id_user, id_pokemon) VALUES ({user_id[0]}, {id_pokemon[0]});"

    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        await set_active_pokemon('NULL')
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

async def get_active_pokemon():
    """ query data from the vendors table """
    conn = None
    user = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(f"SELECT var_value FROM sys_vars WHERE var_name = 'ACTIVE_POKEMON'")
        pokemon_id = cur.fetchone()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return pokemon_id

async def get_user_captures(user_discord_id):
    """ query data from the vendors table """
    conn = None
    count = None
    user_id = await get_user_id(user_discord_id)
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(f" SELECT COUNT(id_pokemon) FROM user_pokemon WHERE id_user = {user_id[0]}")
        count = cur.fetchone()[0]
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return count

async def get_all_user_pokemons(user_discord_id):
    conn = None
    pokemon_ids = None
    user_id = await get_user_id(user_discord_id)
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(f" SELECT id_pokemon FROM user_pokemon WHERE id_user = {user_id[0]}")
        pokemon_ids = cur.fetchall()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return pokemon_ids

async def test():
    session = Session()

    # 3 - extract all movies
    users = session.query(User).all()

    # 4 - print movies' details
    print('\n### All movies:')
    for user in users:
        print(f'{user.user_discord_id}')
    print('')