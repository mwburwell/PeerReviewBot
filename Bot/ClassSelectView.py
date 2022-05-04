
import discord
import discord.ui

class ClassSelect(discord.ui.Select):
    def __init__(self, guild, newclass: discord.Role):
        self.guild = guild
        self.newclass = newclass
        self.flag = True
        members = self.CreateMemberList(guild=guild)
        options = [discord.SelectOption(label=member.name) for member in members]

        super().__init__(
            placeholder="Which students do you want to add to the Class...",
            max_values=len(options),
            options=options,
        )  

    def CreateMemberList(self, guild):
        Membersset = [guild.owner]
        for m in guild.members:
            if (len(m.roles) == 1):
                Membersset.append(m)
        return Membersset

    async def callback(self, interaction: discord.MessageInteraction):
            if self.flag:
                self.flag = False
                for val in self.values:
                    for m in self.guild.members:
                        if (m.name == val):
                            await m.add_roles(self.newclass)
            else:
                self.flag = True

class ClassSelectView(discord.ui.View):
    def __init__(self, guild, newclass):
        self.guild = guild
        self.newclass = newclass
        super().__init__()
        # Adds the dropdown to our view object.
        self.add_item(ClassSelect(self.guild, self.newclass))
