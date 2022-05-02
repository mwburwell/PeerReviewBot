from cgitb import text
import discord
from discord import Interaction
from discord.ui import Button, View, Select

class PromoteClassView(View):
	def __init__(self, classroomRoles: list[discord.Role] =[], members: list[discord.Member] = [], timeout: float = 180):
		super().__init__(timeout=timeout)
		self.members = members
		self.roles = classroomRoles
		self.add_item(ClassSelect(self.buildRoleList(roles=classroomRoles)))
		self.choices = []
		self.classList: str = ""


	def buildRoleList(self, roles: list[discord.Role]) -> list[str]:
		roleNames: list[str] = []
		for role in roles:
			roleNames.append(role.name)
		
		return roleNames

	def buildClassList(self, selections: list[str]) -> str:
		userSelections: str = ""
		for selection in selections:
			userSelections += "-> " + selection + "\n"

		return userSelections


	def getUserChoices(self, interaction: discord.Interaction) -> list[str]:
		if interaction.data['component_type'] != 3:
			raise AttributeError("This interation is not a selection component")

		choices: list[str] = []
		for value in interaction.data['values']:
			choices.append(value)

		return choices

	def refineRoles(self, roles: list[discord.Role], choices: list[str]):
		if len(choices) < 1 or len(choices) > len(roles):
			return
		
		for role in roles:
			if role.name in choices:
				continue
			else:
				roles.remove(role)


	async def interaction_check(self, interaction: Interaction) -> bool:
		print("\nPromote Class View Interaction Check: ")
		# if the interaction is of selection component type then we
		# will add buttons and display what the user selected.
		# we can also pass the selected ROLES into the buttons to
		# do what we need to them.
		if interaction.data['component_type'] == 3:

			self.choices = self.getUserChoices(interaction= interaction)
			self.refineRoles(self.roles, self.choices)
			
			self.clear_items()
			self.add_item(Promote(self.roles))
			self.add_item(Demote(self.roles))
			self.add_item(HelpButton())
			await interaction.response.edit_message(
				embed= discord.Embed(
					color= discord.Colour.red(), 
					title= self.buildClassList(self.choices),
					description= "Choose:\npromote - to move a class forward\ndemote - to move a class backward\ncancel - to cancel promotion\nhelp - to get instructions"
					),
				view=self)

		# after the selection is gotten rid of we have buttons left over,
		# the buttons will handle the ROLE changing
		# this is only after the buttons are selected we will get rid of the
		# menu
		elif interaction.data['component_type'] < 3:
			self.clear_items()
			
			await interaction.response.edit_message(
				embed= discord.Embed(
					color = discord.Color.blue(),
					title= self.buildClassList(self.choices),
					description= "Classes have been promoted" if len(self.classList) > 1 else "Has been promoted"
				), 
				view=self)
			self.stop()

		return await super().interaction_check(interaction)

		# TO DO 
		# 1. need to set permission for view this module, probably
		# in the caller 
		# 
		# space_holder
	

class ClassSelect(Select):
	def __init__(self, roleNames: list[str], *, min_values: int = 1, row: int = 1):
		super().__init__(placeholder = "Choose a class", row=row)

		self.roles = roleNames
		self.options = [discord.SelectOption(label=role) for role in roleNames]
		self.max_values = len(self.options)


		# TO DO
		# 1. allow for the select statement to take in the current Guilds 
		# available class rooms.  These class Rooms will need to be specific
		# to the guild.  Do not include any other roles in the guild. 
		# 
		# 2. increase the maximum select to the length of the class roles being
		# passed in 
		# 
		# space_holder

	# DO NOT REALLY NEED THIS CALLBACK. IT WILL BE HANDLED IN THE VIEW
	#
	# async def callback(self, interaction: discord.Interaction):
	# 	# print(self.values)
	# 	print(interaction.data.keys())
	# 	for value in interaction.data['values']:
	# 		print(value, type(value))


		# for val in self.values:
		# 	print(type(val))
		# return self.values

		#await interaction.response.send_message(self.values)

		# TO DO 
		# 1. When selecting a class need to pass the information to the buttons 
		# to promote or demote their permissions 
		# 
		# space_holder
		# 
		# await interaction.
		# return await super().callback(interaction)

