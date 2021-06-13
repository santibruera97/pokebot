TOKEN = ''

import discord
import pokebase as pb
import random
import database
import poke_maths
import asyncio
import math
from discord.ext import commands
import DiscordUtils
import os

token = os.getenv("DISCORD_BOT_TOKEN")
client = discord.Client()
bot = commands.Bot(command_prefix='$')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@bot.command()
async def test(ctx):
    #await database.test()
    pokemons_data = pb.pokemon('')

    pokemons = pokemons_data.results

    for pokemon in pokemons:
        print(pokemon.name.capitalize())
        print('\n')


    await ctx.send('Test')

@bot.command()
async def pokedex(ctx):
    embeds = []
    paginator = DiscordUtils.Pagination.CustomEmbedPaginator(ctx)
    pokemons_data = pb.pokemon('')
    pokemon_ids = await database.get_all_user_pokemons(ctx.author.id)
    pokemons = [pokemons_data.results[m[0]].name.capitalize() for m in pokemon_ids]
    per_page = 15  # 10 members per page
    pages = math.ceil(len(pokemons) / per_page)
    cur_page = 1
    chunks = [pokemons[:per_page]]
    captured = await database.get_user_captures(ctx.author.id)
    linebreak = "\n"
    for pokemon in pokemons:
        cur_page += 1
        if cur_page != pages:
            chunk = pokemons[(cur_page - 1) * per_page:cur_page * per_page]
            chunks.append(chunk)
        else:
            chunk = pokemons[(cur_page - 1) * per_page:]
            chunks.append(chunk)
    pokelist = []
    for page in chunks:
        pokelist.append(f"{linebreak.join(page)}\n You captured {str(captured)} of 898")

    for poke_page in pokelist:
        embeds.append(discord.Embed(color=ctx.author.color).add_field(name=f"{ctx.author.name.capitalize()}'s pokedex", value=poke_page))

    paginator.add_reaction('⏮️', "first")
    paginator.add_reaction('⏪', "back")
    paginator.add_reaction('🔐', "lock")
    paginator.add_reaction('⏩', "next")
    paginator.add_reaction('⏭️', "last")
    await paginator.run(embeds)

@bot.command(name="random")
async def random_pokemon(ctx):
    poke_id = random.randint(1, 898)
    pokemon = pb.pokemon(poke_id)
    shiny = random.randint(1, 2048)
    if shiny == 1024:
        poke_pic = pokemon.sprites.front_shiny
    else:
        poke_pic = pokemon.sprites.front_default
    await ctx.channel.send(poke_pic)
    await ctx.channel.send(pokemon.name.capitalize())
    await database.set_active_pokemon(poke_id)



@bot.command()
async def register(ctx):
    user = await database.get_user_discord_id(ctx.author.id)
    if user is None:
        await database.register_user(ctx.author.id)
        await ctx.channel.send('Registration Completed! Welcome to the pokemon world')
    else:
        await ctx.channel.send("You\'re already registered")

@bot.command()
async def pokeball(ctx):
    try:
        pokemon_id = await (database.get_active_pokemon())
        if pokemon_id[0] == '':
            await ctx.channel.send('No pokemon to capture')
        else:
            pokemon = pb.pokemon(int(pokemon_id[0]))
            result = poke_maths.catch(4)
            if result == 1:
                await ctx.channel.send(f'{ctx.author.name} You captured a {pokemon.name.capitalize()}')
                await database.insert_pokemon_captured(ctx.author.id, pokemon_id)
            else:
                await ctx.channel.send(f'Sorry {ctx.author.name}, {pokemon.name.capitalize()} dodge your pokeball')
    except Exception as error:
        print(error)

bot.run(token)
