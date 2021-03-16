import os
import discord
from dotenv import load_dotenv
from keep_alive import keep_alive
from discord.ext import commands

from KSM_db import *

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.command()
async def hello(ctx):
    msg = f'Hi {ctx.author.mention}'
    await ctx.send(msg)

@client.command()    
async def ping(ctx):
    await ctx.send('Pong')

@client.command()
async def character(ctx, arg = 'help', name = None, server = None, region = "us"):
    if arg == 'update':
        if name == None or server == None:
            msg = 'Enter !character update (name) (server) to update default character'
        else:
            msg = update_character(ctx.author.mention, name, server, region)
    elif arg == 'info':
        character = get_character(ctx.author.mention)
        msg = f'https://raider.io/characters/{character[3]}/{character[2]}/{character[1]}'
    # elif arg == 'ksm':
        
    else:
        msg = 'Please add "update (name) (server)" or "info"'

    await ctx.send(msg)

@client.command() # NYI
async def guild(ctx, name = "Entropi", server = "zuljin", region = "us"):
    # if arg == 'update':
        # if name == None or server == None:
        #     msg = 'Enter !guild update (guild name) (server) to update default guild'
        # else:
        #     msg = update_guild(ctx.guild.name, name, server, region)
    # elif arg == 'info':
        # guild = get_guild(ctx.guild.name)
        # msg = f'https://raider.io/guilds/{region}/{server}/{name}'
    # else:
        # msg = 'Please add "update (guild name) (server)" or "info"'

    msg = f'https://raider.io/guilds/{region}/{server}/{name}'   
    await ctx.send(msg)

@client.command()
async def roster(ctx, arg = 'help', name = "entropi", server = "zuljin", region = "us"):
    ranks = [0, 1, 2, 3, 5, 8]

    if arg == 'update':
        update_roster(name, server, region)
        msg = f'Guild roster updated for {name.title()}\nType "!roster ksm" to update key info.'
    # elif arg == 'info':
    #     g_roster = get_db_roster(ranks) # [[id, name, rank, class], ]
    #     roster_list = ["```", "Rank", "Name", "Class", "\n"]
    #     for i in g_roster:
    #         roster_list.append(str(i[2]))
    #         roster_list.append(i[1])
    #         roster_list.append(i[3])
    #         roster_list.append("\n")
    #     roster_list.append("```")
    #     msg = ' '.join(roster_list)
    elif arg == 'ksm':
        update_roster_ksm(roster, ranks)
        msg = 'Guild roster updated with key info'
    else:
        msg = 'Please add "update (name) (server) (region)", "info", or "ksm" (to update ksm data)'

    await ctx.send(msg)

@client.command()
async def ksm(ctx, qtype = 'character', *query):
    # if arg == 'guild':
    #     table = 'character_dungeons'
    # elif arg == 'friends':
    #     table = 'friends_dungeons'
    query = " ".join([word.title() if word != "of" else word for word in query])
    table = 'character_dungeons'

    if qtype == 'character':
        needed = ksm_character(table, query)
        dungeons = '\n- '.join(needed)
        msg = f"{query} is missing the following dungeons:\n- {dungeons}"

    elif qtype == 'dungeon':
        needed = ksm_dungeon(table, query)
        characters = '\n- '.join(needed)
        msg = f"The following players are missing {query} for KSM:\n- {characters}"

    await ctx.send(msg)





# NYI
# @client.command()
# async def whitelist(ctx, arg = 'help', name = None, server = None, region = "us"):
#     if arg == 'add':
#         if name == None or server == None:
#             msg = 'Enter !character add (name) (server) to add character to the whitelist'
#         else:
#             msg = add_character(name, server, region)

#     elif arg == 'delete':
#         if name == None or server == None:
#             msg = 'Enter !character delete (name) (server) to delete character from the whitelist'
#         else:
#             msg = delete_character(name, server, region)

#     elif arg == 'info':
#         characters = get_whitelist()
#         msg = 
#     else:
#         msg = 'Please add "add (name) (server)", "delete (name) (server)" or "info"'

#     await ctx.send(msg)

keep_alive()
client.run(TOKEN)