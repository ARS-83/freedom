from context.models import Service, Setting, User , Likes, Report, Details
from context.database import AsyncSessionLocal
from config import ADMIN_IDS
from sqlalchemy import select, func, case, desc,distinct
from sqlalchemy.orm import selectinload



async def get_best_btn_object():
    async with AsyncSessionLocal() as session:

        stmt = (
            select(
                User,
                func.count(distinct(Likes.id)).label("likes_count"),
                func.count(distinct(Service.id)).label("services_count"),
            )
            .outerjoin(Service, Service.created_by_user_id == User.user_id)
            .outerjoin(
                Likes,
                (Likes.service_id == Service.id) & (Likes.is_like == True)
            )
            .group_by(User.id)
            .order_by(
                func.count(distinct(Likes.id)).desc(),      # اول تعداد لایک
                func.count(distinct(Service.id)).desc(),    # بعد تعداد سرویس
            )
            .limit(5)
        )

        result = await session.execute(stmt)
        return result.all()

async def add_user_if_exists(user_data):
    
    async with AsyncSessionLocal() as session:
        user = await session.execute(
            User.__table__.select().where(User.user_id == user_data.id)
        )
        if not user.scalar():
            new_user = User(user_id=user_data.id, username=user_data.username, name=user_data.first_name, last_name=user_data.last_name)
            session.add(new_user)
            await session.commit()

async def update_user_config_count(user_id):
    async with AsyncSessionLocal() as session:
        user = await session.scalar(select(User).where(User.user_id == user_id))
        user.config_count +=1
        await session.commit()
        return user.config_count
async def get_user_step(user_id):
    async with AsyncSessionLocal() as session:

        stmt = select(User).where(User.user_id == user_id)

        user = await session.execute(stmt)
        return user.scalar_one_or_none().step


async def update_user_step(user_id, step='home'):
    async with AsyncSessionLocal() as session:
        await session.execute(
            User.__table__.update().where(User.user_id == user_id).values(step=step)
        )
        await session.commit()


async def get_user_wallet(user_id):
    async with AsyncSessionLocal() as session:
        user = await session.execute(
            User.__table__.select().where(User.user_id == user_id)
        )
        return user.fetchone().wallet

async def update_user_wallet(user_id, amount):
    async with AsyncSessionLocal() as session:
        new_wallet = amount
        await session.execute(
            User.__table__.update().where(User.user_id == user_id).values(wallet=new_wallet)
        )
        await session.commit()


async def add_user_wallet(user_id, amount):
    async with AsyncSessionLocal() as session:
        user = await session.execute(
            User.__table__.select().where(User.user_id == user_id)
        )
        current_wallet = user.fetchone().wallet
        new_wallet = current_wallet + amount
        await session.execute(
            User.__table__.update().where(User.user_id == user_id).values(wallet=new_wallet)
        )
        await session.commit() 

async def get_all_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            User.__table__.select()
        )
        return result.fetchall()
    
async def get_user_count():
    async with AsyncSessionLocal() as session:
        stmt = select(func.count(User.user_id)).select_from(User)
        result = await session.execute(stmt)
        return result.scalar()



async def get_user_by_id(user_id):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            User.__table__.select().where(User.user_id == user_id)
        )
        return result.fetchone()