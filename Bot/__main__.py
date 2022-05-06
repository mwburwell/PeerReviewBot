import discord
from discord import Intents
from discord.ext import commands

import os
from dotenv import load_dotenv

from Bot import GUILD_ID
# from Bot import GUILD_ID

GUILD_ID = [958468593358626816]

load_dotenv()

prefix = commands.when_mentioned_or("!")
token = os.environ['TOKEN']

intents = Intents.default()
intents.members = True
intents.message_content = True
# intents.guilds = True

bot = commands.Bot(command_prefix= prefix, intents= intents)

@bot.event
async def on_ready():
    await bot.register_commands()
    GUILD_ID = [guild.id for guild in bot.guilds]
    print(f"{bot.user} has logged in!")



omittedFiles = ["Bot.cogs.AddClass","Bot.cogs.AddStudent","Bot.cogs.AddTeacher"]

cogfiles: list[str] = []
for filename in os.listdir("./Bot/cogs/"):
    if filename.endswith(".py"):
        cogfiles.append(f"Bot.cogs.{filename[:-3]}")

for cogfile in cogfiles:
    # print(cogfile)
    try:
        bot.load_extension(cogfile)
        print(f"loaded: {cogfile}")
    except Exception as err:
        print(err)

bot.run(token)