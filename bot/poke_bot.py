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
bot = commands.Bot(command_prefix='$')

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
        await message.channel.send(f'{message.author.name} You captured {str(captured[0])} of 898')

client.run(token)
