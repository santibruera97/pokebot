TOKEN = ''

import discord
import pokebase as pb
import random
import database
import poke_maths
from discord.ext import commands


import os

token = os.getenv("DISCORD_BOT_TOKEN")
client = discord.Client()
bot = commands.Bot(command_prefix="$")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@bot.command(name="random")
async def get_random_pokemon(ctx):
    poke_id = random.randint(1, 898)
    pokemon = pb.pokemon(poke_id)
    await database.set_active_pokemon(poke_id)

    shiny = random.randint(1, 2048)
    if shiny == 1024:
        poke_pic = pokemon.sprites.front_shiny
    else:
        poke_pic = pokemon.sprites.front_default
    await ctx.channel.send(poke_pic)
    await ctx.channel.send(pokemon.name.capitalize())

@bot.command(name="register")
async def register_user(ctx):
    user = await database.get_user_discord_id(ctx.author.id)
    if user is None:
        await database.register_user(ctx.author.id)
        await ctx.channel.send('Registration Completed! Welcome to the pokemon world')
    else:
        await ctx.channel.send("You\'re already registered")

@bot.command(name="pokeball")
async def throw_pokeball(ctx):
    try:
        pokemon_id = await (database.get_active_pokemon())
        if pokemon_id is None:
            await ctx.channel.send('No pokemon to capture')
        pokemon = pb.pokemon(int(pokemon_id[0]))
        result = poke_maths.catch(4)
        if result == 1:
            await database.insert_pokemon_captured(ctx.author.id, pokemon_id)
            await ctx.channel.send(f'{ctx.author.name} You captured a {pokemon.name.capitalize()}')
        else:
            await ctx.channel.send(f'Sorry {ctx.author.name}, {pokemon.name.capitalize()} dodge your pokeball')

    except Exception as error:
        print(error)

@bot.command(name="pokedex")
async def see_pokedex(ctx):
    captured = await database.get_user_captures(ctx.author.id)
    print(captured)
    await ctx.channel.send(f'{ctx.author.name} You captured {captured[0]} of 898')

client.run(token)
