import psycopg2
from config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    command = """ CREATE TABLE users (
                user_id SERIAL PRIMARY KEY,
                user_discord_id VARCHAR(255) NOT NULL,
                superballs INTEGER NOT NULL,
                ultraballs INTEGER NOT NULL,
                masterballs INTEGER NOT NULL
                )
        """

    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
        print("Success")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_user(discord_id):
    """ query data from the vendors table """
    conn = None
    user = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
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

def register_user(discord_id):
    """ insert a new user into the users table """
    sql = """INSERT INTO users(user_discord_id,superballs,ultraballs,masterballs)
                 VALUES(%s,50,25,1) RETURNING user_id;"""

    conn = None
    user_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
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
