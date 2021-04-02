import telegram
from data.config import TOKEN, chat_id

bot = telegram.Bot(TOKEN)
bot.send_message(chat_id, 'message')
