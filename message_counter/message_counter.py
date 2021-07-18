#/usr/bin/python3

"""
Dogs
"""
# message_counter_bot.py

import os
import pandas as pd
from collections import defaultdict
import datetime
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='counter!', intents=intents)

@bot.command('count_alive_messages')
async def count(message):
    """
    Hello
    """  

    if not message.author.name == 'Heinrich':
        print('nope')
        return 0
    print('Counting')
    MOB2Categories = [
        'MOB2: CONTINENTS',
        'MOB2 CONFESSIONALS',
        'MOB2 ALLIANCES',
    ]

    deadPPL = {
        'Arpiyen': 'Not Damien (S2-18th)',
        'Darius*': 'Darius (S2-17th)',
        'Angeleka':'Amanda (S2-16th)',
        'EchoKangaroo': 'Echo (S2-15th)',
        'BourkieBoy': 'Bourkie (S2-14th)',
        'eagle2ch': 'Eagle (S2-13th)',
        'Ripple': 'Ripple (S2-12th)',
        'pancake': 'Whimsicott (removed)',
        'marjorie': 'Marjorie (removed)'
    }

    TestCategories = ['Voice Channels']
    game_start = datetime.datetime(2021,4,15,00,00,00)
    from_date = datetime.datetime(2021,4,15,00,00,00)
    to_date = datetime.datetime.now()

    guild = message.author.guild
    alive_players = []

    for player in guild.members:
        for role in player.roles:
            if role.name == 'S2: Continents' or role.name == 'Dead' or role.name == 'Jury':
                alive_players.append(player)
    alive_player_message_time = {}
    alive_player_message_symb_count = {}

    for player in alive_players:
        # print(player.nick)
        # print(player.name)
        name = player.nick if player.nick is not None else player.name
        alive_player_message_time[name] = []
        alive_player_message_symb_count[name] = []
    for player_name in deadPPL.values():
        alive_player_message_time[player_name] = []
        alive_player_message_symb_count[player_name] = []

    for category in guild.categories:
        if category.name in MOB2Categories:
            print(f'Looking at {category.name}')
            for channel in category.text_channels:
                i = 0
                print(f'Looking at {channel.name}')

                async for msg in channel.history(limit=100000, after=from_date, before=to_date):
                    if msg.author in alive_players or msg.author.name in list(deadPPL.keys()):
                        if msg.author.name in list(deadPPL.keys()):
                            name = deadPPL[msg.author.name]
                        else:
                            name = msg.author.nick if msg.author.nick is not None else msg.author.name
                        message_time = (msg.created_at-game_start).seconds + (msg.created_at-game_start).days*24*3600
                        message_length = len(msg.content)
                        # if i < 5:
                        #     print(msg.content)
                        #     i += 1
                        alive_player_message_time[name].append(message_time)
                        alive_player_message_symb_count[name].append(message_length)

    alive_players_list = list(alive_player_message_time.keys())
    message_times = list(alive_player_message_time.values())
    message_lengths = list(alive_player_message_symb_count.values())
    pandas_pre = {
        "Players":alive_players_list,
        "Times":message_times,
        "Lengths":message_lengths
    }
    pddf = pd.DataFrame(pandas_pre)
    print('Done')

    outputfilename = f'message_count_{from_date.month}_{from_date.day}.hdf'
    pddf.to_hdf(outputfilename, key='message_dates')
    #print(pddf)
    print(f'created {outputfilename}')

days_votes = {}
@bot.command("vote")
async def vote(ctx, name):
    print(find_player(ctx.guild, name))
    days_votes[ctx.author.name] = name

@bot.command("show_votes")
async def vote(ctx):
    await ctx.channel.send(days_votes)

def find_player(server, player_name):
    for player in server.members:
        print(player)
        if player_name is player.name:
            return True
        elif player_name is player.nick:
            return True
        elif player_name is player.id:
            return True
        else:
            return False

bot.run(TOKEN)
