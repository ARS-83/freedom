from context.models import Service, Setting, User , Likes, Report, Details
from context.database import AsyncSessionLocal
from sqlalchemy import select, func, case, desc,asc
from sqlalchemy.orm import selectinload


async def like_dislike(service_id, user_id, like=False, dislike=False):
     async with AsyncSessionLocal() as session:
          stmt = select(Likes).where(Likes.user_id == user_id, Likes.service_id == service_id)
          like_dislike = await session.execute(stmt)
          like_dislike = like_dislike.scalar_one_or_none()
          if like_dislike:
               return False

          new_like = Likes()
          new_like.service_id = service_id
          new_like.user_id= user_id
          new_like.is_like = like
          new_like.is_dislike = dislike
          session.add(new_like)
          await session.commit()
          return new_like


async def count_configs_active():
    async with AsyncSessionLocal() as session:
        return await session.scalar(
            select(func.count(Service.id)).where(Service.is_active.is_(True))
        )



async def approve_service(service_id):
    async with AsyncSessionLocal() as session:
        stmt = select(Service).where(Service.id == service_id)
        service = await session.execute(stmt)
        service = service.scalar_one_or_none()
        service.is_active = True
        await session.commit()
        return service

async def add_service(provider, type_app, user_id, is_active=True, is_vip=False):
    async with AsyncSessionLocal() as session:
        new_service = Service(providers=provider, type_product=type_app, created_by_user_id=user_id, is_vip=is_vip, is_active=is_active)
        session.add(new_service)
        await session.commit()
        return new_service.id

async def report_service(service_id, user_id):
     async with AsyncSessionLocal() as session:
        service = await get_service_by_id(service_id)
        report = Report()
        report.user_id = user_id
        report.reported_user = service.creator.user_id
        session.add(report)
        await session.commit()
        return report, service

async def add_detail(service_id, message_id,user_id):
    async with AsyncSessionLocal() as session:
        new_detail = Details(service_id=service_id, message_id=message_id, user_id=user_id, type_message='text')
        session.add(new_detail)
        await session.commit()
        return new_detail

async def get_service_by_id(service_id: int):
    async with AsyncSessionLocal() as session:
        stmt = (
            select(Service)
            .options(
                selectinload(Service.details),  

            ).options(selectinload(Service.creator))
            .where(Service.id == service_id)
        )
        result = await session.execute(stmt)
        return result.scalar_one_or_none()


async def get_service(service_id: int):
    async with AsyncSessionLocal() as session:

        likes_count = func.sum(
            case((Likes.is_like.is_(True), 1), else_=0)
        ).label("likes")

        dislikes_count = func.sum(
            case((Likes.is_dislike.is_(True), 1), else_=0)
        ).label("dislikes")

        stmt = (
            select(Service, func.coalesce(likes_count, 0), func.coalesce(dislikes_count, 0))
            .outerjoin(Likes, Likes.service_id == Service.id)
            .where(Service.id == service_id, Service.is_active.is_(True))
            .group_by(Service.id)
        )

        result = await session.execute(stmt)
        row = result.first()

        if not row:
            return None

        service, likes, dislikes = row
        return service, likes, dislikes


async def get_all_service(limit:int=15, skiped:int=0, provider=''):
    async with AsyncSessionLocal() as session:

        likes_count = func.sum(
            case((Likes.is_like == True, 1), else_=0)
        ).label("likes_count")

        dislikes_count = func.sum(
            case((Likes.is_dislike == True, 1), else_=0)
        ).label("dislikes_count")

        stmt = (
            select(
                Service,
                func.coalesce(likes_count, 0),
                func.coalesce(dislikes_count, 0),
            )
            .outerjoin(Likes, Likes.service_id == Service.id)
            .options(selectinload(Service.creator))
            .where(Service.is_active == True, Service.providers.contains(provider))
            .group_by(Service.id)
            .order_by(
                desc(func.coalesce(likes_count, 0) ),
                asc(func.coalesce(dislikes_count, 0)),
                desc(Service.is_vip),
            ).limit(limit).offset(skiped)
        )

        result = await session.execute(stmt)

        return result.all()
        return [
            {
                "service": service,
                "likes_count": likes,
                "dislikes_count": dislikes,
            }
            for service, likes, dislikes in rows
        ]
async def update_setting(name, value):
        async with AsyncSessionLocal() as session:
            setting = await session.get(Setting, 1)
            setattr(setting, name, value)
            await session.commit()
            await session.refresh(setting)
            return setting


async def get_setting():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            Setting.__table__.select()
        )
        return result.fetchone() if result else None


# async def get_products(state=None, **kwargs):

#     async with AsyncSessionLocal() as session:
#         if state is None:
#              result = await session.execute(
#                 Product.__table__.select()
#             )
#              return result.fetchall()
#         result = await session.execute(
#             Product.__table__.select().where(Product.type_product == state and Product.is_active==True)
#         )
#         return result.fetchall()


# async def get_all_products():
#     async with AsyncSessionLocal() as session:
#         result = await session.execute(
#             Product.__table__.select()
#         )
#         return result.fetchall()

# async def get_product_by_id(product_id):
#     async with AsyncSessionLocal() as session:
#         result = await session.execute(
#             Product.__table__.select().where(Product.id == product_id)
#         )
#         return result.fetchone()
    
# async def create_order(product_id, username, amount, status, type_order, user_id):
#     async with AsyncSessionLocal() as session:
#         new_order = Order(
#             user_id=user_id,
#             item=product_id,
#             user_name=username,
#             amount=amount,
#             status=status,
#             type_order=type_order
#         )
#         session.add(new_order)
#         await session.commit()
#         return new_order



# async def get_order_by_id(order_id):
#     async with AsyncSessionLocal() as session:
#         result = await session.execute(
#             Order.__table__.select().where(Order.id == order_id)
#         )
#         return result.fetchone()

# async def update_order_status(order_id, new_status):
#     async with AsyncSessionLocal() as session:
#         order = await session.get(
#             Order, order_id)    
#         order.status = new_status
#         await session.commit()
#         await session.refresh(order)
#         return order



# async def create_product(name, price, type_product):
#     async with AsyncSessionLocal() as session:
#         new_product = Product(
#             name=name,
#             price=price,
#             type_product=type_product
#         )
#         session.add(new_product)
#         await session.commit()
#         return new_product

# async def update_product(name, value, id):
#     async with AsyncSessionLocal() as session:
#         product = await session.get(
#             Product, id)
#         setattr(product, name, value)
#         await session.commit()
#         await session.refresh(product)
#         return product
# async def delete_product(product_id: int):
#     async with AsyncSessionLocal() as session:
#         product = await session.get(Product, product_id)
#         await session.delete(product)
#         await session.commit()
#     return



async def update_setting_field(field_name: str, new_value: str):
    async with AsyncSessionLocal() as session:
        setting = await session.get(Setting, 1)
        setting_obj = setting
        setattr(setting_obj, field_name, new_value)
      
        await session.commit()
        return setting_obj

# async def stats_reports():
#     async with AsyncSessionLocal() as session:
#         result = await session.execute(
#             Order.__table__.select()
#         )
#         return result.fetchall()