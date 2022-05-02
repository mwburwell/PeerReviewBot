# Author Michael Peck

import discord
from discord.commands import slash_command
from discord.ext import commands
import discord.ui

from Bot.ClassSelectView import ClassSelectView

#from setuptools import Command

# from Bot import GUILD_ID, Readme

GUILD_ID = [958468593358626816, 745428142428258426]

class NewMember(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command()
    async def new_teacher(self, ctx: commands.context.Context, teacher: discord.Member):
        #if ctx.author.guild_permissions.administrator or 
        print(type(ctx))
        pass

    @commands.command()
    async def new_student(self, ctx, student: discord.Member):
        pass

    @commands.command()
    async def new_classroom(self, ctx, classroom: str):
        pass

    @slash_command(
        guild_ids=[958468593358626816],
        name="new_t",
        description="Promotes a use to Teacher"
    )
    async def new_t(
        self,
        ctx: discord.commands.context.ApplicationContext,
        user: discord.Member
        ):
        print(f"\nNew Teacher: {user.name}")
        await ctx.respond("Creating new Teacher")
        # if (ctx.author == ctx.guild.owner):
        #     Teach = self.FindTeacher(ctx.guild)
        #     await user.add_roles(Teach)
        #     await ctx.respond("Complete!")

    @slash_command(
        guild_ids=[958468593358626816],
        name="new_s",
        description="Add student to class"
    )
    async def new_s(
        self,
        ctx: discord.commands.context.ApplicationContext,
        # user: discord.Member,
        # classroom: discord.Role
        ):
        await ctx.respond("New Student")
        # print(f"\nNew Student: {user.name}")
        # if self.ValidateUser(ctx):
        #     try:
        #         # await classroom.members()
        #         await user.add_roles(classroom)
        #         await ctx.respond("Complete!")
        #     except discord.ValidationError as err:
        #         print("Discord Validation Error")
        #         print(err)
        #     except Exception as err:
        #         print("New Student Exception: ")
        #         print(err)


    @slash_command(
        guild_ids=[958468593358626816],
        name="addclass",
        description="Make Classroom"
    )
    async def addclass(
        self,
        ctx: discord.commands.context.ApplicationContext,
        classroom: str = "class01"
        ):
        await ctx.respond("New class")
        print(f"\nNew Classroom: {classroom}")
        # if (self.ValidateUser(ctx)):
        #     NewClass = await ctx.guild.create_role(name=classroom)
        #     view = ClassSelectView(ctx.guild, NewClass)
        #     overwrites = {
        #     ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
        #     ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
        #     NewClass: discord.PermissionOverwrite(read_messages=True),
        #     self.FindTeacher(ctx.guild): discord.PermissionOverwrite(read_messages=True)
        #     }
        #     for c in (ctx.guild.categories):
        #         if (c.name == "Classroom Chat"):
        #             Cat = c
        #     await ctx.guild.create_text_channel(classroom, category=Cat, overwrites=overwrites)
        #     await ctx.send("Add Students?", view=view)
        #     await ctx.respond("Started!")


    # def CreateRolesList()->list[discord.Role]:
    #     RoleSet = []
    #     for r in .roles:
    #         if r.name.startswith("Class"):
    #             RoleSet.append(r)
    #     return RoleSet

    # def ValidateUser(self, ctx):
    #     flag = False
    #     author = ctx.author
    #     roles = author.roles
    #     print(author)
    #     print(ctx.guild.owner)
    #     for r in roles:
    #         if (r.name == "Teacher"):
    #             flag = True
    #     if (author == ctx.guild.owner):
    #         flag = True
    #     return flag

    # def FindTeacher(self, guild):
    #     for r in guild.roles:
    #         if (r.name == "Teacher"):
    #             return r



def setup(bot):
    bot.add_cog(NewMember(bot))