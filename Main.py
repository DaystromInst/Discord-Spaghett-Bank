import discord
from discord.ext import commands
import discord.guild

import json
from typing import Tuple, Dict, Any

TOKEN = ' '
client = commands.Bot(command_prefix='~')
client.remove_command('help')
data = dict()


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


@client.event
async def on_ready():
    with open("BankBook.json") as bankbook:
        global data
        data = json.load(bankbook)
        bankbook.close()
    print("Setup is complete!")


@client.command(pass_context=True)
async def help(ctx):
    message = ctx.message
    await message.channel.send("command-a prefix is-a ~\n stimulus <@ the user you want-a to a-reward> <amount of-a spaghett to pay-a> "
                         "--This command is for admins only.\n deposit <@ the user you want to pay> <amount of spaghett to pay them\n> "
                         "--This command is for everyone so that you can move munny around\n")


@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def stimulus(ctx):
    content = ctx.message.content.split(" ")
    amount = parse_payment(content)
    try:
        recipient = str(ctx.message.mentions[0].id)
    except:
        print("Line 56 didn't work\n")

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
@commands.is_owner()
async def leave(ctx):
    ledger()
    await client.close()
    await client.logout()

def get_Token():
    key = open("token.txt", "r")
    global TOKEN
    TOKEN = key.readline()
    key.close()

get_Token()
client.run(TOKEN)


#		USES FOR SPAGHETT
#	[] Earn Papa's respect
#	[] Change your nickname
#	[] Climb the ranks
#       [] Betting/Gambling
#		- lottery
#		- rng (roulette, slots)
#		- card games
#		- Petty bets ("I bet 20 spaghett that billy is gonna fuck up as thatcher.")
#	[] Stonks
#		HOW TO GET SPAGHOOTIES
#	[] Text chat (like level/rank gaining in MEE6)
#	[] Stimulus from admins (Money printer go brrrrrrrrrrrr)
#	[] payment from others
#	[] 

# TODO learn to interface with MEE6
#	is it even possible to interface? Does it have an api of some kind?
