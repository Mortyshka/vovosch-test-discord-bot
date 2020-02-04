import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot

Bot=commands.Bot(command_prefix="!")


@Bot.event
async def on_ready():
	print("Я онлайн!")


@Bot.event
async def on_member_join(member):
	role=discord.utils.get(member.guild.roles, name = "Всякий сброд")
	await member.add_roles(role)


@Bot.command()
async def hello(ctx):
	author = ctx.message.author
	await ctx.send(f"Hello {author.mention}")
	# await ctx.send(f"Hello <@{author.id}>")	# или так


@Bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
	mute_role=discord.utils.get(ctx.message.guild.roles, name = "Ты в муте, долбаёб")
	await member.add_roles(mute_role)


@Bot.command()
async def reaction(ctx):
        await ctx.message.add_reaction("🤡")



token=os.environ.get('BOT_TOKEN')	# для сервера, чтобы никто не видел токен
Bot.run(str(token))

#Bot.run(open('token.txt','r').readline())	# чтение токена из файла
