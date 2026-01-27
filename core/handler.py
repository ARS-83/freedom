from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, ReplyKeyboardMarkup
from .btns import *
from config import ADMIN_IDS , CHANEL_ID
from context.services import config_service, user_service
from .config_manager import get_config


@Client.on_message(filters.command("start"))
async def start(c:Client, m:Message):
    await user_service.add_user_if_exists(m.from_user)
    await m.reply(f"""**  سلام به ربات ازاد خوش آمدید 📃

🫳🏻 این ربات به قصد اشتراک گذاری سرویس رایگان برای اتصال به اینترنت و مقابله با وی پی ان فروشان دو هزاری در شرایط سخت بوده و مقصود دیگری ندارد

🤝 لطفا اگه دانشی در این زمینه دارید با دیگران به اشتراک بذارید

🐝 (صرفا برای اطلاع رسانی) تنها چنل رسمی ربات آزاد: @{CHANEL_ID}
**
""", reply_markup=await main_key(m.from_user.id))
    await user_service.update_user_step(m.from_user.id, "home")


@Client.on_message(filters.regex("🚀 دریافت کانفیگ"))
async def configs_handler(c:Client, m:Message):
    await m.reply("""**🕊 تو نباید اینجا میبودی ولی شاید لیست زیر به کارت بیاد

👑 جمعی از کانفیگ های دیگران و ما که به صورت رایگان قرار دادیم که میتونید دریافت کنید با روش ها واموزش ها

🔥 شما هم میتوانید با افزودن کانفیگ و یا نظر به سرویس دیگران این زنجیره رو محکم تر کنید**
                  """, reply_markup=InlineKeyboardMarkup(get_type_btn_object))


