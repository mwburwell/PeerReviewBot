import discord
from discord.ext import commands
from discord import Interaction, SelectOption
from discord.ui import Button, View, Select

# This is the Class Promotion view with a Select statement
# and three buttons.
class PromoteClassView(View):
	def __init__(self, options, timeout: float = 180):
		super().__init__(timeout=timeout)
		self.add_item(ClassSelect(options=options))
		self.add_item(Promote(row=2))
		self.add_item(Demote(row=2))
		self.add_item(HelpButton(row=2))

		# TO DO 
		# 1. need to set permission for view this module, probably
		# in the caller space_holder
	

class ClassSelect(Select):
	def __init__(self, *,options, min_values: int = 1, max_values: int = 1, row: int = 1) -> None:
		super().__init__( placeholder = "Choose a class", row=row)
		self.options = options

		# TO DO
		# 1. allow for the select statement to take in the current Guilds 
		# available class rooms.  These class Rooms will need to be specific
		# to the guild.  Do not include any other roles in the guild. 
		# 
		# 2. increase the maximum select to the length of the class roles being
		# passed in 
		# 
		# space_holder

	async def callback(self, interaction: discord.Interaction):
		await interaction.response.send_message(self.values)

		# TO DO 
		# 1. When selecting a class need to pass the information to the buttons 
		# to promote or demote their permissions 
		# 
		# space_holder
		# 
		# await interaction.
		# return await super().callback(interaction)

class Promote(Button):
	def __init__(self, label: str = "Promote", row: int = 1):
		super().__init__(style=discord.ButtonStyle.green, label=label, row=row)

		# TO DO
		# 1. need to take in a list of roles to change permissions
		# 
		# space_holder

	async def callback(self, interaction: discord.Interaction):
		await interaction.response.edit_message(content="Promoting class")
		await interaction.followup.send(content="Class has been Promoted")
		# return await super().callback(interaction)

		# TO DO 
		# 1. need to change permissions to move to the next channel
		# in the curriculum for all classes in the list passed from the
		# select
		# 
		# 2. need to add verification to give the chance for the moderator
		# to accept or decline the changes
		# 
		# 3. need to provide a list of students currently selected
		# 
		# space_holder


class Demote(Button):
	def __init__(self, label: str = "Demote", row: int = 1):
		super().__init__(style=discord.ButtonStyle.danger, label=label, row=row)

		# TO DO
		# 1. need to take in a list of roles to change permissions
		# 
		# space_holder


	async def callback(self, interaction: discord.Interaction):
		await interaction.response.edit_message(content="Demoting class")
		await interaction.followup.send(content="Class has been demoted")
		# return await super().callback(interaction)

		# TO DO 
		# 1. need to change permissions to move to the next channel
		# in the curriculum for all classes in the list passed from the
		# select
		# 
		# 2. need to add verification to give the chance for the moderator
		# to accept or decline the changes
		# 
		# 3. need to provide a list of students currently selected
		# 
		# space_holder

class HelpButton(Button):
	def __init__(self, label: str = "Help", url: str="https://github.com/mwburwell/PeerReviewBot/blob/main/README.md", row: int = 1):
		super().__init__(url= url, label=label, row=row)

	async def callback(self, interaction: discord.Interaction):
		return await super().callback(interaction)

		# TO DO 
		# 1. need to write up documentation on how the Promote Demote
		# functionality will work
		#
		# 2. need to link this button to that newly created documentation
		# 
		# space_holder
