#  Custom Filters
from pyrogram import filters, Client
from pyrogram.types import Message
from .btns import main_keys

async def not_btns(_, c:Client, m:Message):
    if m.text not in main_keys:
        return True

    return False

#  Custom Creator
not_btn = filters.create(not_btns)