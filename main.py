from pyrogram import Client, filters
from pyrogram.types import Message
from config import API_ID, API_HASH, BOT_TOKEN, motivational_texts
from context.services import user_service
from context.models import User
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import random
import datetime

plugins = dict(root="core")

app = Client("telegram_service12", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins=plugins)


sended_today = False
async def send_good_night():
    global sended_today
    if  datetime.datetime.now().hour == 19 and sended_today == False:
        users = await user_service.get_all_users()
        for user in users:
                await app.send_message(user.user_id, f"""**  ببخشید مزاحمت شدم {user.name} خواستم بگم  

    {random.choice(motivational_texts)}

    شبت بخیر مواظب خودت باش❤️
    **

    """)
        sended_today=True
    else :
        sended_today = False



scheduler = AsyncIOScheduler()

scheduler.add_job(send_good_night, "interval", seconds=2600)
scheduler.start()
app.run()
