
import discord
from discord.ext import commands
from pyson import pyson
from itertools import cycle

england=pyson('england')
brittany=pyson('brittany')
soldier=pyson('infantry')

if 'name' not in soldier.data:
    soldier.data['name']='infantry'

if 'name' not in brittany.data:
    brittany.data['name']='brittany'


bot=commands.Bot(command_prefix="!")

@bot.event
async def on_ready():
    print('Logged in as: '+bot.user.name)
    print('With user ID: '+bot.user.id)

def check_id(ID):
    if ID not in soldier.data:
        soldier.data[ID]=0
        soldier.save()

def check_ID2(ID):
    if ID not in brittany.data:
        brittany.data[ID]=0
        brittany.save()

def is_approved():
    def predicate(ctx):
        author=ctx.message.author
        if author==ctx.message.server.owner or ('administrator',True) in author.server_permissions:
            return True
        return False
    return commands.check(predicate)   

@is_approved()
@bot.command(pass_context=True)
async def add(ctx,amount:int=0,member:discord.Member=None):
    ''': Add infantry to a member's army'''
    
    ID=member.id
    check_id(ID)
    soldier.data[ID]+=amount
    soldier.save()
    await bot.say(f'''{amount} {soldier.data["name"]} have been added to {member.mention}'s army''')

@is_approved()
@bot.command(pass_context=True)
async def addbrittany(ctx,amount:int=0,member:discord.Member=None):
    ''': Add infantry to a member's army'''
    ID=member.id
    check_ID2(ID)
    brittany.data[ID]+=amount
    brittany.save()
    await bot.say(f'''{amount} {brittany.data["name"]} have been added to {member.mention}'s army''')

@is_approved()
@bot.command(pass_context=True)
async def remove(ctx,amount:int=0,member:discord.Member=None):
    ''': Remove infantry from a member's army'''
    ID=member.id
    check_id(ID)
    soldier.data[ID]-=amount
    soldier.save()
    await bot.say(f'''{amount} {soldier.data["name"]} has been removed from {member.mention}'s army''')

@bot.command(pass_context=True)
async def totalarmy(ctx):
    ''': Check your army!'''
    member=ctx.message.author
    check_id(member.id)
    await bot.reply(f'you have {soldier.data[member.id]} {soldier.data["name"]}')

@bot.command(aliases=['leaderboards'])
async def leaderboard():
    ''': View the server leaderboad'''
    members=[(ID,score) for ID,score in soldier.data.items() if ID !='name']
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
            

bot.run('tokem')
