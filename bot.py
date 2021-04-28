from discord.ext import commands
import subprocess
import threading
import aiofiles
import discord
import asyncio
import aiohttp
import random
import ctypes
import re
import os

ctypes.windll.kernel32.SetConsoleTitleW('zoom')
token = ''
prefix = '/'

intents = discord.Intents().all()
bot = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
bot.remove_command('help')

administrators = []
chat_channel = 
bots_channel = 
queue = []

def zoom():
    while True:
        try:
            task, arg1, arg2 = queue.pop(0).split('-')
            subprocess.run([f'{task}', f'{arg1}', f'{arg2}'])
        except:
            pass

threading.Thread(target=zoom).start()

@bot.event
async def on_ready():
    print(f'Servers: {len(bot.guilds)}')
    for guild in bot.guilds:
        print(guild.name)
    print()
    # bot.loop.create_task(status())
    while True:
        members = sum([guild.member_count for guild in bot.guilds])
        activity = discord.Activity(type=discord.ActivityType.watching, name=f'{members} users!')
        await bot.change_presence(activity=activity)
        await asyncio.sleep(60)

@bot.event
async def on_member_join(member):
    channel = await bot.fetch_channel(bots_channel)
    await channel.send(f'Welcome to **zoom**, {member.mention}.\nType `/help` to get started!')

@bot.event
async def on_command_error(ctx, error: Exception):
    if ctx.channel.id == bots_channel:
        if isinstance(error, commands.CommandOnCooldown):
            embed = discord.Embed(color=16379747, description=f'{error}')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(color=16379747, description='You are missing arguments required to run this command!')
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
        elif 'You do not own this bot.' in str(error):
            embed = discord.Embed(color=16379747, description='You do not have permission to run this command!')
            await ctx.send(embed=embed)
        else:
            print(str(error))
    else:
        try:
            await ctx.message.delete()
        except:
            pass

@bot.command()
async def help(ctx):
    print(f'{ctx.author} | {ctx.author.id} -> /help')
    if ctx.channel.type != discord.ChannelType.private:
        embed = discord.Embed(color=16379747)
        embed.add_field(name='Help', value='`/help`', inline=True)
        embed.add_field(name='Open Ticket', value='`/ticket`', inline=True)
        embed.add_field(name='Close Ticket', value='`/close`', inline=True)
        embed.add_field(name='Tasks', value='`/tasks`', inline=True)
        embed.add_field(name='Twitch Followers', value='`/tfollow (channel)`', inline=True)
        embed.add_field(name='⭐ Twitch Spam', value='`/tspam (channel) (message)`', inline=True)
        embed.add_field(name='Roblox Followers', value='`/rfollow (user id)`', inline=True)
        embed.add_field(name='Roblox Templates', value='`/rget (asset id)`', inline=True)
        await ctx.send(embed=embed)

@bot.command()
async def ticket(ctx):
    print(f'{ctx.author} | {ctx.author.id} -> /ticket')
    if ctx.channel.type != discord.ChannelType.private:
        channels = [str(x) for x in bot.get_all_channels()]
        if f'ticket-{ctx.author.id}' in str(channels):
            embed = discord.Embed(color=16379747, description='You already have a ticket open!')
            await ctx.send(embed=embed)
        else:
            ticket_channel = await ctx.guild.create_text_channel(f'ticket-{ctx.author.id}')
            await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
            await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
            embed = discord.Embed(color=16379747, description='Please enter the reason for this ticket, type `/close` if you want to close this ticket.')
            await ticket_channel.send(f'{ctx.author.mention}', embed=embed)
            await ctx.message.delete()

@bot.command()
async def close(ctx):
    print(f'{ctx.author} | {ctx.author.id} -> /close')
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.channel.name == f'ticket-{ctx.author.id}':
            await ctx.channel.delete()
        elif ctx.author.id in administrators and 'ticket' in ctx.channel.name:
            await ctx.channel.delete()
        else:
            embed = discord.Embed(color=16379747, description=f'You do not have permission to run this command!')
            await ctx.send(embed=embed)

@bot.command()
async def tasks(ctx):
    print(f'{ctx.author} | {ctx.author.id} -> /tasks')
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.channel.id == bots_channel:
            embed = discord.Embed(color=16379747, description=f'`{len(queue)}` tasks in the queue!')
            await ctx.send(embed=embed)
        else:
            await ctx.message.delete()

