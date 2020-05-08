import discord
from discord.ext import commands
import discord.guild

import json
import configparser
from datetime import datetime, timedelta, time, tzinfo
from typing import Tuple, Dict, Any
from Gambler import Gamble
from level_stuff import *


TOKEN = ' '
client = commands.Bot(command_prefix='~')
client.remove_command('help')
data = dict()
level_info = dict()
identify = []
movies = []
casino = Gamble()

PRICES = dict()
role_cap = 0


def parse_payment(message):  # Returns payment amount from command
    for part in message:
        if part.isdigit():
            return int(part, 10)
    return 0


def ledger():
    with open("BankBook.json", 'w') as bankbook:
        global data
        json.dump(data, bankbook)
        bankbook.close()

    with open("leveling.json", 'w') as leveling:
        global level_info
        json.dump(level_info, leveling)
        leveling.close()

    with open("movielist.txt", 'w') as movielist:
        global movies
        movielist.writelines(movies)
        movielist.close()


@client.event
async def on_ready():
    config = configparser.ConfigParser()
    config.read('SETTINGS.INI')

    global role_cap
    role_cap = int(config['DEFAULT']['roleCap'])
    global PRICES
    PRICES['name'] = int(config['DEFAULT']['name'])
    PRICES['role'] = int(config['DEFAULT']['role'])
    PRICES['movie'] = int(config['DEFAULT']['movie'])

    with open("BankBook.json") as bankbook:
        global data
        data = json.load(bankbook)
        bankbook.close()

    with open("leveling.json") as leveling:
        global level_info
        level_info = json.load(leveling)
        leveling.close()

    with open("blacklist.txt", 'r') as ban:
        global identify
        identify = ban.readlines()
        ban.close()

    with open("movielist.txt", 'r') as movielist:
        global movies
        movies = movielist.readlines()
        movielist.close()

    print("Setup is complete!")


@client.event
async def on_message(message):
    player = str(message.author.id)
    words = message.content
    timing = message.created_at
    global identify

    if player not in identify:
        try:
            level = level_info[player]['level']
            last_time = datetime.strptime(level_info[player]['time'], '%X')
        except:
            level_info[player] = {"xp": 0.0, "level": 1, "time": timing.strftime("%X")}
            level = 1
            last_time = timing

        difference = timing - last_time
        if difference.seconds >= 60 and words.find("~") == -1:
            level_info[player]['time'] = timing.strftime("%X")
            cap = xp_cap(level)
            xp = xp_yield(level)
            level_info[player]['xp'] += float(xp)

            if level_info[player]['xp'] > cap:
                level_info[player]['xp'] -= float(cap)
                level_info[player]['level'] += 1
                data[player]['balance'] += 3
                await message.channel.send("You've-a earned-a trio spaghett-a!")

    ledger()
    await client.process_commands(message)


@client.command(pass_context=True)
async def slots(ctx):
    player = str(ctx.message.author.id)
    content = ctx.message.split(" ")
    amount = parse_payment(content)
    data[player]['balance'] -= int(amount)

    casino.setBet(amount, player)
    winnings, end_msg, results = casino.roll_slots(player)
    await ctx.message.channel.send("You-a rolled and got-a {}", results)


    if winnings > 0:
        await ctx.message.channel.send(end_msg)
        data[player]['balance'] += int(winnings)
    else:
        await ctx.message.channel.send(end_msg)

    ledger()


@client.command(pass_context=True)
async def help(ctx):
    message = ctx.message
    await message.channel.send("command-a prefix is-a ~\n stimulus <@ the user you want-a to a-reward> <amount of-a spaghett to pay-a> "
                         "--This command is for admins only.\n deposit <@ the user you want to pay> <amount of spaghett to pay them\n> "
                         "--This command is for everyone so that you can move munny around\n")


