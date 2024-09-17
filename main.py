from aiogram import Dispatcher, Bot
import config
import handlers

bot = Bot(token = config.TOKEN)
dp = Dispatcher()

dp.include_router(handlers.router)

if __name__ == '__main__':
    dp.run_polling(bot)