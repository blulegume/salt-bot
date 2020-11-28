
from json import load, dump
from os import getenv
import discord
from discord.ext import commands

SUMMON_COMMAND= getenv('SUMMON_COMMAND') or '🧂'
EMOJI = getenv('EMOJI_NAME') or '🧂'
API_KEY = getenv('API_KEY') or 'NO API KEY'
SUMMON_ROLE = getenv('SUMMON_ROLE') or None

COMMANDS = f'''
:salt: :salt: :salt:
```
Commands:
    🧂🧂 <user...>          Add user(s) to the list of saltees
    🧂unsalt <user...>      Remove user(s) from the list of saltees
    🧂h                     Get help with commands

Role required to do this: {SUMMON_ROLE}
```
'''

member_store = []
with open('members.json', 'r') as f:
    member_store = load(f)

bot = commands.Bot(command_prefix=SUMMON_COMMAND)

@bot.listen('on_ready')
async def on_ready():
    print('Beep boop I have started')
    print(member_store)
    

@bot.listen('on_message')
async def on_message(message):
    if message.channel.type == "private":
        await message.channel.send(commands)
        await react(message)

    if should_salt(message):
        await react(message)

async def react(message):
    await message.add_reaction(EMOJI)

def should_salt(message):
    mention_ids = map(lambda mention: mention.id, message.mentions)
    return  (message.author.id in member_store) # or (bot and bot.id in mention_ids)


@bot.command()
async def h(ctx):
    await ctx.send(COMMANDS)

@bot.command(name="🧂")
async def salt(ctx, members: commands.Greedy[discord.Member]):
    if can_summon(ctx.author):
        add_members(members)
    else: 
        ctx.send(f'You need the role of {SUMMON_ROLE} to do that, dummy')
        await react(ctx.message)

@bot.command()  
async def unsalt(ctx, members: commands.Greedy[discord.Member]):
    if can_summon(ctx.author):
        remove_members(members)
        
    else:
        ctx.send(f'You need the role of {SUMMON_ROLE} to do that, dummy')
        await react(ctx.message)

def can_summon(author):
    return (not SUMMON_ROLE) or SUMMON_ROLE in filter(lambda role: role.name, author.roles)

def add_members(members):
    member_ids = get_member_ids(members)
    for id in member_ids:
        if id not in member_store:
            member_store.append(id)
        else:
            print(f'{id} is i n member store {member_store}')
    update_member_file()
    print(f'Added {", ".join(get_member_names(members))}')

def remove_members(members):
    member_ids = get_member_ids(members)
    for id in member_ids:
        if id in member_store:
            member_store.remove(id)
    update_member_file()
    print(f'Removed {", ".join(get_member_names(members))}')

def update_member_file():
    with open('members.json', 'w') as f:
        dump(member_store, f)

def get_member_ids(members):
    return list(map(lambda member: member.id, members))

def get_member_names(members):
    return list(map(lambda member: member.name, members))

bot.run(API_KEY)

    



