from aiogram import types, F, Router
from aiogram.types import BufferedInputFile
from bot.models import ObjectData
from bot.search import search
from bot.keyboards import get_keyboard
from gitlab.parser import git_parser
from logging import getLogger


callbacks_router = Router()

logger = getLogger()


@callbacks_router.callback_query(ObjectData.filter(F.action == "cb_ignore_reg"))
async def ignore_registry(callback: types.CallbackQuery, callback_data: ObjectData):
    if not git_parser.projects:
        await callback.answer("Проекты пока не загруженны", show_alert=True)
        return
    try:
        await callback.message.edit_text(
            text=await search(
                target_text=callback_data.target_string,
                ignore_registry=True
                )
            )
    except Exception as error:
        logger.error(error)
        await callback.answer("Слишком много данных", show_alert=True)
        await callback.message.edit_reply_markup()
