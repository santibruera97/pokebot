import psycopg2
import os

async def connect_db():
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    return conn

async def get_user(discord_id):
    """ query data from the vendors table """
    conn = None
    user = None
    try:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute(f"SELECT user_discord_id FROM users WHERE user_discord_id = '{discord_id}'")
        user = cur.fetchone()
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return user

async def register_user(discord_id):
    """ insert a new user into the users table """
    sql = """INSERT INTO users(user_discord_id,superballs,ultraballs,masterballs)
                 VALUES(%s,50,25,1) RETURNING user_id;"""

    conn = None
    user_id = None
    try:
        conn = connect_db
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (discord_id,))
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
