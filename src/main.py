
from json import load, dump
from os import getenv
import discord
from discord.ext import commands

SUMMON_COMMAND= getenv('SUMMON_COMMAND') or '*:salt:'
EMOJI = getenv('EMOJI_NAME') or ':salt:'
API_KEY = getenv('API_KEY') or ''
SUMMON_ROLE = getenv('SUMMON_ROLE') or None

COMMANDS = '''
Commands:
    :salt: :salt: :salt:
    <user...>           Add user(s) to the list of saltees
    unsalt <user...>    Remove user(s) from the list of saltees
    h | help            Get help with commands

    You must have the role of {SUMMON_ROLE} to do this
'''

members = load('members.json')
client = discord.Client()
bot = commands.Bot(command_prefix=SUMMON_COMMAND)

@client.event
async def on_ready():
    print('Beep boop I have started')
    print(members)

@client.event
async def on_message(message):
    if message.channel.type == "private":
        await message.channel.send(commands)
        await react(message)
    # if sender is a member, react to message
    if should_salt(message):
        await react(message)
    if message.content.strip().startswith(SUMMON_COMMAND):
        on_summon(message)

async def on_summon(message):
    content = message.content.split()
    if len(content) < 2:
        await react(message)

    command = content[1]
    if command == 'h' or command == ['help']:
        await message.channel.send(COMMANDS)
        return
    if can_summon(message.author):
        member_ids = map(lambda member: member.id, members)
        if command = "unsalt":
            unsalt(member_ids)
        else:
            add_members(member_ids)
    else: 
        message.channel.send(f'You need the role of {SUMMON_ROLE} to do that, dummy')
        await react(message)

async def react(message):
    await message.add_reaction(EMOJI)
    print(f'I just reacted to a message : {message.content}')

def can_summon(author):
    return (not SUMMON_ROLE) or SUMMON_ROLE in filter(lambda role: role.name, author.roles)

def should_salt(message):
    mentions_ids = map(lambda mention: mention.id, message.mentions)
    return  (message.author.id in members) or (client and client.id in mention_ids)

def add_members(member_ids):
    for id in member_ids:
        if id not in members:
            members.append(id)
    update_member_file()
    
def unsalt(member_ids):
    members = [member for member in members if member not in member_ids]
    update_member_file()

def update_member_file():
    with open('members.json', 'w') as f:
        dump(members, f)

client.run(API_KEY)

    



