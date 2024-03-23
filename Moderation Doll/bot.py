#Das bot für Moderation des Server Doll
import discord
from discord.ext import commands

TOKEN = ''

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

#Ban
@bot.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention} был забанен.')

#Mute
@bot.command()
async def mute(ctx, member: discord.Member, *, reason=None):
    role = discord.utils.get(ctx.guild.roles, name="Muted")
    if not role:
        role = await ctx.guild.create_role(name="Muted")

        for channel in ctx.guild.channels:
            await channel.set_permissions(role, send_messages=False)

    await member.add_roles(role, reason=reason)
    await ctx.send(f'{member.mention} был замучен.')

#Warn
@bot.command()
async def warn(ctx, member: discord.Member, *, reason=None):
    await ctx.send(f'{member.mention} получил предупреждение: {reason}')

#Joining
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("Вы должны быть в голосовом канале, чтобы бот мог присоединиться.")

#Kick
@bot.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} был кикнут.')

#List of Ban Words
forbidden_words = ['Nigger', 'Niger', 'Niga', 'Faggot', 'Gay', 'Shit', 'Нигер', 'пидорас', 'Пидорас']
@bot.event
async def on_message(message):
    print(f'Получено сообщение от {message.author}: {message.content}')

    for word in forbidden_words:
        if word in message.content:
            await message.delete()
            await message.channel.send(f'{message.author.mention}, ваше сообщение было удалено, так как оно содержало запрещённое слово.')
            break 
    await bot.process_commands(message)

bot.run(TOKEN)