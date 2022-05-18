from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import os


#token =  os.getenv('TOKEN')
#print(os.getenv('TOKEN'))
if not os.getenv('TOKEN'):
    token = "5372206660:AAHDj9nhx9wodD9qcBDwVMndCAHzLjSNrho"
else: token = os.getenv('TOKEN')


bot = Bot(token=token)
dp = Dispatcher(bot)