TOKEN = ''

import discord
import pokebase as pb
import random
import database


import os

#token = os.getenv("DISCORD_BOT_TOKEN")
token = 'ODUxOTU0NDQ4NzcwNTMxMzg4.YL_yaQ.KtQy9s7Y5uLPlpWPXR_O-GrKNMw'


client = discord.Client()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('$poke random'):
        poke_id = random.randint(1, 898)
        pokemon = pb.pokemon(poke_id)
        shiny = random.randint(1, 2048)
        if shiny == 1024:
            poke_pic = pokemon.sprites.front_shiny
        else:
            poke_pic = pokemon.sprites.front_default
        await message.channel.send(poke_pic)
        await message.channel.send(pokemon.name.capitalize())
    if message.content.startswith('$poke register'):
        user = database.get_user(message.author.id)
        if user is None:
            database.register_user(message.author.id)
            await message.channel.send('Registration Completed! Welcome to the pokemon world')
        else:
            await message.channel.send("You\'re already registered")



client.run(token)
