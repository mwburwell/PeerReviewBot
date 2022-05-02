from discord import Intents
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

prefix = commands.when_mentioned_or("><")
token = os.environ['TOKEN']

intents = Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix= prefix, intents= intents)

@bot.event
async def on_ready():
	print(f"{bot.user} has logged in!")


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