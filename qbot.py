import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json
import datetime
from discord.ext.commands import CommandNotFound
import os
import requests
from discord import Webhook, AsyncWebhookAdapter
import aiohttp
import ctypes


def mbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, text, title, style)


def updater():
    version = "0"
    mbox('Automatically Checking For Updates!', 'Updater', 0)
    url = "https://raw.githubusercontent.com/Kimigo/TatoBot/main/version.txt"
    req = requests.get(url)
    version2 = req.text
    if version == version2:
        pass
    else:
        url1 = "https://raw.githubusercontent.com/Kimigo/TatoBot/main/qbot.py"
        request = requests.get(url1)
        code = request.text
        fa = open("bot.py", "w+")
        fa.write(code)
        fa.close()
        os.system("bot.py")


intents = discord.Intents.default()
intents.members = True
intents.presences = True
bot = commands.Bot(command_prefix="t!", intents=intents)
color = 0x00FFFF

bot.remove_command('help')


@bot.event
async def on_ready():
    print(f"{bot.user} ready!")


@bot.command(pass_context=True, no_dm=True)
async def apply(ctx):
    await ctx.message.delete()
    if ctx.channel.id == 804913455597092934:
        first = datetime.datetime.utcnow()
        at = ctx.author
        em = discord.Embed(color=color, description="Please answer the following questions!")
        em.set_footer(text="Made by Kimigo#3171")
        dm = await at.send(embed=em)

        def check(message):
            return message.author == ctx.author and message.channel == dm.channel

        q = ["IGN?", "Alt Account?", "Age?", "Time Zone?",
             "Previous Minecraft experience (when you started, what type of player you are etc. This should be more "
             "than "
             "one sentence)",
             "Why do you want to join this server, and what can you add to it?(This should be more than one sentence)",
             "What is the secret code found in the rules?",
             "Anything you would like to add?"]

        async def aq(qu):
            await at.send(qu)
            rep = await bot.wait_for('message', check=check)
            return rep.content

        q1 = await aq(q[0])
        q2 = await aq(q[1])
        q3 = await aq(q[2])
        q4 = await aq(q[3])
        q5 = await aq(q[4])
        q6 = await aq(q[5])
        q7 = await aq(q[6])
        q8 = await aq(q[7])

        if str(q7).lower() == 'coconuts'.lower():

            emem = discord.Embed(color=color)
            emem.add_field(name='Q1', value=str(q1), inline=False)
            emem.add_field(name='Q2', value=str(q2), inline=False)
            emem.add_field(name='Q3', value=str(q3), inline=False)
            emem.add_field(name='Q4', value=str(q4), inline=False)
            emem.add_field(name='Q5', value=str(q5), inline=False)
            emem.add_field(name='Q6', value=str(q6), inline=False)
            emem.add_field(name='Q7', value=str(q7), inline=False)
            emem.add_field(name="Q8", value=str(q8), inline=False)
            end = datetime.datetime.utcnow()
            emem.set_footer(
                text=f'{ctx.author.name}#{ctx.author.discriminator} | Start: {first} | End: {end} | '
                     f'Made by Kimigo#3171',
                icon_url=ctx.author.avatar_url)

            with open("config.json", "r") as wa:
                chn = json.load(wa)
            lop = chn['responsechannel']
            channel = bot.get_channel(int(lop))
            await channel.send(embed=emem)
            lmao = discord.Embed(color=color, description='Your application was submitted successfully!')
            lmao.set_footer(text='Made by Kimigo#3171')
            await at.send(embed=lmao)
            async with aiohttp.ClientSession() as session:
                webhook = Webhook.from_url('webhook_url', adapter=AsyncWebhookAdapter(session))
                await webhook.send(embed=emem)

        else:
            lpoa = discord.Embed(color=color, description='Please read the rules entirely!')
            await at.send(embed=lpoa)


@bot.command(pass_context=True, no_dm=True)
@has_permissions(administrator=True)
async def setresponse(ctx):
    with open("config.json", "r") as wa:
        chn = json.load(wa)

    chn['responsechannel'] = str(ctx.channel.id)

    with open('config.json', 'w') as wa:
        json.dump(chn, wa)

    em = discord.Embed(color=color, description='Response channel set!')
    em.set_footer(text='Made my Kimigo#3171')
    await ctx.send(embed=em)


@bot.command(pass_context=True, no_dm=True)
@has_permissions(administrator=True)
async def setapply(ctx):
    with open("config.json", "r") as wa:
        chn = json.load(wa)

    chn['applychannel'] = str(ctx.channel.id)

    with open('config.json', 'w') as wa:
        json.dump(chn, wa)

    em = discord.Embed(color=color, description='Application channel set!')
    em.set_footer(text='Made my Kimigo#3171')
    await ctx.send(embed=em)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return


with open("config.json", "r") as f:
    tkn = json.load(f)
    bot.run(tkn['token'])
