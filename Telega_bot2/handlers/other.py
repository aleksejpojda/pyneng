from aiogram import types, Dispatcher
from create_bot import dp


#@dp.message_handler() # Пустой хэндлер должен быть (если нужен) только в конце
async def echo_send(message: types.Message):
    await message.answer(message.text) #тупо отсылает текст
    #await message.reply(message.text) # отвечает, цитируя твое сообщение
    #await bot.send_message(message.from_user.id, message.text) #отправить лично пользователю

def register_handler_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)#Можно писать такие функции вместо декораторов
    #для каждого декоратора дополнительная строка в функции