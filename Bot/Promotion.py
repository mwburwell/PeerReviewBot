from cProfile import label
import discord
from discord.ui import Button, View, Select

class ClassMenu():
	def __init__(self):
		self.selector = ClassSelect()
		self.promoteButton = Promote("Promote", row= 2)
		self.demoteButton = Demote("Demote", row=2)
		self.helpButton = HelpButton(row=2)

		self.view = View()
		self.view.add_item(self.selector)
		self.view.add_item(self.promoteButton)
		self.view.add_item(self.demoteButton)
		self.view.add_item(self.helpButton)
	

class ClassSelect(Select):
	def __init__(self, *, min_values: int = 1, max_values: int = 1, row: int = 1) -> None:
		super().__init__( placeholder = "Choose a class", row=row)
		self.options.append(discord.SelectOption(label="class 1a"))
		self.options.append(discord.SelectOption(label="class 2a"))

	async def callback(self, interaction: discord.Interaction):
		await interaction.response.send_message(self.values)
		# await interaction.
		# return await super().callback(interaction)

class Promote(Button):
	def __init__(self, label, row: int = 1):
		super().__init__(style=discord.ButtonStyle.green, label=label, row=row)

	async def callback(self, interaction: discord.Interaction):
		await interaction.response.edit_message(content="Promoting class")
		await interaction.followup.send(content="Class has been Promoted")
		# return await super().callback(interaction)


class Demote(Button):
	def __init__(self, label, row: int = 1):
		super().__init__(style=discord.ButtonStyle.danger, label=label, row=row)

	async def callback(self, interaction: discord.Interaction):
		await interaction.response.edit_message(content="Demoting class")
		await interaction.followup.send(content="Class has been demoted")
		# return await super().callback(interaction)

class HelpButton(Button):
	def __init__(self, label: str = "Help", url: str="https://github.com/mwburwell/PeerReviewBot/blob/main/README.md", row: int = 1):
		super().__init__(url= url, label=label, row=row)

	# async def callback(self, interaction: discord.Interaction):
	# 	await interaction.
	# 	return await super().callback(interaction)
