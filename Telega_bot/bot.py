import logging
from aiogram import Bot, Dispatcher, executor, types
import config
from filters import IsAdminFilter

logging.basicConfig(level=logging.INFO
                    )
#token = '5372206660:AAHDj9nhx9wodD9qcBDwVMndCAHzLjSNrho'
#chatId = "@my_test_chanal_1"
bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

dp.filters_factory.bind(IsAdminFilter)

@dp.message_handler(content_types=["new_chat_members"])
# не выводить сообщение о новом пользователе в чате
async def on_user_goined(message: types.Message):
    await message.delete()

@dp.message_handler(is_admin=True, commands=['ban'], commands_prefix="!/")
async def cmd_ban(message: types.Message):
    if not message.reply_to_message:
        await message.reply("Эта команда должна быть ответом на сообщение")
        return
    await message.bot.delete_message(chat_id=config.GROUP_ID, message_id=message.message_id)
    await message.bot.kick_chat_member(chat_id=config.GROUP_ID, user_id=message.from_user.id)
    await message.reply_to_message.reply("Пользователь забанен")

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

