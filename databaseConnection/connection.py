import aiomysql
import asyncio

DB_CONFIG = {
    'host': 'localhost',
    'user': 'admin',
    'password': 'Hamster2005!',
    'db': 'JudoBase',
}


async def get_connection():
    return await aiomysql.connect(**DB_CONFIG)


async def execute_query(query, params=None, many=False):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        if many:
            for row in params or []:
                await cursor.execute(query, row)
        else:
            await cursor.execute(query, params or ())
        await conn.commit()
    conn.close()


async def fetch_all(query, params=None):
    conn = await get_connection()
    async with conn.cursor() as cursor:
        await cursor.execute(query, params or ())
        result = await cursor.fetchall()
    conn.close()
    return result