@client.command(pass_context=True)
async def role(ctx):
    user = str(ctx.message.author.id)
    chan = ctx.message.channel
    global data
    global PRICES
    global roleCap

    startBal = data[user]['balance']

    # Take the spaghett and assign new role
    if data[user]['balance'] >= int(PRICES['role']):
        base_role = ctx.author.top_role

        for thing in ctx.guild.roles:
            if base_role >= roleCap:
                await chan.send("You stupido! You're already at-a the top-a!")
                break

            if thing.position > base_role.position:
                await ctx.author.remove_roles(base_role)
                await ctx.author.add_roles(thing)
                data[user]['balance'] -= int(PRICES['role'])

                if data[user]['balance'] == startBal:
                    print("Spaghett was not deducted in role purchase")

                break
            else:
                continue
    else:
        chan.send("You don't-a have enough-a spaghett!")

    ledger()


@client.command(pass_context=True)
async def nickname(ctx):
    global PRICES
    global data
    content = ctx.message.content.split(" ")

    if data[user]['balance'] >= PRICES['name']:
        newName = " "
        word = 0
        while True:
            if i == 0:
                continue
            elif i == len(content):
                newName += content[i]
                break
            elif i == 1:
                newName = content[i]+" "
            else:
                newName += content[i]+" "
            i += 1
        await ctx.author.edit(nick=new_name)
        data[user]['balance'] -= PRICES['name']
    else:
        await chan.send("You don't-a have enough-a spaghett!")

    ledger()


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def stimulus(ctx):
    content = ctx.message.content.split(" ")
    amount = parse_payment(content)
    try:
        recipient = str(ctx.message.mentions[0].id)
    except:
        print("Line 149 didn't work\n")

    if recipient in data.keys():
        data[recipient]['balance'] += int(amount)
    else:
        data[recipient] = {'name': ctx.message.mentions[0].display_name, 'balance': int(amount)}

    ledger()


@client.command(pass_context=True)
@commands.has_guild_permissions(administrator=True)
async def debt(ctx):
    content = ctx.message.content.split(" ")
    amount = parse_payment(content)

    debtor = str(ctx.message.mentions[0].id)

    if data[debtor]['balance'] > abs(amount):
        data[debtor]['balance'] -= abs(int(amount))

    ledger()


@client.command(pass_context=True)
async def deposit(ctx):
    content = ctx.message.content.split(" ")
    amount = parse_content(content)
    recipient = str(ctx.message.mentions[0].id)
    who_paid = str(ctx.message.author.id)

    if data[who_paid]['balance'] < amount:
        ctx.message.channel.send("Not enough-a spaghett!")
        return
    data[who_paid]['balance'] -= int(amount)

    if recipient in data.keys():
        data[recipient]['balance'] += int(amount)
    else:
        data[recipient] = {'name': ctx.message.mentions[0].display_name, 'balance': int(amount)}

    ledger()


@client.command(pass_context=True)
async def balance(ctx):
    account = str(ctx.message.author.id)
    chan = ctx.message.channel

    if account in data.keys():
       await chan.send("You have-a "+str(data[account]['balance'])+" Spaghett-a")
    else:
       await chan.send("Who-a the fuck are-a you? I-a don't see-a you in-a the bank-a book.")


@client.command(pass_context=True)
#@commands.is_owner()
async def leave(ctx):
    ledger()
    await client.close()
    await client.logout()


def get_Token():
    global TOKEN
    config = configparser.ConfigParser()
    config.read('SETTINGS.INI')
    TOKEN = config['DEFAULT']['token']


get_Token()
client.run(TOKEN)


#		USES FOR SPAGHETT
#	[] Earn Papa's respect
#	[] Change your nickname
#	[*] Climb the ranks
#       [] Betting/Gambling
#		[] lottery
#		[] rng (roulette, slots)
#			[] output roll results
#		[] card games
#			[] Poker maybe
#			[] Blackjack
#		[] Petty bets ("I bet 20 spaghett that billy is gonna fuck up as thatcher.")
#	[] Stonks
#		HOW TO GET SPAGHOOTIES
#	[*] Text chat (like level/rank gaining in MEE6)
#	[*] Stimulus from admins (Money printer go brrrrrrrrrrrr)
#	[*] payment from others
#	[] Gambling

# TO DO learn to interface with MEE6
#	is it even possible to interface? Does it have an api of some kind?
