import uvicorn
from database import Base, get_engine
from auth.model import User
from todo.model import Task

async def create_tables():
    engine = get_engine()
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

if __name__ == '__main__':
    import asyncio
    asyncio.run(create_tables())
#     uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)
