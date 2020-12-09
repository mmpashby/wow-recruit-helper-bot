# bot.py
import os
import sys
import discord
from discord.embeds import Embed
import requests as r
import raiderio

from discord.ext import commands

## CONFIG RELATED CONSTS
EXPANSION = "Shadowlands"
TOKEN = os.getenv('DISCORD_TOKEN')
RAIDERIO_URL = "https://raider.io/api/v1"
NO_DUNGEONS_CS = 8
FIFTEEN_TIMED = 161


# TODO: break out into multi-class for character return info etc
class RecruitDecision:
    """Class responsable for performing recruitment type decisions."""
    def __init__(self, role, apirsp):
        self.role = role
        self.body = apirsp
        self.rolescore = self.get_role_score()
        self.ninetyninep = NO_DUNGEONS_CS * FIFTEEN_TIMED
        self.sixtysixp = round(((NO_DUNGEONS_CS * 2) / 3) * FIFTEEN_TIMED)
        self.recruitanswer = self.getdecision()

    def __str__(self):
        return "Recruit Decision Object..."

    def get_role_score(self):
        try:
            rolescore = self.body['mythic_plus_scores_by_season'][0]['scores'][self.role]
        except (KeyError, TypeError) as e:
            rolescore = 0
        return rolescore

    def getdecision(self):
        decision = "Unknown..."
        if self.rolescore >= self.ninetyninep:
            decision = "Recruit! Very Good - 15+ on all dungeons likely."
        elif self.rolescore >= self.sixtysixp:
            decision = "Recruit! Check ilvl and gain more info - Average - in 66p for this season assuming 15+ 2/3 keys."
        elif self.rolescore < self.sixtysixp:
            decision = "No - Below Average - below 66p for this season and likely needs work."
        return decision

    def readymsg(self):
        """Make message to discord look ok"""
        print(self.body)
        prsp = (
            f"**CharName:** {self.body['name']}\n",
            f"**Class:** {self.body['class']}\n",
            f"**Role:** {self.role}\n",
            f"**ilvl:** {self.body['gear']['item_level_equipped']}\n",
            f"**Role Score (current season):** {self.rolescore}\n",
            f"**Recruit(?):** {self.recruitanswer}"
        )
        return prsp


bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    io_api_conn = r.get(RAIDERIO_URL)
    if io_api_conn.status_code == 200:
        print(f'{bot.user.name} has established connection to raider.io...')
    else:
        print(f'{bot.user.name} could not establish connection to raider.io...exiting')
        sys.exit(1) 

@bot.command(name='recruit',
             help='Provides rudimentary recommendation engine for recruitment purposes.',
             usage='[PlayerName] [Role:dps/healer/tank] [Region] [Realm]')
async def recruit(ctx, player: str, role: str, region: str, realm: str):
    e = discord.Embed()
    sr = raiderio.resource("characters")
    s_params = {'player': player,
                'role': role,
                'region': region,
                'realm': realm}
    stat_code, grsp =  sr.get_char(**s_params)
    if stat_code == 200:
        rsp = grsp
        descision = RecruitDecision(role, rsp)
        dmsg = ''.join(descision.readymsg())
        e.set_image(url=rsp['thumbnail_url'])
        await ctx.send(dmsg, embed=e)
    elif stat_code == 400:
        rsp = "Character Not Found..."
        dmsg = ''.join(rsp)
        await ctx.send(dmsg)
    else:
        rsp = "Unknown Error..."
        dmsg = ''.join(rsp)
        await ctx.send(dmsg)

bot.run(TOKEN)