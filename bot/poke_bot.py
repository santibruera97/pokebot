TOKEN = ''

import discord
import pokebase as pb
import random
import database
import poke_maths
from discord.ext import commands
import asyncio
import math


import os

token = os.getenv("DISCORD_BOT_TOKEN")
client = discord.Client()
bot = commands.Bot(command_prefix='%')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@bot.command()
async def test(ctx, arg):
    await ctx.send(arg)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$poke random'):
        poke_id = random.randint(1, 898)
        pokemon = pb.pokemon(poke_id)
        await database.set_active_pokemon(poke_id)

        shiny = random.randint(1, 2048)
        if shiny == 1024:
            poke_pic = pokemon.sprites.front_shiny
        else:
            poke_pic = pokemon.sprites.front_default
        await message.channel.send(poke_pic)
        await message.channel.send(pokemon.name.capitalize())
    if message.content.startswith('$poke register'):
        user = await database.get_user_discord_id(message.author.id)
        if user is None:
            await database.register_user(message.author.id)
            await message.channel.send('Registration Completed! Welcome to the pokemon world')
        else:
            await message.channel.send("You\'re already registered")
    if message.content.startswith('$pokeball'):
        try:
            pokemon_id = await (database.get_active_pokemon())
            if pokemon_id is None:
                await message.channel.send('No pokemon to capture')
            pokemon = pb.pokemon(int(pokemon_id[0]))
            result = poke_maths.catch(4)
            if result == 1:
                await database.insert_pokemon_captured(message.author.id,pokemon_id)
                await message.channel.send(f'{message.author.name} You captured a {pokemon.name.capitalize()}')
            else:
                await message.channel.send(f'Sorry {message.author.name}, {pokemon.name.capitalize()} dodge your pokeball')

        except Exception as error:
            print(error)

    if message.content.startswith('$pokedex'):
        captured = await database.get_user_captures(message.author.id)
        await message.channel.send(f'{message.author.name} You captured {str(captured)} of 898')
    if message.content.startswith('$list'):
        pokemon_ids = await database.get_all_user_pokemons()
        pokemons = [pb.pokemon(m).name for m in pokemon_ids]
        per_page = 10  # 10 members per page
        pages = math.ceil(len(pokemons) / per_page)
        cur_page = 1
        chunk = pokemons[:per_page]
        linebreak = "\n"
        message = await message.send(f"Page {cur_page}/{pages}:\n{linebreak.join(chunk)}")
        await message.add_reaction("◀️")
        await message.add_reaction("▶️")
        active = True

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) in ["◀️", "▶️"]
            # or you can use unicodes, respectively: "\u25c0" or "\u25b6"

        while active:
            try:
                reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    if cur_page != pages:
                        chunk = pokemons[(cur_page - 1) * per_page:cur_page * per_page]
                    else:
                        chunk = pokemons[(cur_page - 1) * per_page:]
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{linebreak.join(chunk)}")
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    chunk = pokemons[(cur_page - 1) * per_page:cur_page * per_page]
                    await message.edit(content=f"Page {cur_page}/{pages}:\n{linebreak.join(chunk)}")
                    await message.remove_reaction(reaction, user)
            except asyncio.TimeoutError:
                await message.delete()
                active = False

client.run(token)
