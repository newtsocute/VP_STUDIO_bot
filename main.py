import logging
from aiogram import Bot, Dispatcher, types
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.fsm.storage.memory import MemoryStorage
from config import TOKEN, MINIAPP_URL
from handlers import routers
#from database import setup_database

# Логирование
logging.basicConfig(level=logging.INFO)

# бот и диспетчер
session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
dp = Dispatcher(storage=MemoryStorage())

async def set_menu_button():
    await bot.set_chat_menu_button(
        menu_button=types.MenuButtonWebApp(
            text="Онлайн запись",
            web_app=types.WebAppInfo(url=MINIAPP_URL)
        )
    )

for router in routers:
    dp.include_router(router)


async def main():
    #await setup_database()
    await set_menu_button()
    await dp.start_polling(bot, skip_updates=True)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
