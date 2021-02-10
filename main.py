import os
import discord
import requests
import json
from dotenv import load_dotenv
from keep_alive import keep_alive
from discord.ext import commands
from KSM_functions import *

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
async def character(ctx, name, server, region = "us"):
    name = name.lower()
    server = server.lower()
    server = server.replace(" ", "-").replace("'", "")
    region = region.lower()
    msg = f'Main character set to {name.title()}-{region.upper()}-{server.title()}'
    await ctx.send(msg)

keep_alive()
client.run(TOKEN)