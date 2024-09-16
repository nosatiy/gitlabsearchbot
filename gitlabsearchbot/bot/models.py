from pydantic import BaseModel
from aiogram.filters.callback_data import CallbackData


class ObjectData(CallbackData, prefix="obj_data"):
    target_string: str
    action: str