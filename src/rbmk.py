import discord
from discord.ext import commands
from json import load, dump

class Rbmk(commands.Cog):
    
    def __init__(self, bot, emoji, summon_role):
        self.emoji = emoji
        self.summon_role = summon_role
        self.member_store = {}


        self.load_member_store()

        self.COMMANDS = f'''
:salt: :salt: :salt:
```
Commands:
    🧂🧂 <user...>          Add user(s) to the list of saltees
    🧂unsalt <user...>      Remove user(s) from the list of saltees
    🧂clear                 Clear the list of saltees
    🧂list                  List the current saltees
    🧂h                     Print this message

Role required to do this: {self.summon_role}
```
'''

    @commands.Cog.listener()
    async def on_ready(self):
        print('Beep boop I have started')
        print(self.member_store)
        

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.type == "private":
            await message.channel.send(commands)
            await self.react(message)

        if self.should_salt(message):
            await self.react(message)

    async def react(self, message, emoji=None):
        await message.add_reaction(emoji if emoji else self.emoji)

    def should_salt(self, message):
        guild_name = message.guild.id
        return  guild_name in self.member_store and message.author.id in self.member_store[guild_name]


    @commands.command()
    async def h(self, ctx):
        await ctx.send(self.COMMANDS)

    @commands.command()
    async def clear(self, ctx):
        self.clear_members(ctx.guild.id)
        await ctx.send('ugh, fine')

    @commands.command(name="🧂")
    async def salt(self, ctx, members: commands.Greedy[discord.Member]):
        await self._salt(ctx, members, self.add_members)

    @commands.command()  
    async def unsalt(self, ctx, members: commands.Greedy[discord.Member]):
        await self._salt(ctx, members, self.remove_members)

    @commands.command(name="list")  
    async def ls(self, ctx):
        # await ctx.send(f'Currently salty: {','.join(self.get_saltees(ctx.guild.id))}')
        await ctx.send("that's private.")

    async def _salt(self, ctx, members: commands.Greedy[discord.Member], fn):
        if self.can_summon(ctx.author):
            fn(ctx.guild.id, members)
            await self.react(ctx.message, '👍')
        else:
            ctx.send(f'You need the role of {self.summon_role} to do that, dummy')
            await self.react(ctx.message)

    def can_summon(self, author):
        return (not self.summon_role) or self.summon_role in filter(lambda role: role.name, author.roles)

    def add_members(self, guild_name, members):
        member_ids = self.get_member_ids(members)
        if guild_name not in self.member_store:
            self.member_store[guild_name] = member_ids
        else: 
            guild_members = self.member_store[guild_name]
            for id in member_ids:
                if id not in guild_members:
                    guild_members.append(id)
                else:
                    print(f'{id} is already in member store for server {guild_name}')
        self.update_member_file()
        print(f'Added {", ".join(self.get_member_names(members))}')

    def remove_members(self, guild_name, members):
        if guild_name not in self.member_store:
            return
        else:
            guild_members = self.member_store[guild_name]
            member_ids = self.get_member_ids(members)
            for id in member_ids:
                if id in guild_members:
                    guild_members.remove(id)
        self.update_member_file()
        print(f'Removed {", ".join(self.get_member_names(members))}')

    def clear_members(self, guild_name):
        if guild_name not in self.member_store:
            return
        self.member_store[guild_name].clear()
        self.update_member_file()
        print('Cleared member store')

    def load_member_store(self):
        with open('members.json', 'r') as f:
            self.member_store = load(f)

    def update_member_file(self):
        with open('members.json', 'w') as f:
            dump(self.member_store, f)

    def get_member_ids(self, members):
        return list(map(lambda member: member.id, members))

    def get_member_names(self, members):
        return list(map(lambda member: member.name, members))

    def get_saltees(self, guild_id):
        return self.member_store[guild_id] if guild_id in self.member_store else 'nobody!'