tfollow_cooldown = []

@bot.command()
@commands.cooldown(1, 600, type=commands.BucketType.user)
async def tfollow(ctx, channel, amount: int=None):
    print(f'{ctx.author} | {ctx.author.id} -> /tfollow {channel}')
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.channel.id == bots_channel or ctx.author.id in administrators:
            if str(channel.lower()) in tfollow_cooldown and ctx.author.id not in administrators:
                try:
                    await ctx.message.delete()
                except:
                    pass
            else:
                try:
                    if '-' in str(channel):
                        raise Exception
                    max_amount = 0
                    if ctx.author.id in administrators:
                        tfollow.reset_cooldown(ctx)
                        max_amount += 1000
                    premium = discord.utils.get(ctx.guild.roles, name='Premium')
                    if premium in ctx.author.roles:
                        max_amount += 1000
                    diamond = discord.utils.get(ctx.guild.roles, name='Diamond')
                    if diamond in ctx.author.roles:
                        max_amount += 750
                    gold = discord.utils.get(ctx.guild.roles, name='Gold')
                    if gold in ctx.author.roles:
                        max_amount += 450
                    silver = discord.utils.get(ctx.guild.roles, name='Silver')
                    if silver in ctx.author.roles:
                        max_amount += 250
                    bronze = discord.utils.get(ctx.guild.roles, name='Bronze')
                    if bronze in ctx.author.roles:
                        max_amount += 100
                    booster = discord.utils.get(ctx.guild.roles, name='Booster')
                    if booster in ctx.author.roles:
                        max_amount += 75
                    _75 = discord.utils.get(ctx.guild.roles, name='+75')
                    if _75 in ctx.author.roles:
                        max_amount += 75
                    _25 = discord.utils.get(ctx.guild.roles, name='+25')
                    if _25 in ctx.author.roles:
                        max_amount += 25
                    _10 = discord.utils.get(ctx.guild.roles, name='+10')
                    if _10 in ctx.author.roles:
                        max_amount += 10
                    _5 = discord.utils.get(ctx.guild.roles, name='+5')
                    if _5 in ctx.author.roles:
                        max_amount += 5
                    max_amount += 25
                    if amount is None:
                        amount = max_amount
                    elif amount > max_amount:
                        amount = max_amount
                    if amount <= max_amount:
                        premium = discord.utils.get(ctx.guild.roles, name='Premium')
                        if premium in ctx.author.roles:
                            position = len(queue) + 1
                            # embed = discord.Embed(color=16379747, description=f'Added `tfollow-{channel}-{amount}` to queue! (`1/{position}`)')
                            embed = discord.Embed(color=16379747, description=f'Adding `{amount}` followers to `{channel}`! (`1/{position}`)')
                            await ctx.send(embed=embed)
                            queue.insert(0, f'tfollow-{channel}-{amount}')
                        else:
                            position = len(queue) + 1
                            # embed = discord.Embed(color=16379747, description=f'Added `tfollow-{channel}-{amount}` to queue! (`{position}/{position}`)')
                            embed = discord.Embed(color=16379747, description=f'Adding `{amount}` followers to `{channel}`! (`{position}/{position}`)')
                            await ctx.send(embed=embed)
                            queue.append(f'tfollow-{channel}-{amount}')
                        if ctx.author.id not in administrators:
                            tfollow_cooldown.append(str(channel.lower()))
                            await asyncio.sleep(600)
                            tfollow_cooldown.remove(str(channel.lower()))
                except:
                    embed = discord.Embed(color=16379747, description='An error has occured while attempting to run this command!')
                    await ctx.send(embed=embed)
                    tfollow.reset_cooldown(ctx)
        else:
            await ctx.message.delete()
            tfollow.reset_cooldown(ctx)

