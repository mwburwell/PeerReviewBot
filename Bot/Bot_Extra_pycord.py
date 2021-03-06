# Author Michael Peck

from ast import Break
from asyncore import read
from http import client
import imp
from lib2to3.pgen2.token import SLASH
from multiprocessing.connection import Client
import os
from pickle import FALSE, TRUE
from pydoc import describe
from tokenize import Token
from unicodedata import name
import discord
from discord.ext import commands
import discord.ui
#from setuptools import Command
from discord.commands import Option

import Readme

def main():

    
    print(discord.__version__)
    
    intent = discord.Intents.default()
    intent.members = True
    intent.message_content = True

    client = commands.Bot(command_prefix="<>", intents = intent)

    @client.event
    async def on_ready():
        print(f"{client.user.name} has connected")

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
                    overwrites = {
                        self.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                        self.guild.me: discord.PermissionOverwrite(read_messages=True),
                        FindTeacher(self.guild): discord.PermissionOverwrite(read_messages=True)
                    }
                    await self.guild.create_category("Classroom Chat", position=1)
                    for i in range(1, int(self.values[0]) + 1):
                        await self.guild.create_category(f"Module-{i}", position=i)
                        for c in (self.guild.categories):
                            if (c.name == f"Module-{i}"):
                                Cat = c
                        await self.guild.create_text_channel("Best-Of", category=Cat, overwrites=overwrites)
                    await interaction.response.send_message(f"There are {self.values[0]} Modules.")
                else:
                    await interaction.response.send_message("Implementation already used.")

    class DropdownView(discord.ui.View):
        def __init__(self, guild):
            self.guild = guild
            super().__init__()
            # Adds the dropdown to our view object.
            self.add_item(Dropdown(self.guild))      

    @client.event
    async def on_guild_join(guild):
        view = DropdownView(guild)
        await guild.text_channels[0].send("How many Modules do you want?", view = view)
        await guild.create_role(name="Teacher")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            FindTeacher(guild): discord.PermissionOverwrite(read_messages=True)
        }
        await guild.create_category("Teachers_Channel", overwrites=overwrites, position=0)
        for c in (guild.categories):
            if (c.name == "Teachers_Channel"):
                Cat = c
        await guild.create_text_channel("Moderate-Classroom", overwrites=overwrites, category=Cat)
        await guild.create_text_channel("Bot-Info", overwrites=overwrites, category=Cat)
        await Cat.text_channels[1].send(Readme.Readme.Readme())

    @client.command()
    async def ping(ctx):
        """Checks for response form bot"""
        guild = ctx.guild
        view = DropdownView(guild)
        await guild.text_channels[0].send("How many Modules do you want?", view = view)
        await guild.create_role(name="Teacher")
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            FindTeacher(guild): discord.PermissionOverwrite(read_messages=True)
        }
        await guild.create_category("Teachers_Channel", overwrites=overwrites, position=0)
        for c in (guild.categories):
            if (c.name == "Teachers_Channel"):
                Cat = c
        await guild.create_text_channel("Moderate-Classroom", overwrites=overwrites, category=Cat)
        await guild.create_text_channel("Bot-Info", overwrites=overwrites, category=Cat)
        await Cat.text_channels[1].send(Readme.Readme.Readme())

    @client.slash_command(
        name="new_teacher",
        description="Promotes a use to Teacher",
        guild_ids=[958468593358626816, 966429842532884490],
    )
    async def new_teacher(
        ctx,
        user: discord.Member
        ):
        if (ctx.author == ctx.guild.owner):
            Teach = FindTeacher(ctx.guild)
            await user.add_roles(Teach)
            await ctx.respond("Complete!")

    @client.slash_command(
        name="new_classroom",
        description="Make Classroom",
        guild_ids=[958468593358626816, 966429842532884490],
    )
    async def new_classroom(
        ctx,
        classroom: str
        ):
        if (ValidateUser(ctx)):
            NewClass = await ctx.guild.create_role(name=classroom)
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(read_messages=False),
            ctx.guild.me: discord.PermissionOverwrite(read_messages=True),
            NewClass: discord.PermissionOverwrite(read_messages=True),
            FindTeacher(ctx.guild): discord.PermissionOverwrite(read_messages=True)
        }
            for c in (ctx.guild.categories):
                if (c.name == "Classroom Chat"):
                    Cat = c
            await ctx.guild.create_text_channel(classroom, category=Cat, overwrites=overwrites)
            await ctx.respond("Complete!")

    def ValidateUser(ctx):
        flag = False
        author = ctx.author
        roles = author.roles
        for r in roles:
            if (r.name == "Teacher"):
                flag = True
        if (author == ctx.guild.owner):
            flag = True
        return flag

    def FindTeacher(guild):
        for r in guild.roles:
            if (r.name == "Teacher"):
                return r

    client.run("OTYyNzg3MTM2MjEyNDUxMzk4.YlMnZA.g1fbpVCA4BE6EMuY1101s67Xe0c")


main()