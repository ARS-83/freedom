from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from .filters import not_btn
from .btns import  main_key

from context.services import config_service, user_service

from config import ADMIN_IDS

@Client.on_message(not_btn)
async def handle_steps(c:Client, m:Message):
    try:
        if m.text == "انصراف":
            await user_service.update_user_step(m.from_user.id, "home")

            await m.reply("""  سلام به ربات ما خوش آمدید 📃

            ℹ️ برای استفاده از ربات از دکمه‌های زیر استفاده کنید.

            """, reply_markup=await main_key(m.from_user.id))
            return
    except Exception as e:
        print("".format(e))
        pass
    step = await user_service.get_user_step(m.from_user.id)

    if step =='callsup':
        if m.text:
            for admin in ADMIN_IDS:
                await c.send_message(admin, f"""🕊️پیام کاربر  {m.from_user.username} - {m.from_user.first_name} - {m.from_user.id} 
{m.text}
""" )
            await user_service.update_user_step(m.from_user.id, "home")
            await m.reply("❤️ ارسال شد پیامت برامون مرسی ازت ", reply_markup=await main_key(m.from_user.id))

    if step == "broadcast_message":
        users = await user_service.get_all_users()
        success = 0
        failed = 0
        await m.reply("در حال ارسال پیام همگانی... لطفا صبر کنید ⏳", reply_markup=await main_key(m.from_user.id))
        for user in users:
            try:
                if m.photo:
                    await c.send_photo(user.user_id, m.photo.file_id, caption=m.text)
                else:
                    await c.send_message(user.user_id, m.text)
                success += 1
            except:
                failed += 1
        await m.reply(f"پیام همگانی با موفقیت ارسال شد ✅\n\nموفق: {success}\nناموفق: {failed}" , reply_markup=await main_key(m.from_user.id))
        await user_service.update_user_step(m.from_user.id, "home")

    elif step == "edit_channel":
        await config_service.update_setting_field("channel", m.text.strip())
        await m.reply("آیدی کانال با موفقیت ویرایش شد ✅", reply_markup=await main_key(m.from_user.id))
        await user_service.update_user_step(m.from_user.id, "home")
    
    elif step == "edit_support":
        await config_service.update_setting_field("support", m.text.strip())
        await m.reply("آیدی پشتیبانی با موفقیت ویرایش شد ✅", reply_markup=await main_key(m.from_user.id))
        await user_service.update_user_step(m.from_user.id, "home")

    elif 'sendetails_' in step:
        service_id = int(step.split('_')[1])
        if m.text:
            if m.text == '✅ تایید':
                await user_service.update_user_step(m.from_user.id, "home")
                await user_service.update_user_config_count(m.from_user.id)
                # send to admin service
                for admin in ADMIN_IDS:
                    try:
                        await c.send_message(admin, f""" پیام جدید در سرویس {service_id} ارسال شد

نام کاربر : {m.from_user.first_name} {m.from_user.last_name}
آیدی کاربر : {m.from_user.id}
نام کاربری : @{m.from_user.username}
                                            """, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👀 مشاهده کانفیگ", callback_data=f"getadmin_{service_id}")]]))
                        await m.reply("❤️ پیام شما ارسال شد پس از تایید در لیست قرار میگیرد",reply_markup=await main_key(m.from_user.id))
                    except:
                        pass
                
                return 
        await config_service.add_detail(service_id, m.id, m.from_user.id)
        await m.reply("🩵 پیام اضافه شد در صورت اتمام تایید رو ارسال کنید در صورتی که هنوز مجتوا برای ارسال دارید ادامه دهید")
        


