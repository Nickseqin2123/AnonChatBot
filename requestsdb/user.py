from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker
from db.config import cfg
from db.models import Users
from uti.code import encode_id


async def getUserLink(id_usr: int):
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            user = await session.get(Users, id_usr)
            
            if bool(user):
                return user.link
            else:
                return False
    finally:
        await cfg.engine.dispose()


async def setUser(id_usr: int):
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            encoded: str = await encode_id(id_usr)
            
            user = Users(id=id_usr, link=encoded)
            session.add(user)
            
            await session.commit()  
    finally:
        await cfg.engine.dispose()


async def searchUser(user_link: str):
    session = async_sessionmaker(cfg.engine)
    
    try:
        async with session() as session:
            user = select(Users).filter(Users.link == user_link).all()
            print(user)
    finally:
        await cfg.engine.dispose()

