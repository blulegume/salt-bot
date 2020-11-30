from os import getenv
from discord.ext import commands
from rbmk import Rbmk

COMMAND_PREFIX= getenv('SUMMON_COMMAND') or '🧂'
EMOJI = getenv('EMOJI') or '🧂'
TOKEN = getenv('TOKEN')
SUMMON_ROLE = getenv('SUMMON_ROLE') or None

bot = commands.Bot(command_prefix=COMMAND_PREFIX)
bot.add_cog(Rbmk(bot, EMOJI, SUMMON_ROLE))

bot.run(TOKEN)