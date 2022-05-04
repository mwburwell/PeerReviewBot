from pydoc import describe
import discord
from discord.commands import slash_command
from discord.ext import commands
from Bot.PromotionView import PromoteClassView
# This is the Class Promotion view with a Select statement
# and three buttons.

from Bot import GUILD_ID

class Promote(commands.Cog):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot: commands.Bot = bot

	@commands.command()
	async def alter_class(self, ctx: commands.Context):
		if ctx.author.guild_permissions.administrator:
			print("\nPromotion Command: ")
			classes: list[discord.Role] = []

			# get all of the rolles in the guild that end with classroom
			for role in ctx.guild.roles:
				if role.name.startswith('class'):
					classes.append(role)

			promoteMenu = PromoteClassView(classroomRoles= classes)
			await ctx.send("Promote class or Demote class", view = promoteMenu)

		else:
			await ctx.send("You do not have permission to use this command")



def setup(bot):
	bot.add_cog(Promote(bot))