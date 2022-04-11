import discord
from discord.ui import Button, View, Select
from discord.ext import commands

from dotenv import load_dotenv
from os import getenv
load_dotenv()

from Bot import GUILD_ID, STDOUT_ID
from Bot import Greetings

from Bot.Promotion import ClassMenu, Promote, Demote, HelpButton
import random

description = '''An example bot to showcase the discord.ext.commands extension
module.
There are a number of utility commands being showcased here.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='><', intents= intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')
    for channel in bot.get_all_channels():
       print(channel.name, channel.category)

@bot.command()
async def promote(ctx):
    button1 = Promote("Promote")
    button2 = Demote("Demote")
 
    # TO DO
    # need to add proper documentation for teachers or moderators
    # to reference what promoting and demoting is
    button3 = HelpButton(label="Help", url="https://github.com/mwburwell/PeerReviewBot/blob/main/README.md")
    # END TO DO

    view = View()
    view.add_item(button1)
    view.add_item(button2)
    view.add_item(button3)
    await ctx.send("Click to promote or demote a Class", view=view)

@bot.command()
async def selection(ctx):
    menu = ClassMenu()

    await ctx.send("Choose the class", view= menu.view)
 
@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

# print(discord.__version__)
# # This example requires the 'members' and 'message_content' privileged intents to function.



# @bot.command()
# async def add(ctx, left: int, right: int):
# 	"""Adds two numbers together."""
# 	await ctx.send(left + right)
# 	await ctx.send(ctx.channel)
# 	# await ctx.fetch_message(bot.user.id)



# @bot.command(description='For when you wanna settle the score some other way')
# async def choose(ctx, *choices: str):
#     """Chooses between multiple choices."""
#     await ctx.send(random.choice(choices))


# @bot.command()
# async def repeat(ctx, times: int, content='repeating...'):
#     """Repeats a message multiple times."""
#     for i in range(times):
#         await ctx.send(content)


# @bot.command()
# async def joined(ctx, member: discord.Member):
#     """Says when a member joined."""
#     await ctx.send(f'{member.name} joined in {member.joined_at}')


bot.run(getenv('TOKEN'))