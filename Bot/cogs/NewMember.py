# Author Michael Peck

import discord
from discord.commands import slash_command
from discord.ext import commands
import discord.ui

#from setuptools import Command

# from Bot import GUILD_ID, Readme

GUILD_ID = [958468593358626816, 745428142428258426]

class NewMember(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command()
    async def new_teacher(self, ctx: commands.context.Context, teacher: discord.Member):
        if ctx.author.guild_permissions.administrator:
            newMembers: list[discord.Member] = []
            for member in ctx.guild.members:
                newMember = True
                for role in member.roles:
                    if not discord.Role.is_default(role):
                        newMember = False
                        break

                if newMember:
                    newMembers.append(member.name)

            if teacher.name not in newMembers:
                await ctx.send(f"The new teacher must be a new member: {teacher.name} is not a new member")
                return

            for role in ctx.guild.roles:
                if role.name == "Teacher-Moderator":
                    await teacher.add_roles(role)

            await ctx.send("Completed!")
        else:
            await ctx.send("You do not have permission to use this command")


    @slash_command(name="moderator", description="Makes a member a teacher or moderator.",guild_ids=GUILD_ID)
    async def moderator(self, ctx: commands.context.Context, teacher: discord.Member):
        if ctx.author.guild_permissions.administrator:
            newMembers: list[discord.Member] = []
            for member in ctx.guild.members:
                if len(member.roles) == 1:
                    newMembers.append(member.name)

            if teacher.name not in newMembers:
                await ctx.send(f"The new teacher must be a new member: {teacher.name} is not a new member")
                return

            for role in ctx.guild.roles:
                if role.name == "Teacher-Moderator":
                    teacher.add_roles(role)

            await ctx.send("Completed!")
        else:
            await ctx.send("You do not have permission to use this command")

    @commands.command()
    async def new_student(self, ctx: commands.context.Context, student: discord.Member, classroom: discord.Role):
        if ctx.author.guild_permissions.administrator:
            newMembers: list[discord.Member] = []
            for member in ctx.guild.members:
                newMember = True
                for role in member.roles:
                    if not discord.Role.is_default(role):
                        newMember = False
                        break

                if newMember:
                    newMembers.append(member.name)
            
            if student.name not in newMembers:
                await ctx.send(f"The new student must be a new member: {student.name} is not a new member")
                return

            if classroom.name in [role.name for role in ctx.guild.roles]:
                await ctx.send("Completed")
                await student.add_roles(classroom)

        else:
            await ctx.send("You do not have permission to use this command")


    @slash_command(guild_ids=GUILD_ID, name="student", description="Makes a member a student.")
    async def student(self, ctx: commands.context.Context, student: discord.Member, classroom: discord.Role):
        if ctx.author.guild_permissions.administrator:
            newMembers: list[discord.Member] = []
            for member in ctx.guild.members:
                if len(member.roles) == 1:
                    newMembers.append(member.name)
            
            if student.name not in newMembers:
                await ctx.send(f"The new student must be a new member: {student.name} is not a new member")
                return

            if classroom.name in [role.name for role in ctx.guild.roles]:
                await ctx.send("Completed")
                await student.add_roles(classroom)

        else:
            await ctx.send("You do not have permission to use this command")


    @commands.command()
    async def new_classroom(self, ctx: commands.context.Context, classroom: str):
        # need to modify this command to not allow for entering the new classroom
        # instead use a time and date function to fill in the semester and class
        # year
        if ctx.author.guild_permissions.administrator:
            oldColors = [role.color.value for role in ctx.guild.roles]

            newColor = discord.Color.random()
            while newColor.value in oldColors:
                newColor = discord.Color.random()

            oldClassRooms = [role.name for role in ctx.guild.roles]
            if classroom not in oldClassRooms:
                await ctx.guild.create_role(name=classroom, colour=newColor)
                await ctx.send(f"New Class added {classroom}")
            else:
                await ctx.send("Class is already in the Guild")
        else:
            await ctx.send("You do not have permission to use this command")


    @slash_command(guild_ids=GUILD_ID, name="classroom", description="Add a classroom to the server",)
    async def classroom(self, ctx: commands.context.Context, classroom: str):
        # need to modify this command to not allow for entering the new classroom
        # instead use a time and date function to fill in the semester and class
        # year
        if ctx.author.guild_permissions.administrator:
            oldColors = [role.color.value for role in ctx.guild.roles]

            newColor = discord.Color.random()
            while newColor.value in oldColors:
                newColor = discord.Color.random()

            oldClassRooms = [role.name for role in ctx.guild.roles]
            if classroom not in oldClassRooms:
                await ctx.guild.create_role(name=classroom, colour=newColor)
                await ctx.send(f"New Class added {classroom}")
            else:
                await ctx.send("Class is already in the Guild")
        else:
            await ctx.send("You do not have permission to use this command")




def setup(bot):
    bot.add_cog(NewMember(bot))