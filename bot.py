import os
import asyncio
from itertools import cycle

import discord
from discord.ext import tasks,commands
from discord.ext.commands import Bot


ban_msg = ["qwe","123"]
status = ['Msg1','Msg2','Msg3']
rainbow = ['0xd40404',      # красный
           '0xd85017',      # оранжевый
           '0xe7ca0d',      # жёлтый
           '0x1cc20a',      # зелёный
           '0x0aaec2',      # голубой
           '0x2a2dc9',      # синий
           '0xc92ab9',      # фиолетовый
           ]


prefix = '!'
Bot=commands.Bot(command_prefix=prefix)

# Удаляет команду
#Bot.remove_command('help')


# при долгой работе выдаёт ошибку "429 too many requests"
# Функция меняет цвет роли каждые 1 секунду
@tasks.loop()
async def change_color(colors, this_color, role):
        next_color = next(colors)             # берём след цвет
        this_color.value = int(next_color,16) # надо перевести цвет из 16 в 10 систему счислений
        # не можем вставить просто цвет, нужно вставить класс Colour
        await role.edit(colour = this_color)
        await asyncio.sleep(1)


# при долгой работе выдаёт ошибку "429 too many requests"
# Функция заменяет игровой статус бота каждые 1 сек
@tasks.loop()
async def change(msgs):
        current_status = next(msgs)     # выбираем след статус
        await Bot.change_presence(activity=discord.Game(name=current_status))  # "играет в ..."
        # не рекомендую ставить меньше 4, начинает тупить и виснуть
        await asyncio.sleep(4)



# Говорит о начале работы бота
@Bot.event
async def on_ready():
        print("Бот онлайн!")


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
        role = discord.utils.get(member.guild.roles, name = "Всякий сброд")
        await member.add_roles(role)


# Выдача роли по реакции
@Bot.event
async def on_raw_reaction_add(payload):
        POST_ID = 674874182483443722    # ID сообщения, где ставятся реакции
        circus = {
        '🐯':674857578932731925,  # тигр : id роли №1
        '🐉':674857717269135361,  # дракон : id роли №2
        '🤡':674857774215200789,  # клоун : id роли №3
        '🤖':674857894306512908,  # машина : id роли №4
        }
        if payload.message_id == POST_ID:
                
                try:
                        channel = Bot.get_channel(payload.channel_id) # канал, где было поставлена реакция (для нахождения объекта "cообщение")
                        message = await channel.fetch_message(payload.message_id) # получаем объект "сообщение" (для нахождения объекта "член")
                        member = discord.utils.get(message.guild.members, id=payload.user_id) # получаем объект "член", который поставил реакци
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
        '🐯':674857578932731925,  # тигр : id роли №1
        '🐉':674857717269135361,  # дракон : id роли №2
        '🤡':674857774215200789,  # клоун : id роли №3
        '🤖':674857894306512908,  # машина : id роли №4
        }
        if payload.message_id == POST_ID:
                
                try:
                        if (str(payload.emoji) in circus.keys()):
                                channel = Bot.get_channel(payload.channel_id)
                                message = await channel.fetch_message(payload.message_id) # получаем объект "сообщение"
                                member = discord.utils.get(message.guild.members, id=payload.user_id) # получаем объект "пользователь", который поставил реакцию
                                role = discord.utils.get(message.guild.roles, id=int(circus[str(payload.emoji)])) # объект выбранной роли (если есть)
                                await member.remove_roles(role)
                                print('[SUCCESS] Role {1.name} has been remove for user {0.display_name}'.format(member, role))
                                
                except KeyError as e:
                        print('[ERROR] KeyError, no role found for ' + str(payload.emoji))
                except Exception as e:
                        print(repr(e))



@Bot.command(pass_context = True)
async def info(ctx):
        """Выдаёт некую информацию"""
        emb = discord.Embed(title="Title", color=0x39d0d6)
        emb.add_field(name="Name", value="Value")
        emb.set_thumbnail(url=ctx.guild.icon_url)
        emb.set_author(name="Author", url=ctx.guild.icon_url)
        emb.set_footer(text="Footer", icon_url=ctx.guild.icon_url)
        await ctx.send(embed=emb)


