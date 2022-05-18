from aiogram.utils import executor
from create_bot import dp
from handlers import client, admin, other, anonse
"""
Основной файл для запуска
"""

async def on_startup(_):
    """Выполняется при подключении бота
    добавить в executor параметр on_startup=on_startup"""
    print("Бот подключился")


anonse.register_handler_anonse(dp)
client.register_handler_clients(dp)
other.register_handler_other(dp)
#anonse.register_handler_anonse(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)


