import os
import discord
from discord.ext import commands
from discord.ext.commands import Bot

ban_msg = ["qwe","123"]

prefix = '!'
Bot=commands.Bot(command_prefix=prefix)

# Удаляет команду
#Bot.remove_command('help')


# Говорит о начале работы бота
@Bot.event
async def on_ready():
	print("Я онлайн!")


# Фильтрация чата
@Bot.event
async def on_message(msg):
        #if msg.content in ban_msg:      # если сообщение в списке банов
        for i in ban_msg:               # если часть, которая в списке банов, есть в сообщении
                if i in msg.content:
                        await msg.delete()
        await Bot.process_commands(msg)


# Выдача роли новому члену сервера
@Bot.event
async def on_member_join(member):
	role=discord.utils.get(member.guild.roles, name = "Всякий сброд")
	await member.add_roles(role)


# Выдача роли по реакции
@Bot.event
async def on_raw_reaction_add(payload):
        POST_ID = 674874182483443722	# ID сообщения, где ставятся реакции
        circus = {
        '🐯':674857578932731925,  # тигр
        '🐉':674857717269135361,  # дракон
        '🤡':674857774215200789,  # клоун
        '🤖':674857894306512908,}  # машина
        if payload.message_id == POST_ID:
                
                try:
                        channel = Bot.get_channel(payload.channel_id) # канал, где было поставлена реакция (для нахождения объекта "cообщение")
                        message = await channel.fetch_message(payload.message_id) # получаем объект сообщения (для нахождения объекта "член")
                        member = discord.utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакци
                        if (str(payload.emoji) in circus.keys()):
                                role = discord.utils.get(message.guild.roles, id=circus[str(payload.emoji)]) # объект выбранной роли (если есть)
                                await member.add_roles(role)
                                print('[SUCCESS] User {0.display_name} has been granted with role {1.name}'.format(payload.member, role))
                        else:
                                await message.remove_reaction(payload.emoji, member)
                                print('[ERROR] Ban role for user {0.display_name}'.format(member))
                                
                except KeyError as e:
                        print('[ERROR] KeyError, no role found for ' + str(payload.emoji))
                except Exception as e:
                        print(repr(e))


# Удаление роли со снятием реакции (комменты см. в событии выше)
@Bot.event
async def on_raw_reaction_remove(payload):
        POST_ID = 674874182483443722
        circus = {
        '🐯':674857578932731925,  # тигр
        '🐉':674857717269135361,  # дракон
        '🤡':674857774215200789,  # клоун
        '🤖':674857894306512908,}  # машина
        if payload.message_id == POST_ID:
                
                try:
                        if (str(payload.emoji) in circus.keys()):
                                channel = Bot.get_channel(payload.channel_id)
                                message = await channel.fetch_message(payload.message_id) # получаем объект сообщения
                                member = discord.utils.get(message.guild.members, id=payload.user_id) # получаем объект пользователя который поставил реакци
                                role = discord.utils.get(message.guild.roles, id=int(circus[str(payload.emoji)])) # объект выбранной роли (если есть)
                                await member.remove_roles(role)
                                print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
                                
                except KeyError as e:
                        print('[ERROR] KeyError, no role found for ' + str(payload.emoji))
                except Exception as e:
                        print(repr(e))



@Bot.command(pass_context = True)
async def info(ctx, user: discord.User):
        """Выдаёт некую информацию"""
        emb = discord.Embed(title="Title", color=0x39d0d6)
        emb.add_field(name="Name", value="Value")
        if user.game is not None:
                emb.add_field(name="Game", value=user.game)
        emb.set_thumbnail(url=ctx.guild.icon_url)
        emb.set_author(name="Author", url=ctx.guild.icon_url)
        emb.set_footer(text="Footer", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=emb)


@Bot.command(pass_context = True)
async def create_role(ctx):
        """Создаёт новую роль"""
        new_name = ' '.join(ctx.message.content.split(' ')[1:]) # выделяет из сообщения название роли
        new_role = await ctx.guild.create_role()
        await new_role.edit(name=new_name, reason="А вот захотел")


@Bot.command(pass_context = True)
async def delete_role(ctx):
        """Удаляет роль, в котором есть вводимое слово"""
        for i in ctx.guild.roles:
                if (' '.join(ctx.message.content.split(' ')[1:])) in i.name:
                        await i.delete()


@Bot.command(pass_context = True)
async def ban(ctx, member: discord.Member):
        """Банит выбранного человека"""
        await member.guild.ban(member)


@Bot.command(pass_context = True)
async def help_me(ctx):
        """Отправляет сведения о коммандах (может в личку)"""
        emb = discord.Embed(title= "Info about commands", colour=0x39d0d6)
        emb.add_field(name= "{}help".format(prefix), value= "Show this embed")
        emb.add_field(name= "{}hello".format(prefix), value= "Answer me")
        await ctx.send(embed=emb)               # вывод на канал
        #await ctx.author.send(embed=emb)        # вывод в личку


@Bot.command()
async def hello(ctx):
	"""Бот приветствует тебя в ответ"""
	author = ctx.message.author
	await ctx.send(f"Hello {author.mention}")
	# await ctx.send(f"Hello <@{author.id}>")	# или так


@Bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
	"""Добавляет участнику роль, которая мутит на сервере"""
	mute_role=discord.utils.get(ctx.message.guild.roles, name = "Ты в муте, долбаёб")
	await member.add_roles(mute_role)


@Bot.command()
async def reaction(ctx):
	"""Добавляет эмоцию под сообщение"""
	await ctx.message.add_reaction("🤡")      # не забудь вставить эмодзи



token=os.environ.get('BOT_TOKEN')	# для сервера, чтобы никто не видел токен
Bot.run(str(token))

#Bot.run(open('token.txt','r').readline())	# чтение токена из файла
