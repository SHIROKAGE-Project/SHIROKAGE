import aiosqlite

async def change(sql: str) -> bool:
    async with aiosqlite.connect("data/data.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute(sql)
    return True