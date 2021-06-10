TOKEN = ''

import discord
import pokebase as pb
import random
import database


import os

token = os.getenv("DISCORD_BOT_TOKEN")


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$poke random'):
        pokeID = random.randint(1, 800)
        pokemon = pb.pokemon(pokeID)
        shiny = random.randint(1, 8192)
        if shiny == 888:
            pokePic = pokemon.sprites.front_shiny
        else:
            pokePic = pokemon.sprites.front_default
        await message.channel.send(pokePic)
        await message.channel.send(pokemon.name.capitalize())
    if message.content.startswith('$poke register'):
        user = database.get_user(message.author.id)
        print(user[0])
        if user is None:
            database.register_user(message.author.id)
            await message.channel.send('Registration Completed! Welcome to the pokemon world')


client.run(token)
