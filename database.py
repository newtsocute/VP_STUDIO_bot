# import aiosqlite
#
# async def setup_database():
#     """Создаёт базу данных и таблицу пользователей, если их нет (один раз)"""
#     async with aiosqlite.connect("users.db") as db:
#         await db.execute("""
#             CREATE TABLE IF NOT EXISTS users (
#                 user_id INTEGER PRIMARY KEY
#             )
#         """)
#         await db.commit()
