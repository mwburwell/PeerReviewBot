from discord.ext import commands

class Dev(commands.Cog):
	def __init__(self, bot) -> None:
		super().__init__()
		self.bot: commands.Bot = bot

	@commands.group()
	async def cog(self, ctx):
		pass

	@cog.command()
	async def load(self, ctx: commands.Context, extension: str):
		if self.bot.extensions.get(extension):
			self.bot.reload_extension(extension)
		else:
			self.bot.load_extension(extension)
		await ctx.send("done")

	@cog.command()
	async def unload(self, ctx: commands.Context, extension: str):
		self.bot.unload_extension(extension)
		await ctx.send("done")

def setup(bot):
	bot.add_cog(Dev(bot))