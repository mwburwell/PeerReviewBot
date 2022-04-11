import discord
from discord.ui import Button, View

class Promote(Button):
	def __init__(self, label):
		super().__init__(style=discord.ButtonStyle.green, label=label)

	async def callback(self, interaction: discord.Interaction):
		return await super().callback(interaction)


class Demote(Button):
	def __init__(self, label):
		super().__init__(style=discord.ButtonStyle.danger, label=label)

	async def callback(self, interaction: discord.Interaction):
		return await super().callback(interaction)

class HelpButton(Button):
	def __init__(self, label, url):
		super().__init__(url= url, label=label)

	# async def callback(self, interaction: discord.Interaction):
	# 	await interaction.
	# 	return await super().callback(interaction)
