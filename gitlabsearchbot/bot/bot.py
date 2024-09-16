from aiogram import Bot, Dispatcher
import asyncio

from bot.commands import commands_router
from bot.callbacks import callbacks_router
from bot.middleware import GoAwayMiddleware
from gitlab.parser import git_parser
from settings import settings


bot = Bot(token=settings.bot_token)
dp = Dispatcher()
dp.include_router(commands_router)
dp.include_router(callbacks_router)
dp.message.middleware(GoAwayMiddleware())


@dp.startup()
async def on_startup():
    asyncio.create_task(git_parser.start())
    print('startup')
    


@dp.shutdown()
async def on_shutdown():
    await git_parser.git_api.close_session()
    print('shutdown')
