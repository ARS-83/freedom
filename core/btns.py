from context.services.config_service import get_setting, get_all_service, get_service
from context.services.user_service import get_best_btn_object
from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
)
from utils import external_requests
from config import ADMIN_IDS
from pyrogram import Client
from pyrogram.types import Message, CallbackQuery

from context.models import Service, Setting, User, Likes

main_keys = [
    "🚀 دریافت کانفیگ",
    "برترین ها 🪽",
    "🤝 افزودن کانفیگ",
    "☎️ ارتباط با من",
    "مدیریت",
]


provide_btns = [
    ("ایرانسل", "mtn"),
    ("همراه اول", "mci"),
    ("رایتل", "rightel"),
    ("بقیه چیزا", "other"),
    ("همه", "alls"),
]
provider_btns_object = [
    [
        InlineKeyboardButton("ایرانسل", callback_data="provdide_mtn"),
        InlineKeyboardButton("همراه اول", callback_data="provdide_mci"),
    ],
    [
        InlineKeyboardButton("رایتل", callback_data="provdide_rightel"),
        InlineKeyboardButton("بقیه چیزا", callback_data="provdide_other"),
    ],
    [
        InlineKeyboardButton("همه", callback_data="provdide_alls"),
    ],
]
get_type_btn_object = [
    [
        InlineKeyboardButton("ایرانسل", callback_data="getlistc_mtn"),
        InlineKeyboardButton("همراه اول", callback_data="getlistc_mci"),
    ],
    [
        InlineKeyboardButton("رایتل", callback_data="getlistc_rightel"),
        InlineKeyboardButton("بقیه چیزا", callback_data="getlistc_other"),
    ],
    [
        InlineKeyboardButton("همه", callback_data="getlistc_alls"),
    ],
]


def type_btn_object(provider: str):

    return [
        [
            InlineKeyboardButton("npv", callback_data="type_npv_" + provider),
            InlineKeyboardButton("v2ray", callback_data="type_v2ray_" + provider),
        ],
        [
            InlineKeyboardButton(
                "netmod - http injector", callback_data="type_netmod_" + provider
            ),
            InlineKeyboardButton("other vpns", callback_data="type_v2ray_" + provider),
        ],
        [
            InlineKeyboardButton(
                "telegram proxy", callback_data="type_proxy_" + provider
            ),
        ],
    ]


CANCEL_KEY = ReplyKeyboardMarkup([["انصراف"]], resize_keyboard=True)

ADMIN_BTNS = InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("مدیریت کاربران 📃", callback_data="manage_users")],
        [InlineKeyboardButton("پیام همگانی 📢", callback_data="broadcast_message")],
        [InlineKeyboardButton("افزودن کانفیگ", callback_data="add_config")],
        [InlineKeyboardButton("آمار و گزارشات 📊", callback_data="stats_reports")],
        [InlineKeyboardButton("تنظیمات کلی ⚙️", callback_data="general_settings")],
    ],
)

main_admin_key = InlineKeyboardButton(
    "بازگشت به منوی اصلی 🔙", callback_data="main_admin_menu"
)


async def main_key(user_id: int = 0):
    btns = ReplyKeyboardMarkup(
        [
            ["🚀 دریافت کانفیگ", "برترین ها 🪽"],
            ["🤝 افزودن کانفیگ", "☎️ ارتباط با من"],
        ],
        resize_keyboard=True,
    )
    if user_id in ADMIN_IDS:
        btns.keyboard.append(["مدیریت"])

    return btns


async def get_service_btn(service_id: int):
    btns = []
    res = await get_service(service_id)
    if res:
        print(res)
        service, likes, dislikes = res
        btns = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(f"👍🏻", callback_data=f"ars"),
                    InlineKeyboardButton(f"👎🏻", callback_data=f"ars"),
                    InlineKeyboardButton(
                        "⚠️ گزارش", callback_data=f"report_{service.id}"
                    ),
                ],
            ]
        )
    return btns


async def get_best_btn_object():
    btns = []
    top_users = await get_best_btn_object()
    for user, likes, services in top_users:
        btns.append(
            [
                InlineKeyboardButton(f"👤{user.name} - 👍{likes} - 🌐{services}", callback_data=f"ars"),
            ]
        )
    return btns


async def general_settings_key():
    
    setting = await get_setting()
    btns = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    f"{setting.channel}", callback_data="edit_channel"
                ),
                InlineKeyboardButton(f"چنل قفل", callback_data="none"),
            ],
            [
                InlineKeyboardButton(
                    f"{setting.support}", callback_data="edit_support"
                ),
                InlineKeyboardButton(f"پشتیبانی", callback_data="none"),
            ],
        ]
    )
    return btns


async def get_config_list_btn(
    app: Client, message: CallbackQuery, provider: str = None, limit=15, skip=0, page=0
):
    btns = []
    service: Service = ""
    services = await get_all_service(limit, skip, provider=provider)
    for service, likes, dislikes in services:
        if service.is_vip:
            btns.append(
                [
                    InlineKeyboardButton(
                        f"{service.creator.name} - {service.type_product} - VIP",
                        callback_data=f"getconfig_{service.id}",
                    ),
                    InlineKeyboardButton(f"👍🏻{likes}", callback_data=f"ars"),
                ]
            )

        else:
            btns.append(
                [
                    InlineKeyboardButton(
                        f"{service.creator.name} - {service.type_product} - VIP",
                        callback_data=f"getconfig_{service.id}",
                    ),
                    InlineKeyboardButton(f"👍🏻{likes}", callback_data=f"ars"),
                ]
            )
    if page == 0:
        if services and len(services) == limit:
            btns.append(
                [
                    InlineKeyboardButton(
                        "بعدی",
                        callback_data=f"next_{provider}_{limit}_{(page+1) * limit}_{page+1}",
                    )
                ]
            )

    else:
        if services and len(services) == limit:
            btns.append(
                [ InlineKeyboardButton(
                        "قبلی", callback_data=f"back_{provider}_{limit}_{(page - 1)}_{page - 1}"
                    ),
                    InlineKeyboardButton(
                        "بعدی",
                        callback_data=f"next_{provider}_{limit}_{(page+1) * limit}_{page+1}",
                    ),
                   
                ]
            )
        else:
            btns.append(
                [
                    InlineKeyboardButton(
                        "قبلی", callback_data=f"back_{provider}_{limit}_{(page - 1)}_{page - 1}"
                    )
                ]
            )
    print(btns)
    if not btns:
        return await message.answer("🥲 سرویسی یافت نشد ")

    await message.edit_message_text(
        """لیست سرویس های برتر 👇

برای مشاهده هر سرویس بر روی آن بزنید 🫳🏻

""",
        reply_markup=InlineKeyboardMarkup(btns),
    )
    return True


def get_provide_btns(key):
    for i in range(len(provide_btns)):
        if provide_btns[i][1] == key:
            return provide_btns[i][0]
