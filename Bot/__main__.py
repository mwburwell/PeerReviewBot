import discord
from discord import Intents
from discord.ext import commands

import os
from dotenv import load_dotenv

from Bot import GUILD_ID
# from Bot import GUILD_ID

GUILD_ID = [958468593358626816]

from Bot.PromotionView import PromoteClassView
from Bot.AddModules import DropdownView
load_dotenv()

prefix = commands.when_mentioned_or("!")
token = os.environ['TOKEN']

intents = Intents.default()
intents.members = True
intents.message_content = True
# intents.guilds = True

bot = commands.Bot(command_prefix= prefix, intents= intents)

@bot.event
async def on_ready():
    await bot.register_commands()
    GUILD_ID = [guild.id for guild in bot.guilds]
    print(f"{bot.user} has logged in!")

@bot.slash_command(name="moderator", description="Makes a member a teacher or moderator.",guild_ids=GUILD_ID)
async def moderator(ctx: commands.context.Context, teacher: discord.Member):
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

@bot.slash_command(guild_ids=GUILD_ID, name="classroom", description="Add a classroom to the server",)
async def classroom(ctx: commands.context.Context, classroom: str):
    # need to modify this command to not allow for entering the new classroom
    # instead use a time and date function to fill in the semester and class
    # year
    if ctx.author.guild_permissions.administrator:
        oldColors = [role.color.value for role in ctx.guild.roles]

        newColor = discord.Color.random()
        print("old Colors: ", oldColors)
        print("new colors: ", newColor.value)
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


@bot.slash_command(guild_ids=GUILD_ID, name="student", description="Makes a member a student.")
async def student(ctx: commands.context.Context, student: discord.Member, classroom: discord.Role):
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




@bot.slash_command(guild_ids=GUILD_ID, name= "advancement", description="Alter's a classes permissions to allow viewing of the next module or demoting to the previous module")
async def advancement(ctx: discord.commands.context.ApplicationContext):
    if ctx.author.guild_permissions.administrator:				
        print("\nPromote Slash Command: ")
        classes: list[discord.Role] = []

        for role in ctx.guild.roles:
            if role.name.startswith('class'):
                classes.append(role)

        promoteMenu = PromoteClassView(classroomRoles= classes)
        await ctx.respond("Promote class or Demote class", view = promoteMenu)

    else:
        await ctx.respond("You do not have permission to use this command")

omittedFiles = ["Bot.cogs.AddClass","Bot.cogs.AddStudent","Bot.cogs.AddTeacher"]

cogfiles: list[str] = []
for filename in os.listdir("./Bot/cogs/"):
    if filename.endswith(".py"):
        cogfiles.append(f"Bot.cogs.{filename[:-3]}")

for cogfile in cogfiles:
    # print(cogfile)
    try:
        bot.load_extension(cogfile)
        print(f"loaded: {cogfile}")
    except Exception as err:
        print(err)

bot.run(token)