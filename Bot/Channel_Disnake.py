from ast import Pass
import asyncio
from asyncore import read
from dis import dis
from gettext import Catalog
from http import client
import imp
from lib2to3.pgen2.token import SLASH
import os
import typing
from pydoc import describe
import random
from tokenize import Token
from turtle import position, textinput
from unicodedata import category, name
from discord import Guild, Interaction
# import discord
# from discord.ext import commands
# from discord_slash import SlashCommand, SlashContext
import disnake
from disnake.ext import commands
import Readme
from setuptools import Command

def main():
    print(disnake.__version__)

    intent = disnake.Intents.default()
    intent.members = True
    val = 0
    #intent.message_content = True

    client = commands.Bot(command_prefix="<>", intents = intent)

    @client.event
    async def on_ready():
        print(f"{client.user.name} has connected")

    class Dropdown(disnake.ui.Select):
        def __init__(self, guild):
            self.guild = guild
            self.flag = True
            # Set the options that will be presented inside the dropdown
            options = [
                disnake.SelectOption(
                    label="1", description="There is 1 Module"
                ),
                disnake.SelectOption(
                    label="4", description="There are 4 Modules"
                ),
                disnake.SelectOption(
                    label="8", description="There are 8 Modules"
                ),
                disnake.SelectOption(
                    label="16", description="There are 16 Modules"
                ),
            ]

            super().__init__(
                placeholder="How many modules are in the Class...",
                min_values=1,
                max_values=1,
                options=options,
            )  

        async def callback(self, interaction: disnake.MessageInteraction):
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

    class DropdownView(disnake.ui.View):
        def __init__(self, guild):
            self.guild = guild
            super().__init__()
            # Adds the dropdown to our view object.
            self.add_item(Dropdown(self.guild))      

    @client.event
    async def on_guild_join(guild):
        view = DropdownView(guild)
        await guild.text_channels[0].send("How many Modules do you want?", view = view)
        overwrites = {
            guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            guild.me: disnake.PermissionOverwrite(read_messages=True)
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
        overwrites = {
            guild.default_role: disnake.PermissionOverwrite(read_messages=False),
            guild.me: disnake.PermissionOverwrite(read_messages=True)
        }
        await guild.create_category("Teachers_Channel", overwrites=overwrites, position=0)
        for c in (guild.categories):
            if (c.name == "Teachers_Channel"):
                Cat = c
        await guild.create_text_channel("Moderate-Classroom", overwrites=overwrites, category=Cat)
        await guild.create_text_channel("Bot-Info", overwrites=overwrites, category=Cat)
        await Cat.text_channels[1].send(Readme.Readme.Readme())
    
    @client.listen()
    async def on_message(ctx):
         if (ctx.content.startswith("Hello")):
             await ctx.channel.send(f"Hi {ctx.author.mention}!")

         if ctx.content.startswith("$guess"):
            await ctx.channel.send("Guess a number between 1 and 10.")

            def is_correct(m):
                return m.author == ctx.author and m.content.isdigit()

            answer = random.randint(1, 10)

            try:
                guess = await client.wait_for("message", check=is_correct, timeout=5.0)
            except asyncio.TimeoutError:
                return await ctx.channel.send(f"Sorry, you took too long it was {answer}.")

            if int(guess.content) == answer:
                await ctx.channel.send("You are right!")
            else:
                await ctx.channel.send(f"Oops. It is actually {answer}.")


    #slash = SlashCommand(client, sync_commands=True)

    @client.slash_command(
        name="hello",
        description="Just to send a message",
        guild_ids=[958468593358626816]
    )
    async def _hello(ctx):
        await ctx.send(f"{ctx.author.mention} has activated a command.")


    class Confirm(disnake.ui.View):
        def __init__(self):
            super().__init__()
            self.value = None

        @disnake.ui.button(label="Confirm",style=disnake.ButtonStyle.green)
        async def confirm(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
            await interaction.response.send_message("Conforming", ephemeral=True)
            self.value = True
            self.stop()

        @disnake.ui.button(label="Cancel",style=disnake.ButtonStyle.gray)
        async def cancel(self, button: disnake.ui.Button, interaction: disnake.MessageInteraction):
            await interaction.response.send_message("Cancelling", ephemeral=True)
            self.value = False
            self.stop()        

    @client.slash_command(
        name="Button",
        description="Calls forth a button",
        guild_ids=[958468593358626816]
    )
    async def _Button(ctx):
        view = Confirm()
        await ctx.send("Do you want to continue?", view=view)

        await view.wait()
        if view.value is None:
            print("Time out...")
        elif view.value:
            print("Confirmed...")
        else:
            print("Cancelled")

    client.run("OTYyNzg3MTM2MjEyNDUxMzk4.YlMnZA.TvtbX17F7MynW1Qr7U8dMIQQJK0")

if __name__ == '__main__':
    main()