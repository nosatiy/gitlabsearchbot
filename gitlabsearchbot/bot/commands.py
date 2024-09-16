from aiogram import types, Router, F
from aiogram.filters.command import Command, CommandObject
from logging import getLogger

from settings import settings
from bot.keyboards import get_keyboard
from bot.search import search
from gitlab.parser import git_parser


commands_router = Router()


logger = getLogger()


@commands_router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


@commands_router.message(Command("add_user"))
async def cmd_add_user(
    message: types.Message,
    command: CommandObject,
    ):
    if message.from_user.username not in settings.admin_users:
        await message.answer('У тебя нет прав, шалунишка!')
        return
    try:
        add_id = command.args.split(' ')[0]
    except:
        await message.answer('Что-то ты не то передал')
        return
    if add_id in settings.approved_users:
        await message.answer('Юзер уже добавлен')
        return
    settings.approved_users.add(add_id)
    await message.answer("User added!")


@commands_router.message(F.text)
async def go_away(message: types.Message):
    if not git_parser.projects:
        await message.answer("Проекты пока не загруженны")
        return
    try:
        await message.answer(await search(message.text), reply_markup=get_keyboard(message))
    except Exception as error:
        logger.warning(error)
        await message.answer("Слишком много данных")

