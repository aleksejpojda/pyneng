from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os
from aiogram.contrib.fsm_storage.memory import MemoryStorage


#chatid="@my_test_chanal_1"

#token =  os.getenv('TOKEN')
#print(os.getenv('TOKEN'))

if not os.getenv('TOKEN'):
    token = "5372206660:AAHDj9nhx9wodD9qcBDwVMndCAHzLjSNrho"
    path = "Telega_bot2"
else:
    token = os.getenv('TOKEN')
    path = "."


storage = MemoryStorage()

bot = Bot(token=token)
dp = Dispatcher(bot, storage=storage)