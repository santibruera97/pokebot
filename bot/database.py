import psycopg2
from user import User
from pokemon import Pokemon
from sys_vars import SystemVars
from base import Session, engine, Base
import os

DATABASE_URL = os.environ['DATABASE_URL']


async def register_user(id_user_discord):
    """ insert a new user into the users table """
    user = None
    try:
        Base.metadata.create_all(engine)

        session = Session()

        user = User(id_user_discord,25,50,1)

        session.add(user)

        session.commit()

        session.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        return True


async def set_active_pokemon(pokemon_id,guild_id):
    try:
        Base.metadata.create_all(engine)

        # 3 - create a new session
        session = Session()
        active_pokemon = await get_active_pokemon(guild_id)
        if active_pokemon is None:
            active_pokemon = SystemVars('ACTIVE_POKEMON', str(pokemon_id), str(guild_id))

        else:
            active_pokemon.var_value = str(pokemon_id)

        session.merge(active_pokemon)

        session.commit()

        session.close()


    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return False
    finally:
        return True


async def get_active_pokemon(guild_id):
    pokemon_id = None
    try:
        session = Session()
        pokemon_id = session.query(SystemVars).filter(SystemVars.guild_id == str(guild_id)).one()
        return pokemon_id

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return pokemon_id

async def get_user_captures(user_discord_id):
    count = None
    user = await get_user(user_discord_id)
    try:
        session = Session()
        count = 0
        count = session.query(Pokemon).distinct(Pokemon.name).filter(Pokemon.user_id == user.user_id).count()



    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        return count


async def get_all_users():
    session = Session()
    users = session.query(User).all()
    return users

async def insert_pokemon(pokemon):
    Base.metadata.create_all(engine)

    # 3 - create a new session
    session = Session()

    session.add(pokemon)

    session.commit()

    session.close()

async def get_user(user_discord_id):
        session = Session()
        user = session.query(User).filter(User.user_discord_id == str(user_discord_id)).one()
        return user