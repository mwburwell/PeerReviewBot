from dis import disco
import discord 
from discord.ext import commands
import discord.ui

from Bot import Readme


class Initaillization(discord.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot: commands.Bot = bot

    @commands.command()
    async def on_guild_join(self, guild):
        view = DropdownView(guild)
        await guild.text_channels[0].send("How many Modules do you want?", view = view)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        await guild.create_category("Teachers_Channel", overwrites=overwrites, position=0)
        for c in (guild.categories):
            if (c.name == "Teachers_Channel"):
                Cat = c
        await guild.create_text_channel("Moderate-Classroom", overwrites=overwrites, category=Cat)
        await guild.create_text_channel("Bot-Info", overwrites=overwrites, category=Cat)
        await Cat.text_channels[1].send(Readme.Readme.Readme())

    @commands.command()
    async def pong(self, ctx):
        """Checks for response form bot"""
        guild = ctx.guild
        view = DropdownView(guild)
        await guild.text_channels[0].send("How many Modules do you want?", view = view)
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }
        await guild.create_category("Teachers_Channel", overwrites=overwrites, position=0)
        for c in (guild.categories):
            if (c.name == "Teachers_Channel"):
                Cat = c
        await guild.create_text_channel("Moderate-Classroom", overwrites=overwrites, category=Cat)
        await guild.create_text_channel("Bot-Info", overwrites=overwrites, category=Cat)
        await Cat.text_channels[1].send(Readme.Readme.Readme())
    

    

class Dropdown(discord.ui.Select):
    def __init__(self, guild):
        self.guild = guild
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

    async def callback(self, interaction: discord.MessageInteraction):
            if self.flag:
                self.flag = False
                for i in range(1, int(self.values[0]) + 1):
                    await self.guild.create_category(f"Module-{i}", position=i)
                    for c in (self.guild.categories):
                        if (c.name == f"Module-{i}"):
                            Cat = c
                    await self.guild.create_text_channel("Best-Of", category=Cat)
                await interaction.response.send_message(f"There are {self.values[0]} Modules.")
            else:
                await interaction.response.send_message("Implementation already used.")

class DropdownView(discord.ui.View):
    def __init__(self, guild):
        self.guild = guild
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.guild))      



def setup(bot):
    bot.add_cog(Initaillization(bot))