@Bot.command(pass_context = True)
async def help_me(ctx):
        """Отправляет сведения о некоторых коммандах (может в личку)"""
        emb = discord.Embed(title= "Info about commands", colour=0x39d0d6)
        emb.add_field(name= "{}help".format(prefix), value= "Show this embed")
        emb.add_field(name= "{}hello".format(prefix), value= "Answer me")
        await ctx.send(embed=emb)               # вывод на канал
        #await ctx.author.send(embed=emb)        # вывод в личку


@Bot.command(pass_context = True)
async def create_role(ctx):
        """Создаёт новую роль"""
        new_name = ' '.join(ctx.message.content.split(' ')[1:]) # выделяет из сообщения название роли
        new_role = await ctx.guild.create_role()
        await new_role.edit(name=new_name, reason="А вот захотел")


@Bot.command(pass_context = True)
async def delete_role(ctx):
        """Удаляет роль, в котором есть сочитание слов"""
        for i in ctx.guild.roles:
                if (' '.join(ctx.message.content.split(' ')[1:])) in i.name:
                        await i.delete()


@Bot.command()
@commands.has_permissions(administrator=True)
async def kick(ctx,member:discord.Member):
        """Кикает указанного члена сервера"""
        await member.kick()


@Bot.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member):
        """Банит выбранного человека"""
        await member.guild.ban(member)
        await ctx.send(f'Unban user {member.mention}')


@Bot.command(pass_context = True)
@commands.has_permissions(administrator=True)
async def unban(ctx, member):
        """Разбанивает выбранного человека"""
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
                if str(ban_entry.user) == member:
                        user = ban_entry.user
                        await ctx.guild.unban(user)
                        await ctx.send(f'Unban user {user.mention}')
                        return
        await ctx.send(f"Didn't find {member}")


@Bot.command()
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member):
        """Добавляет участнику роль, которая мутит на сервере"""
        mute_role=discord.utils.get(ctx.message.guild.roles, name = "Ты в муте, долбаёб")
        await member.add_roles(mute_role)


# выводит сообщение, если команда mute выдаёт ошибку
@mute.error 
async def mute_error(ctx, error):
        '''
        commands.MissingRequiredArgument - отсутствие аргумента
        commands.MissingPermissions - отсутствие нужных прав
        commands.CommandNotFound - отсутствие команды
        '''
        if isinstance(error,commands.MissingRequiredArgument):
                await ctx.send(f'{ctx.author.name}, вы не указали кого замутить!')


@Bot.command()
async def hello(ctx):
        """Бот приветствует тебя в ответ"""
        author = ctx.message.author
        await ctx.send(f"Hello {author.mention}")
        # await ctx.send(f"Hello <@{author.id}>")       # или так


@Bot.command()
async def reaction(ctx):
        """Добавляет эмоцию под сообщение"""
        await ctx.message.add_reaction("🤡")


@Bot.command()
async def clear(ctx, amount = 1):
        """Удаляет N кол-во последних сообщений"""
        await ctx.channel.purge (limit = amount)


@Bot.command()
async def rainbow(ctx):
        """Меняет цвет роли "Воть" """
        await Bot.wait_until_ready()
        colors = cycle(colors_of_rainbow)
        role_id = 674646053110415371        # id роли
        role = ctx.guild.get_role(role_id)  # сама роль, у которой меняется цвет
        this_color = role.Colour            # создание класса Colour
        old_color = role.Сolour
        change_color.start(colors, this_color, role)
        await asyncio.sleep(60)
        change_color.stop()
        await role.edit(colour = old_color) # возвращает роли изначальный цвет


@Bot.command()
async def play(ctx):
        """ Меняет статус бота"""
        await Bot.wait_until_ready()
        msgs = cycle(status)
        change.start(msgs)
        await asyncio.sleep(60)
        change.stop()
        await Bot.change_presence(activity=None)    # устанавливает активность равной "None"


token=os.environ.get('BOT_TOKEN')   # для сервера, чтобы никто не видел токен
Bot.run(str(token))

#Bot.run(open('token.txt','r').readline())  # чтение токена из файла
