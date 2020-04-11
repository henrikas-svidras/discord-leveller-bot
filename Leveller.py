# Leveller.py

import os

import discord
from discord.ext import commands

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

@bot.command(name='Bot', help='gali pakviesti mane ir pasisveikinti su manimi.')
async def sveikinimas(ctx):
    response = f'Sveikas, {ctx.author.name}, kuo galiu padėti?'
    await ctx.send(response)

@bot.command(name='Role', help='gali pakviesti mane ir suzinoti savo role.')
async def roliu_tikrinimas(ctx):
    response = f'Sveikas, {ctx.author.name}: tavo aukščiausia  rolė yra {ctx.author.top_role}.'
    await ctx.send(response)

@bot.command(name='SetRoleFor', help='gali pakviesti mane ir nustatysiu role liurbiui. Bet gali tik zemesnes uz save.')
async def roliu_nustatymas(ctx,useris:str,role:str):
    dcuser = discord.utils.get(ctx.message.guild.members, name = useris)
    if not dcuser:
        await ctx.send('nėra tokio LIURBAGALVIO šitame serveryje!')
        return
    dcrole = discord.utils.get(ctx.message.guild.roles, name = role)
    if not dcrole:
        await ctx.send('nėra tokios rolės, LIURBAGALVI!')
        return
    if dcuser.top_role == ctx.message.guild.roles[-1]:
        await ctx.send(f'{ctx.message.guild.roles[-1].name.capitalize()[:-2]}Ų DEMOKTRATIŠKU PROCESU NEPAŠALINSI.')
        return
    if dcrole ==  ctx.message.guild.roles[-1]:
        await ctx.send(f'{ctx.message.guild.roles[-1].name.capitalize()[:-2]}AIS NEPASKIRIAMA - ETMONAIS TAMPAMA!')
        return
    if ctx.author.top_role > dcrole:
        response = f'Sveikinu, dabar: {dcuser.name} turi rolę {dcrole.name}.'
        for role in dcuser.roles[1:]:
          await dcuser.remove_roles(role,reason='setting a new role via {bot.name}.')
        await dcuser.add_roles(dcrole,reason='{ctx.author.name} nustate role {bot.name} pagalba.')
    else:
        response = f'neturi teisės {ctx.author.top_role.name[:-2]}e nelaimingas!'
    await ctx.send(response)

@bot.command(name='RemoveRoleFor',help='istrina visas roles is userio, very sad times...')
async def roliu_nuemimas(ctx,useris:str):
    dcuser = discord.utils.get(ctx.message.guild.members, name = useris)
    if not dcuser:
        await ctx.send('nėra tokio LIURBAGALVIO šitame serveryje!')
        return
    elif dcuser.top_role == ctx.message.guild.roles[-1]:
        await ctx.send(f'{ctx.message.guild.roles[-1].name.capitalize()[:-2]}Ų DEMOKTRATIŠKU PROCESU NEPAŠALINSI.')
        return
    elif ctx.author.top_role > dcuser.top_role:
        response = f'Sveikinu, dabar: {dcuser.name} nebeturi jokių rolių.'
        for role in dcuser.roles[1:]:
          await dcuser.remove_roles(role,reason='setting a new role via {bot.name}')
    else:
        response = f'neturi teisės {ctx.author.top_role.name[:-2]}e nelaimingas!'
    await ctx.send(response)

@bot.command(name='SetNickFor',help='nustatysiu niką, šiam gerajam useriui, kokį paliepsi')
async def niko_nustatymas(ctx,useris:str,nikas:str=''):
    dcuser = discord.utils.get(ctx.message.guild.members, name = useris)
    if not dcuser:
        await ctx.send('nėra tokio LIURBAGALVIO šitame serveryje!')
        return
    if dcuser.top_role == ctx.message.guild.roles[-1]:
        await ctx.send(f'{ctx.message.guild.roles[-1].name.capitalize()} PATS RENKASI SAVO VARDĄ')
        return
    elif ctx.author.top_role >= dcuser.top_role:
        await dcuser.edit(nick=nikas)
        response = f'sveikinu, dabar {dcuser.name} turi niką {dcuser.nick}'
    else:
        response = f'neturi teisės {ctx.author.top_role.name[:-2]}e nelaimingas!'
    await ctx.send(response)



@bot.event
async def on_command_error(ctx,error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Šiaip siūlau prieš naudojant gal paskaityti biškį kaip veikia low IQ tu')

bot.run(TOKEN)