@bot.command()
@commands.cooldown(1, 600, type=commands.BucketType.user)
async def tspam(ctx, channel, *, msg):
    print(f'{ctx.author} | {ctx.author.id} -> /tspam {channel} {msg}')
    if ctx.channel.type != discord.ChannelType.private:
        premium = discord.utils.get(ctx.guild.roles, name='Premium')
        if premium in ctx.author.roles:
            if ctx.channel.id == bots_channel:
                try:
                    max_amount = 0
                    if ctx.author.id in administrators:
                        tspam.reset_cooldown(ctx)
                    max_amount += 25
                    amount = None
                    if amount is None:
                        amount = max_amount
                    if amount <= max_amount:
                        position = len(queue) + 1
                        embed = discord.Embed(color=16379747, description=f'Added `tspam-{channel}-{msg}` to queue! (`1/{position}`)')
                        await ctx.send(embed=embed)
                        queue.insert(0, f'tspam-{channel}-{msg}')
                except:
                    embed = discord.Embed(color=16379747, description='An error has occured while attempting to run this command!')
                    await ctx.send(embed=embed)
                    tspam.reset_cooldown(ctx)
            else:
                await ctx.message.delete()
                tspam.reset_cooldown(ctx)
        else:
            embed = discord.Embed(color=16379747, description='You do not have permission to run this command!')
            await ctx.send(embed=embed)

rfollow_cooldown = []

@bot.command()
@commands.cooldown(1, 600, type=commands.BucketType.user)
async def rfollow(ctx, user_id, amount: int=None):
    print(f'{ctx.author} | {ctx.author.id} -> /rfollow {user_id}')
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.channel.id == bots_channel or ctx.author.id in administrators:
            if str(user_id) in rfollow_cooldown and ctx.author.id not in administrators:
                try:
                    await ctx.message.delete()
                except:
                    pass
            else:
                try:
                    int(user_id)
                    max_amount = 0
                    if ctx.author.id in administrators:
                        rfollow.reset_cooldown(ctx)
                        max_amount += 5000
                    max_amount += 25
                    if amount is None:
                        amount = max_amount
                    elif amount > max_amount:
                        amount = max_amount
                    if amount <= max_amount:
                        premium = discord.utils.get(ctx.guild.roles, name='Premium')
                        if premium in ctx.author.roles:
                            position = len(queue) + 1
                            embed = discord.Embed(color=16379747, description=f'Adding `{amount}` followers to `{user_id}`! (`1/{position}`)')
                            await ctx.send(embed=embed)
                            queue.insert(0, f'rfollow-{user_id}-{amount}')
                        else:
                            position = len(queue) + 1
                            embed = discord.Embed(color=16379747, description=f'Adding `{amount}` followers to `{user_id}`! (`{position}/{position}`)')
                            await ctx.send(embed=embed)
                            queue.append(f'rfollow-{user_id}-{amount}')
                        if ctx.author.id not in administrators:
                            rfollow_cooldown.append(str(user_id))
                            await asyncio.sleep(600)
                            rfollow_cooldown.remove(str(user_id))
                except:
                    embed = discord.Embed(color=16379747, description='An error has occured while attempting to run this command!')
                    await ctx.send(embed=embed)
                    rfollow.reset_cooldown(ctx)
        else:
            await ctx.message.delete()
            rfollow.reset_cooldown(ctx)

@bot.command()
async def rget(ctx, asset_id):
    print(f'{ctx.author} | {ctx.author.id} -> /rget {asset_id}')
    if ctx.channel.type != discord.ChannelType.private:
        if ctx.channel.id == bots_channel:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f'https://assetdelivery.roblox.com/v1/asset?id={asset_id}') as r:
                        r = await r.text()
                    async with session.get(f'https://assetdelivery.roblox.com/v1/asset?id=' + re.search('id=(.*)</url>', r).group(1)) as r:
                        r = await r.read()
                try:
                    f = await aiofiles.open(f'{asset_id}.png', mode='wb')
                    await f.write(r)
                    await f.close()
                    embed = discord.Embed(color=16379747)
                    file = discord.File(f'{asset_id}.png')
                    embed.set_image(url=f'attachment://{asset_id}.png')
                    await ctx.send(embed=embed, file=file)
                finally:
                    try:
                        os.remove(f'{asset_id}.png')
                    except:
                        pass
            except:
                embed = discord.Embed(color=16379747, description='An error has occured while attempting to run this command!')
                await ctx.send(embed=embed)
        else:
            await ctx.message.delete()

bot.run(token)
