from pydoc import describe
import discord
from discord.commands import slash_command
from discord.ext import commands
from Bot.PromotionView import PromoteClassView
# This is the Class Promotion view with a Select statement
# and three buttons.

GUILD_ID = [958468593358626816, 745428142428258426]

class Promote(commands.Cog):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot: commands.Bot = bot

	@commands.command()
	async def promote(self, ctx: commands.Context):
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

	@slash_command(guild_ids=GUILD_ID, name= "promotion")
	async def promotion(self, ctx: discord.commands.context.ApplicationContext):
		print("\nPromote Slash Command: ")
		classes: list[discord.Role] = []

		for role in ctx.guild.roles:
			if role.name.endswith('classroom'):
				classes.append(role)

		if ctx.channel.category.name.startswith("Teacher"):#== "TEACHERS_CHANNEL":
			promoteMenu = PromoteClassView(classroomRoles= classes)
			await ctx.respond("Promote class or Demote class", view = promoteMenu)
		else:
			await ctx.respond("You do not have permission to use this command")

	@slash_command(guild_ids=GUILD_ID, name="ping")
	async def ping(self, ctx: discord.commands.context.ApplicationContext):
		await ctx.respond("pong!")

	# @slash_command(guild_ids= GUILD_ID, name="addclassroom", description="add a classroom to the server")
	# async def addclassroom(self, ctx: discord.commands.context.ApplicationContext):
	# 	await ctx.respond("add class")

	# @slash_command(guild_ids=GUILD_ID, name="addteacher")
	# async def addteacher(self, ctx: discord.commands.context.ApplicationContext):
	# 	await ctx.respond("add teacher")

	# @slash_command(guild_ids=GUILD_ID, name="addstudent")
	# async def addstudent(self, ctx: discord.commands.context.ApplicationContext):
	# 	await ctx.respond("add student")





def setup(bot):
	bot.add_cog(Promote(bot))