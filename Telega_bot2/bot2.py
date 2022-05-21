from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other, anonse
from database import sqlite_db
from files import list_dir_sites

"""
Основной файл для запуска
"""


async def on_startup(_):
    """Выполняется при подключении бота
    добавить в executor параметр on_startup=on_startup"""
    print("Бот подключился")
    sqlite_db.sql_start() #подключимся или создадим базу данных
    list_dir_sites()

admin.register_handlers_new_message(dp)
anonse.register_handler_anonse(dp)
client.register_handler_clients(dp)
other.register_handler_other(dp) #Этот должен быть последним
#admin.register_handlers_new_message(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


