import telegram
from discord.ext import commands

from data import db_session
from data.channels import Channels
from data.config import D_TOKEN, T_TOKEN, chat_id

"""This bot take messages from selected channels and send messages from them to telegram"""

d_bot = commands.Bot(command_prefix='!')  # Discord bot
t_bot = telegram.Bot(T_TOKEN)  # Telegram bot


def main():
    """Function initializes db and runs bot"""
    db_session.global_init('db/chats.db')
    global db_sess
    db_sess = db_session.create_session()
    chats = db_sess.query(Channels)
    print('Selected chats:')
    for i in chats:
        print(i.chan_name, i.chan_id)
    d_bot.run(D_TOKEN)


def send(message):
    """Function sends message to telegram channel"""
    t_bot.send_message(chat_id, message)


@d_bot.event
async def on_ready():
    """Shows us connected Discord servers"""
    print(f'{d_bot.user} has connected to Discord!')
    for guild in d_bot.guilds:
        print(
            f'{d_bot.user} connected to chats:\n'
            f'{guild.name}(id: {guild.id})')


# @d_bot.command()
# async def help(ctx):
#    ctx.send('Команды\n\tl!set <канал>, чтобы бот просматривал этот канал'
#             '\nl!del <канал>, чтобы бот перестал просматривать этот канал')


@d_bot.event
async def on_message(message):
    """Function watch for messages in selected channel and send ones to telegram"""
    chats = db_sess.query(Channels).filter(Channels.chan_id == message.channel.id).all()
    if message.author != d_bot.user and chats:
        send(message.content)
    await d_bot.process_commands(message)


@d_bot.command(name='del')
async def del_bot(ctx, channel):
    """Function deletes channels from watched list"""
    try:
        chan = db_sess.query(Channels).filter(Channels.chan_id == int(channel[2:-1])).first()
        if not chan:
            await ctx.send('Чат не найден')
            raise ValueError
        db_sess.delete(chan)
        db_sess.commit()
        await ctx.send('Канал успешно убран')
    except Exception as e:
        await ctx.send('Использование: L!del <канал> (с решёткой в начале)')
        print(e)


@d_bot.command(name='set')
async def set_bot(ctx, channel):
    """Function adds channel to a watched list"""
    try:
        chan = Channels(
            chan_id=channel[2:-1],
            chan_name=channel,
            server_id=ctx.guild.id
        )
        some = db_sess.query(Channels).filter(Channels.chan_id == chan.chan_id).all()
        if some:
            await ctx.send('Такой канал уже добавлен')
            return
        db_sess.add(chan)
        db_sess.commit()
        await ctx.send('Канал успешно сохранён')
    except Exception as e:
        await ctx.send('Использование: L!set <канал> (с решёткой в начале)')
        print(e)


@d_bot.command('list')
async def chan_list(ctx):
    """Function shows list of connected channels on server"""
    try:
        chan = db_sess.query(Channels.chan_name).filter(Channels.server_id == ctx.guild.id).all()
        if not chan:
            await ctx.send('На этом сервере нет отслеживаемых чатов')
        guilds = '\n'.join(list(map(lambda x: x[0], chan)))
        text = f'Отслеживаемые чаты на этом сервере:\n{guilds}'
        await ctx.send(text)
    except Exception as e:
        await ctx.send('Использование: L!list')
        print(e)


if __name__ == '__main__':
    main()
