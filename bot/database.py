import psycopg2
import os
import datetime;

DATABASE_URL = os.environ['DATABASE_URL']


async def get_user_discord_id(id_user_discord):
    """ query data from the vendors table """
    conn = None
    user = None
    try:
        DATABASE_URL = os.environ['DATABASE_URL']
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
        DATABASE_URL = os.environ['DATABASE_URL']
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
    sql = """INSERT INTO users(user_discord_id,superballs,ultraballs,masterballs)
                 VALUES(%s,50,25,1) RETURNING user_id;"""

    conn = None
    user_id = None
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (id_user_discord))
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
    ct = datetime.datetime.now()
    sql = f"UPDATE sys_vars SET var_value= {str(pokemon_id)}, updated_at={ct} WHERE var_name = 'ACTIVE_POKEMON';"

    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (str(pokemon_id)))
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
    user_id = get_user_id(id_user_discord)
    sql = f"INSERT INTO user_pokemon(id_user, id_pokemon) VALUES ({user_id}, {id_pokemon});"

    conn = None

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        await set_active_pokemon('')
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
        DATABASE_URL = os.environ['DATABASE_URL']
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(f"SELECT var_value FROM users WHERE var_name = 'ACTIVE_POKEMON'")
        pokemon_id = cur.fetchone()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return pokemon_id