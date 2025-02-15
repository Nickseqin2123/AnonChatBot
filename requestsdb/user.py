import asyncio

from sqlalchemy.ext.asyncio import async_sessionmaker
from db.config import cfg
from db.models import Users


async def get_user(id_usr: int):
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            user = await session.get(Users, id_usr)
            
            if bool(user):
                return user.link
            else:
                ...
    finally:
        await cfg.engine.dispose()


asyncio.run(get_user(1124518724))