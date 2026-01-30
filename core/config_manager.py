
from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery
from context.services import config_service
from context.models import Service, User
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
)
async def get_config(c: Client, m: Message, service_id: int):
    service = await config_service.get_service_by_id(service_id)
    for detail in service.details:
        print(service.creator)
        await c.copy_message(chat_id=m.chat.id, from_chat_id=service.creator.user_id, message_id=int(detail.message_id))

    await m.reply('🤝 ارسال محتوا این سرویس انجام شد لطفا در نظر سنجی زیر شرکت کنید برای بهبود کیفیت کار ',reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"👍🏻", callback_data=f"likeservice_{service.id}"),
                    InlineKeyboardButton(f"👎🏻", callback_data=f"dislike_{service.id}"),
                    InlineKeyboardButton("⚠️ گزارش", callback_data=f"report_{service.id}"),
                ],
            ]))



async def create_config(c: Client, m: Message, user_id: int, type_product, provider, name,  is_vip=True):...

