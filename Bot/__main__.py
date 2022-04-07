import os
import discord

from Bot import GUILD_ID, STDOUT_ID

with open("./secrets/token") as f:
	_token = f.read().strip()

intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
	# guild = client.get_guild(GUILD_ID)
	print('We have logged in as {0.user}'.format(client))
	# for member in guild.members:
	# 	print(member)
		
@client.event
async def on_message(message):
	if message.author == client.user:
		return
		
	if message.content.startswith('!hello'):
		await message.channel.send('Change Permissions!')
		return
	
	# if message.content.startswith('!createChannel'):
	# 	channel = await discord.guild.TextChannel()

client.run(_token)