import discord
from discord import slash_command
from discord.ext import commands
import discord.ui

from Bot import GUILD_ID, Readme
from Bot.AddModules import DropdownView

class Initaillization(discord.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot: commands.Bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Checks for response form bot"""
        print(f"\nguild joined: {guild.name}")
        teacher = await self.createTeacherRole(guild)
        modChannel = await self.addChannelsToTeacherCategory(teacher, guild)

        await modChannel.send("How many modules would you like?", view=DropdownView())

    @commands.command()
    async def new_modules(self, ctx: commands.context.Context):
        """Checks for response form bot"""
        if ctx.author == ctx.guild.owner or ctx.author.guild_permissions.administrator:
            teacher = await self.createTeacherRole(ctx.guild)
            await self.addChannelsToTeacherCategory(teacher, ctx.guild)

            await ctx.send("How many modules would you like?", view=DropdownView())            
        else:
            ctx.send("You do not have permission to use this command")

    @slash_command(guild_ids=GUILD_ID, name="add_modules", description="Add's categories of modules by choice to the server")
    async def add_modules(self, ctx: commands.context.Context):
        """Checks for response form bot"""
        if ctx.author == ctx.guild.owner or ctx.author.guild_permissions.administrator:
            teacher = await self.createTeacherRole(ctx.guild)
            await self.addChannelsToTeacherCategory(teacher, ctx.guild)

            await ctx.send("How many modules would you like?", view=DropdownView())            
        else:
            ctx.send("You do not have permission to use this command")



    async def addChannelsToTeacherCategory(self, teacher: discord.Role, guild: discord.Guild) ->discord.TextChannel:
        categoryNames = [category.name for category in guild.categories]
        if "Teacher-Moderator" not in categoryNames:
            category = await guild.create_category("Teacher-Moderator")
            return await self.createModChannels(teacher, category, guild)
        else:
            for category in guild.categories:
                channelNames = [channel.name for channel in category.channels]
                if "moderate-classroom" not in channelNames and category.name == "Teacher-Moderator":
                    return await self.createModChannels(teacher, category, guild)
                else:
                    print("Already have channels in teacher moderator")
                    for channel in category.channels:
                        if channel.name == "moderate-classroom":
                            return channel


    async def createTeacherRole(self, guild: discord.Guild) -> discord.Role:
        if "Teacher-Moderator" not in guild.roles:
            return await self.createModeratorRole(guild.owner, guild=guild)
        else:
            for role in guild.roles:
                if role.name == "Teacher-Moderator":
                    roleID = role.id
            return await guild._fetch_role(roleID)


    def getTeacherChannelID(self, guild: discord.Guild) -> int:
        for category in guild.categories:
            for channel in category.channels:
                if channel.name.startswith("moderate"):
                    return channel.id
    
    async def createModChannels(self, teacher: discord.Role, category: discord.CategoryChannel, guild) -> discord.TextChannel:
        # permssion overwrites to make the channels being created
        # private to the person creating them
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            teacher: discord.PermissionOverwrite(read_messages=True)
        }

        # create the teacher / moderator channel.  This channel will be used to
        # access the bot
        
        # create the bot info channel.  This channel will have information for
        # the bot

        botInfoChannel = await category.create_text_channel("Bot-Info", overwrites=overwrites)
        await category.create_text_channel("Moderator-Text-Channel", overwrites=overwrites)
        await botInfoChannel.send(Readme.Readme.Readme())
        return await category.create_text_channel("moderate-classroom", overwrites=overwrites)


    async def createModeratorRole(self,member: discord.Member, guild: discord.Guild) -> discord.Role:
        for role in guild.roles:
            if role.name == "Teacher-Moderator":
                print("Already have a moderator")
                return role

        teacherOverwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages= True),
            guild.me: discord.PermissionOverwrite(kick_members=True),
            guild.me: discord.PermissionOverwrite(ban_members=True),
            guild.me: discord.PermissionOverwrite(priority_speaker=True)
        }

        role = await guild.create_role(name="Teacher-Moderator",color=discord.Colour.orange())
        await member.add_roles(role)
        return role
    


def setup(bot):
    bot.add_cog(Initaillization(bot))