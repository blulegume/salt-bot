import discord
from discord.ext import commands
from member_manager import MemberManager as Mgr

class Rbmk(commands.Cog):
    '''
    A Discord bot that reacts to messages. Anyone with the specified role  can
    add a member of their server to the list of reactees.
    '''
    
    def __init__(self, bot, emoji, summon_role):
        self.emoji = emoji
        self.summon_role = summon_role

        Mgr.load_store()

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

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.type == "private":
            await message.channel.send(commands)
            await self.react(message)

        if self.should_salt(message):
            await self.react(message)

    @commands.command()
    async def h(self, ctx):
        await ctx.send(self.COMMANDS)

    @commands.command()
    async def clear(self, ctx):
        Mgr.clear_members(ctx.guild.id)
        await ctx.send('ugh, fine')

    @commands.command(name="🧂")
    async def salt(self, ctx, members: commands.Greedy[discord.Member]):
        await self._salt(ctx, members, Mgr.add_members)

    @commands.command()  
    async def unsalt(self, ctx, members: commands.Greedy[discord.Member]):
        await self._salt(ctx, members, Mgr.remove_members)

    @commands.command(name="list")  
    async def ls(self, ctx):
        await ctx.send(f'Currently salty: {Mgr.list_members(ctx.guild.id)}')

    async def react(self, message, emoji=None):
        await message.add_reaction(emoji if emoji else self.emoji)

    def should_salt(self, message):
        return Mgr.exists(message.guild.id, message.author.id)

    async def _salt(self, ctx, members: commands.Greedy[discord.Member], fn):
        '''Add or remove members'''
        if self.can_summon(ctx.author):
            fn(ctx.guild.id, members)
            await self.react(ctx.message, '👍')
        else:
            ctx.send(f'You need the role of {self.summon_role} to do that, dummy')
            await self.react(ctx.message)

    def can_summon(self, author):
        return (not self.summon_role) or self.summon_role in filter(lambda role: role.name, author.roles)
