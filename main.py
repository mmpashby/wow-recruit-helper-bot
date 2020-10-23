# bot.py
import os
import raiderio

# 1
from discord.ext import commands

TOKEN = os.getenv('DISCORD_TOKEN')

# 2
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    print(f'{bot.user.name} has established connection to raider.io...')

@bot.command(name='recruit',
             help='Provides rudimentary recommendation engine for recruitment purposes.',
             usage='[PlayerName] [Role] [Region] [Realm]')
async def recruit(ctx, player, role, region, realm):
    sr = raiderio.resource("characters")
    s_params = {'player': player,
                'role': role,
                'region': region,
                'realm': realm}
    rsp =  sr.get_char(**s_params)
    await ctx.send(rsp)


bot.run(TOKEN)