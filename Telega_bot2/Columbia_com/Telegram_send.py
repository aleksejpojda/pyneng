from telegram import Update
from telegram import Bot
from telegram import ParseMode
from telegram.ext import CommandHandler
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
import time



token = '5372206660:AAHDj9nhx9wodD9qcBDwVMndCAHzLjSNrho'
chatId = "@my_test_chanal_1"
bot = Bot(
        token = token,
    )

def generate_text(out_list, message):
    for line in out_list:
        text = f"<b>{line['title']}</b>\n\n{line['price']}\n\n<a href='{line['img']}' ></a> {line['link']}\n\n{message}"
        send_data(bot, text)
        time.sleep(3) # если слать чаще - банят
        print(f"Отправлено сообщений {out_list.index(line)+1} из {len(out_list)}...")

def send_data(bot: Bot, text):
    bot.send_message(chatId, text, parse_mode="HTML")



def main():
    bot = Bot(token = token,)
    updater = Updater(bot=bot)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()