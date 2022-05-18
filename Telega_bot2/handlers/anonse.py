from aiogram import types, Dispatcher
from aiogram.types import ReplyKeyboardRemove
from create_bot import dp, bot
from keyboards import kb_clients_settings, kb_clients
from Columbia_com.parser import parse
import time

#@dp.message_handler(commands=["Анонсы"])
async def command_anonse(message: types.Message):
    print("прилетело")
    #await bot.send_message(message.from_user.id, "/Настройки", reply_markup=ReplyKeyboardRemove(kb_clients))
    out = parse()
    print(out)
    for line in out:
        if line["old_price"]:
            text = f"<b>{line['title']}</b>\n\n{line['price']}\t\t\t\t\t\t<s>{line['old_price']}</s>\n\n<a href='{line['img']}' ></a> {line['link']}\n"
        else:
            text = f"<b>{line['title']}</b>\n\n{line['price']}\n\n<a href='{line['img']}' ></a> {line['link']}\n"
        await message.answer(allow_sending_without_reply=True, text=text, parse_mode="html")
        time.sleep(3)
    #await message.delete()


def register_handler_anonse(dp: Dispatcher):
    dp.register_message_handler(command_anonse, commands=["Анонсы"])
