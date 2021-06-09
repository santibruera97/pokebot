TOKEN = ''

import discord
import pokebase as pb
import random
import time
from pokebase import cache
cache.API_CACHE
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
            pokePic = pokemon.sprite.front_shiny
        else: 
            pokePic = pokemon.sprite.front_default
        await message.channel.send(pokePic)
        await message.channel.send(pokemon.name.capitalize()) 


    # if message.author.name == "PablitoBot" and message.content.startswith('Llamando al delivery...'):
    #     await message.channel.send('Hola?')


    # if message.author.name == "PablitoBot" and message.content.startswith('Si, que tal? Para hacerte un pedido'):
    #     time.sleep(3)
    #     await message.channel.send('Decime')

    # if message.author.name == "PablitoBot" and message.content.startswith('Quiero 4 empanadas de carne, una de verdura y queso, una de choclo, una de carne, otra de choclo'):
    #     time.sleep(3)
    #     await message.channel.send('No. Para para para, no puedo anotar así, ordena cuantas de carne queres, cuantas de choclo y así, no es tan dificil')


    # if message.author.name == "PablitoBot" and message.content.startswith('Si, tenes razon, disculpame. A ver, listo, anotas?'):
    #     time.sleep(3)
    #     await message.channel.send('Dale...')

    # if message.author.name == "PablitoBot" and message.content.startswith('Quiero 7 de carne, dos de verdura y queso, tres de choclo, una de atun'):
    #     time.sleep(3)
    #     await message.channel.send('No, de atun no nos quedan más')


    # if message.author.name == "PablitoBot" and message.content.startswith('Ah, entonces una mas de carne. Ahí no te enojas no? Para reemplazar la de atun'):
    #     time.sleep(3)
    #     await message.channel.send('Nonono, esta bien')


    # if message.author.name == "PablitoBot" and message.content.startswith('Bueno sigo, otra de carne y otra mas de carne'):
    #     time.sleep(3)
    #     await message.channel.send('Para, me estas jodiendo?')

    # if message.author.name == "PablitoBot" and message.content.startswith('Bueno, al no estar la de atun se me cambian los planes, ahora tengo que inventar sobre la marcha negro viste'):
    #     time.sleep(3)
    #     await message.channel.send('Sabes que? Dictamelo como quieras porque si no vamos a estar 10 horas, dale. Decimelo, porque, como se te cante las bolas que yo anoto')


    # if message.author.name == "PablitoBot" and message.content.startswith('Bueno, dos de carne, cuatro de choclo, cinco de carne, una de choclo, nueve de carne, una de carne, siete de choclo, cinco de carne, cinco de choclo, cinco de choclo, cinco de choclo, una de choclo, dos de choclo, cinco de choclo, cinco de choclo'):
    #     time.sleep(3)
    #     await message.channel.send('Ei ei ei ei. Que te pasa? Te volviste loco? Me estás cargando?')



client.run(token)