class Promote(Button):
	def __init__(self, roles: list[discord.Role], label: str = "Promote", row: int = 2):
		super().__init__(style=discord.ButtonStyle.green, label=label, row=row)

		self.roles = roles
		# TO DO
		# 1. need to take in a list of roles to change permissions
		# 
		# space_holder

	async def callback(self, interaction: discord.Interaction):
		print("\nPromote Button Callback:")
		for role in self.roles:
			print(f"\nRole: {role.name}")
			categories = role.guild.categories
			# previousCategory: categories
			
			# search through each category and see if the current
			# role can access channels in that category if it can
			# move on to the next one.
			#
			# if we find a category that they can not read then this
			# is the next level for that role and we create private
			# channels for them.
			for cat in categories:

				overwrites = {
					interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
					interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
					role: discord.PermissionOverwrite(read_messages=True)
				}
				# the overwrites needed to create a secret channel
				if cat.name.startswith("Module"):
					# cat.create_text_channel()
					print(cat)
					perm: discord.permissions.Permissions = cat.permissions_for(role)
					print(perm.view_channel)
					for p in perm:
						print(p)
					if not perm.view_channel:
						textChannel:str = "chat-" + role.name
						prChannel: str = "pr-" + role.name


						print(f"Perm type: {type(perm)}")
						print(f"checking permission on category: {role.name}")

						if not self.hasChannel(cat, textChannel):
							await cat.create_text_channel(name=textChannel, overwrites=overwrites)
							
						if not self.hasChannel(cat, prChannel):
							await cat.create_text_channel(name=prChannel, overwrites=overwrites)

						await cat.edit(overwrites={role: discord.PermissionOverwrite(view_channel=True)})


						print(f"Create channels in {cat.name}")

						# we will break because we do not want all of the categories
						# that they have false but the latest one
						break

				if cat == categories[len(categories) - 1]:
					print("NEED TO IMPLEMENT LEGACY PROMOTION")
				# cat = previousCategory
		await interaction.followup.send(content="Class has been Promoted")
		return await super().callback(interaction)

	def hasChannel(self, category: discord.CategoryChannel, channelName: str) -> bool:
		for channel in category.channels:
			if channel.name == channelName:
				return True

		return False

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
	def __init__(self, roles: list[discord.Role], label: str = "Demote", row: int = 2):
		super().__init__(style=discord.ButtonStyle.green, label=label, row=row)

		self.roles = roles

		# TO DO
		# 1. need to take in a list of roles to change permissions
		# 
		# space_holder


	async def callback(self, interaction: discord.Interaction):
		print("\nDemote Button Callback:")
		for role in self.roles:
			print(f"\nRole: {role.name}")
			categories = role.guild.categories
			for cat in categories:
				overwrites = {
					interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
					role: discord.PermissionOverwrite(read_messages=False)
				}
				if cat.name.startswith("Module"):
					# cat.create_text_channel()
					print(cat)
					perm: discord.permissions.Permissions = cat.permissions_for(role)
					print(perm.view_channel)
					if not perm.view_channel:
						print(f"Previous Category: {previousCategory}")
						for channel in previousCategory.channels:
							print(f"removing viewing for {role.name} in {channel.name}")
							await channel.edit(overwrites=overwrites)
						await cat.edit(overwrites= overwrites)
						break
					previousCategory = cat

		await interaction.followup.send(content="Class has been Demoted")

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

class Cancel(Button):
	def __init__(self, label: str = "Cancel", row: int = 2):
		super().__init__(style=discord.ButtonStyle.grey, label=label, row=row)


class HelpButton(Button):
	# This is a help button that will direct the user to the documentation for
	# this specific section of the bot
	# 
	# place_holder
	def __init__(self, 
		label: str = "Help", 
		url: str="https://github.com/mwburwell/PeerReviewBot/blob/main/README.md", 
		row: int = 2):
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