@Client.on_message(filters.regex("🤝 افزودن کانفیگ"))
async def add_configs_handler(c:Client, m:Message):
        await user_service.update_user_step(m.from_user.id, "addconfig")
        await m.reply("""**
🕊 گاهی اخلاق نه در کارهای بزرگ،
بلکه در همین تصمیم‌های کوچک معنا پیدا می‌کند:
این‌که می‌توانی آزار بدهی و نمی‌دهی.
می‌توانی سنگین‌ترش کنی و نمی‌کنی.
**می‌توانی انسان بمانی.

🪽 مچکرم که به این جمع میپینودی
...از طریق دکمه‌های زیر میتوانید سرویس اضافه کنید
""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('ساخت کانفیگ', callback_data='CREATECONFIG')]]))



@Client.on_message(filters.regex("☎️ ارتباط با من"))
async def callsup_handler(c:Client, m:Message):
        await user_service.update_user_step(m.from_user.id, "callsup")
        await m.reply("""**
🕊 عزیز دل اگه پیشنهادی , حرفی داری میتونی از این طریق ارسال کنی 

**
""",reply_markup=ReplyKeyboardMarkup([['انصراف']], resize_keyboard=True))


@Client.on_message(filters.regex('انصراف'))
async def cancel_handler(c:Client, m:Message):
    await user_service.update_user_step(m.from_user.id, "home")

    await m.reply(f"""**  سلام به ربات ازاد خوش آمدید 📃

🫳🏻 این ربات به قصد اشتراک گذاری سرویس رایگان برای اتصال به اینترنت و مقابله با وی پی ان فروشان دو هزاری در شرایط سخت بوده و مقصود دیگری ندارد
                  
🤝 لطفا اگه دانشی در این زمینه دارید با دیگران به اشتراک بذارید  

🐝 (صرفا برای اطلاع رسانی) تنها چنل رسمی ربات آزاد: @{CHANEL_ID}
**
""", reply_markup=await main_key(m.from_user.id))

@Client.on_message(filters.regex("مدیریت") & filters.user(ADMIN_IDS))
async def setting_handler(c:Client, m:Message):
    await m.reply("""تنظیمات ادمین

 به بخش مدیریت ادمین خوش آمدید.
""", reply_markup=ADMIN_BTNS)


@Client.on_callback_query()
async def callback(c:Client, q:CallbackQuery):
    if "getlistc_" in q.data:
        provider = q.data.split("_")[1]
        await get_config_list_btn(c, q, provider, 15, 0)

    if "next_" in q.data:
        data = q.data.split("_")
        provider = q.data.split("_")[1]
        limit = int(data[2])
        skip = int(data[3])
        page = int(data[4])
        await get_config_list_btn(c, q, provider, limit, skip=skip, page=page)

    if 'back_' in q.data:
        data = q.data.split("_")
        provider = q.data.split("_")[1]
        limit = int(data[2])
        skip = int(data[3])
        page = int(data[4])
        await get_config_list_btn(c, q, provider, limit, skip=skip, page=page)


    if 'likeservice_' in q.data:
        service_id = int(q.data.split("_")[1])
        res = await config_service.like_dislike(service_id, q.from_user.id, like=True)
        if res:
            await q.answer("با موفقیت لایک شد :)", show_alert=True)
        else:
            await q.answer("قبلا نظرتو دادی یا مشکلی پیش اومده", True)
            return
        btns = await get_service_btn(service_id)
        await q.edit_message_reply_markup(reply_markup=btns)


    if 'dislike_' in q.data:
        service_id = int(q.data.split("_")[1])
        res = await config_service.like_dislike(service_id, q.from_user.id, dislike=True)
        if res:
            await q.answer("چند نفر دیگه بزنن پاکش میکنم :)", show_alert=True)
        else:
            await q.answer("قبلا نظرتو دادی یا مشکلی پیش اومده", True)
            return
        btns = await get_service_btn(service_id)
        await q.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btns))


    if 'report_' in q.data:
        service_id = int(q.data.split("_")[1])
        res, service= await config_service.report_service(service_id, q.from_user.id)
        if res:
            await q.answer('گزارش ثبت شد ✅')
            await q.message.delete()
            for admin in ADMIN_IDS:
                await c.send_message(f'''ادمین گرامی کاربر : {q.from_user.id}
کاربر @{service.creator.username} - <code>{service.creator.name}</code> - {service.creator.user_id}گزارش داده است
لطفا بررسی کنیید از طریق دکمه زیر
                ''',reply_markup=InlineKeyboardMarkup([InlineKeyboardButton("دریافت کانفیگ", callback_data=f"getconfig_{service_id}")]))


    if 'getconfig_' in q.data:
       
        await q.answer("دریافت جزییات ...")
        await q.edit_message_text("""📌 مواردی که باید در نظر بگیرید  :

⚠️ درصورتی محتوایی بجز کانفیگ برای اتصال دریافت کرید حتما گزارش کنید 
👮🏻‍♀️ ترجیحا کلاینت رو از جای مورد اطمینان دانلود و نصب کنید افراد سود جو از این موقعیت ها هم برای خوردن خون شما استفاده میکنند 

                              """)

        service_id = int(q.data.split('_')[1])
        await get_config(c, q,service_id)


    if q.data == "add_config":
        await user_service.update_user_step(q.from_user.id, "addconfig")
        await q.message.reply("""**
🕊 گاهی اخلاق نه در کارهای بزرگ،
بلکه در همین تصمیم‌های کوچک معنا پیدا می‌کند:
این‌که می‌توانی آزار بدهی و نمی‌دهی.
می‌توانی سنگین‌ترش کنی و نمی‌کنی.
**می‌توانی انسان بمانی.

🪽 مچکرم که به این جمع میپینودی
...از طریق دکمه‌های زیر میتوانید سرویس اضافه کنید
""", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('ساخت کانفیگ', callback_data='CREATECONFIG')]]))

    if  q.data == 'CREATECONFIG':
        await q.edit_message_text("☄️ لطفا اینترنتی که کانفیگ روی اون جواب میده رو انتخاب کن", reply_markup=InlineKeyboardMarkup(provider_btns_object))

    if 'provdide_' in q.data:
        provider = q.data.split("_")[1]
        await q.edit_message_text("لطفا برنامه مورد نیاز رو انتخاب کنید ", reply_markup=InlineKeyboardMarkup(type_btn_object(provider)))

    if 'type_' in q.data:
        print(q.data)
        type_app = q.data.split("_")[1]
        provider = q.data.split('_')[2]
        if q.from_user.id in ADMIN_IDS:
            service_id =await config_service.add_service(provider, type_app, q.from_user.id, is_active=False, is_vip=True)
        else:
            service_id =await config_service.add_service(provider, type_app, q.from_user.id, is_active=False, is_vip=False)

        await user_service.update_user_step(q.from_user.id, "sendetails_{}".format(service_id))
        await q.message.delete()
        await q.message.reply("🙏🏼❤️ خواهشمند است از ارسال محتوایی بجز سرویس برای اتصال خود داری کنید")
        await q.message.reply('''✅ تشکر از شما لطفا پس از این متن سرویس اموزش رو قرار بدید میتونید لینک دانلود اپلیکیشن مورد نیاز رو هم قرار بدید 

🛜 پس از اتمام ارسال دکمه تایید یا در صورت انصراف دکمه انصراف رو وارد کنید 
                                ''', reply_markup=ReplyKeyboardMarkup([['✅ تایید', 'انصراف']], resize_keyboard=True))





    # Admin
    if q.from_user.id in ADMIN_IDS:
        if 'getadmin_' in q.data:
            # await q.message.delete()
            await q.answer("دریافت جزییات ...")
            await q.message.reply("""📌 مواردی که باید در نظر بگیرید  :

    ⚠️ درصورتی محتوایی بجز کانفیگ برای اتصال دریافت کرید حتما گزارش کنید 
    👮🏻‍♀️ ترجیحا کلاینت رو از جای مورد اطمینان دانلود و نصب کنید افراد سود جو از این موقعیت ها هم برای خوردن خون شما استفاده میکنند 

                                """)

            service_id = int(q.data.split('_')[1])
            await get_config(c, q,service_id)
            await q.message.reply('در صورتی که مورد تایید بود تایید را فشار داده تا در اختیار عموم قرار گیرد', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("تایید", callback_data=f"approve_{service_id}"), InlineKeyboardButton("انصراف", callback_data=f"cancel_{service_id}")]]))
        if 'approve_' in q.data:
            service_id = int(q.data.split('_')[1])
            await config_service.approve_service(service_id)
            await q.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("تایید شده",callback_data='ars')]]))

        #  maNAGE uSERS


        if q.data == "manage_users":
            users = await user_service.get_all_users()
            await q.message.reply(f"تعداد کل کاربران ثبت شده: {len(users)}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("جستجو کاربر", callback_data="search_user_by_id")]]))


        if q.data == "search_user_by_id":
            await user_service.update_user_step(q.from_user.id, "search_user_by_id")
            await q.message.reply("لطفا ایدی عددی کاربر را وارد کنید:", reply_markup=CANCEL_KEY)


        if q.data == "broadcast_message":
            await user_service.update_user_step(q.from_user.id, "broadcast_message")
            await q.message.reply("لطفا پیام همگانی را وارد کنید میتواید تصویر هم ارسال کنید:", reply_markup=CANCEL_KEY)


        if q.data == "general_settings":
            setting_btn = await general_settings_key()
            await q.message.reply("به بخش تنظیمات کلی خوش آمدید.", reply_markup=setting_btn)

        if q.data == "main_admin_menu":
                await q.edit_message_text("""تنظیمات ادمین

 به بخش مدیریت ادمین خوش آمدید.
""", reply_markup=ADMIN_BTNS)

        if q.data == "edit_channel":
            await user_service.update_user_step(q.from_user.id, "edit_channel")
            await q.message.reply("لطفا ایدی کانال را وارد کنید:", reply_markup=CANCEL_KEY)

        if q.data == "edit_support":
            await user_service.update_user_step(q.from_user.id, "edit_support")
            await q.message.reply("لطفا ایدی پشتیبانی را وارد کنید:", reply_markup=CANCEL_KEY)
        
        if q.data == 'stats_reports':
            user_count = await user_service.get_user_count()
            active_configs = await config_service.count_configs_active()
            await q.message.reply(f"👤 تعداد کل کاربران ثبت شده: {user_count}\n\n📂 تعداد کل سرویس های فعال: {active_configs}")
