
import discord
from discord.ext import commands
from pyson import pyson

currency=pyson('currency')

if 'name' not in currency.data:
    currency.data['name']='dollars'

bot=commands.Bot(command_prefix="++")

@bot.event
async def on_ready():
    print('Logged in as: '+bot.user.name)
    print('With user ID: '+bot.user.id)

def check_id(ID):
    if ID not in currency.data:
        currency.data[ID]=0
        currency.save()

def is_approved():
    def predicate(ctx):
        author=ctx.message.author
        if author==ctx.message.server.owner or ('administrator',True) in author.server_permissions:
            return True
        return False
    return commands.check(predicate)   

@is_approved()
@bot.command()
async def currency_type(ntype:str='dollars'):
    ''': Change name of your currency'''
    ptype=currency.data['name']
    currency.data['name']=ntype
    currency.save()
    await bot.say(f'The economy type has been changed from **{ptype}** to **{ntype}**')

@is_approved()
@bot.command(pass_context=True)
async def add(ctx,amount:int=0,member:discord.Member=None):
    ''': Add points/currency to a member's stash'''
    ID=member.id
    check_id(ID)
    currency.data[ID]+=amount
    currency.save()
    await bot.say(f'''{amount} {currency.data["name"]} have been added to {member.mention}'s stash''')

@is_approved()
@bot.command(pass_context=True)
async def remove(ctx,amount:int=0,member:discord.Member=None):
    ''': Remove points/currency from a member's stash'''
    ID=member.id
    check_id(ID)
    currency.data[ID]-=amount
    currency.save()
    await bot.say(f'''{amount} {currency.data["name"]} has been removed from {member.mention}'s stash''')

@bot.command(pass_context=True)
async def stash(ctx):
    ''': Check your stash!'''
    member=ctx.message.author
    check_id(member.id)
    await bot.reply(f'you have {currency.data[member.id]} {currency.data["name"]}')

@bot.command(aliases=['leaderboards'])
async def leaderboard():
    ''': View the server leaderboad'''
    members=[(ID,score) for ID,score in currency.data.items() if ID !='name']
    if len(members)==0:
        await bot.say('I have nothing to show')
        return
    ordered=sorted(members,key=lambda x:x[1] ,reverse=True )
    players=''
    scores=''
    for ID,score in ordered:
        player=discord.utils.get(bot.get_all_members(),id=ID)
        players+=player.mention+'\n'
        scores+=str(score)+'\n'
    embed=discord.Embed(title='Leaderboard')
    embed.add_field(name='Player',value=players)
    embed.add_field(name='Score',value=scores)
    await bot.say(embed=embed)
            

bot.run('TOKEN')
