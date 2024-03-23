import discord
from discord.ext import commands
import json
import os
import random
if not os.path.exists("users.json"):
    with open("users.json", "w") as f:
        json.dump({}, f)

# Schaut ob es gibt der user
with open("users.json", "r") as f:
    users = json.load(f)

intents = discord.Intents.default()

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def online(ctx):
    online_count = ctx.guild.member_count
    await ctx.send(f"На сервере онлайн {online_count} человек.")
# Command für das Balance
@bot.command()
async def balance(ctx):
    user_id = str(ctx.author.id)
    await ctx.send(f"{ctx.author.mention}, ihre balance: {users.get(user_id, 0)} €")

# Command für verdienen das Geld
@bot.command()
async def earn(ctx):
    user_id = str(ctx.author.id)
    earnings = random.randint(1, 100)
    users[user_id] = users.get(user_id, 0) + earnings
    with open("users.json", "w") as f:
        json.dump(users, f)
    await ctx.send(f"{ctx.author.mention}, sie haben verdient {earnings} €!")

# Command für Kaufen
@bot.command()
async def spend(ctx, amount: int):
    user_id = str(ctx.author.id)
    if users.get(user_id, 0) < amount:
        await ctx.send(f"{ctx.author.mention}, Sie habe kein geld!")
    else:
        users[user_id] -= amount
        with open("users.json", "w") as f:
            json.dump(users, f)
        await ctx.send(f"{ctx.author.mention}, sie haben so viel € {amount} gespendet!")

# Command für spenden
@bot.command()
async def transfer(ctx, recipient: discord.Member, amount: int):
    author_id = str(ctx.author.id)
    recipient_id = str(recipient.id)

    if users.get(author_id, 0) < amount:
        await ctx.send(f"{ctx.author.mention}, Sie haben nicht zu viel geld!")
    else:
        users[author_id] -= amount
        users[recipient_id] = users.get(recipient_id, 0) + amount
        with open("users.json", "w") as f:
            json.dump(users, f)
        await ctx.send(
            f"{ctx.author.mention}, sie haben mit ohne probleme  {amount} das geld gepsendet für das User {recipient.mention}!"
        )


@bot.event
async def on_message(message):
    print(f'Получено сообщение от {message.author}: {message.content}')
    await bot.process_commands(message)
bot.run("")