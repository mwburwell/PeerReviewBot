from dis import disco
from operator import mod
import discord

class Dropdown(discord.ui.Select):
	def __init__(self):
		self.flag = True
        
		# Set the options that will be presented inside the dropdown
		options = [
            discord.SelectOption(
                label="1", description="There is 1 Module"
            ),
            discord.SelectOption(
                label="4", description="There are 4 Modules"
            ),
            discord.SelectOption(
                label="8", description="There are 8 Modules"
            ),
            discord.SelectOption(
                label="16", description="There are 16 Modules"
            ),
        ]
		super().__init__(
            placeholder="How many modules are in the Class...",
            min_values=1,
            max_values=1,
            options=options,
        )

	async def callback(self, interaction: discord.interactions.Interaction):
		if not interaction.user.guild_permissions.administrator:
			interaction.response.send_message("You do not have permission.")
			return

		categories = interaction.guild.categories
		newModules: list[str] = []
		oldModules: list[str] = []


		# collect the names of all the old modules in the server already
		for category in categories:
			if category.name.startswith("Module"):
				oldModules.append(category.name)

		# gather the new modules by iterating over the amount of modules
		# the user would like to create
		for i in range(1, int(self.values[0]) + 1):
			newModules.append("Module-" + str(i))
		
		# remove the old modules from the new module list and create new
		# modules
		for module in newModules:
			if module not in oldModules:
				category = await interaction.guild.create_category(name=module)
		
		for role in interaction.guild.roles:
			if role.name == "Teacher-Moderator":
				teacher = role
		
		overwrites = {
			interaction.guild.default_role: discord.PermissionOverwrite(read_messages= False),
			teacher: discord.PermissionOverwrite(read_messages = True)
		}

		# add best of channel to all modules that do not already have it
		for category in interaction.guild.categories:
			bestOf = "best-of-programs"
			channelList = [channel.name for channel in category.channels]
			if bestOf not in channelList and category.name.startswith("Module"):
				await category.create_text_channel(name=bestOf, overwrites=overwrites)

		await interaction.response.edit_message(content="Your Module channels are all set up")

class DropdownView(discord.ui.View):
	def __init__(self):
		super().__init__()
		# Adds the dropdown to our view object.
		self.add_item(Dropdown())      
		
	async def interaction_check(self, interaction: discord.Interaction) -> bool:
		self.clear_items()
		await interaction.response.edit_message(content="Your Modules have been set up.", view = self)
		pass