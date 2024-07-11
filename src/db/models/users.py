from dataclasses import dataclass
from typing import Optional
from psycopg.rows import class_row
from datetime import date, datetime

SELECT_USER = "SELECT * FROM users WHERE telegram_id = %s"
INSERT_USER = "INSERT INTO users (telegram_id) VALUES (%s)"

@dataclass
class User:
    """
    Class representing a user record.

    Attributes:
        id (Optional[int]): The unique id of the user.
        telegram_id (str): The Telegram id of the user.
    """
    id: Optional[int]
    telegram_id: str
    
async def get_user(pool, telegram_id):
    try:
        async with pool.connection() as conn, conn.cursor(
            row_factory=class_row(User)
        ) as cursor:
            await cursor.execute(
                SELECT_USER, (telegram_id,)
            )
            return await cursor.fetchone()
    except Exception as e:
        print(f"Unable to fetch user: {e}")
    
async def add_user(pool, user: User):
    try:
        async with pool.connection() as conn:
            await conn.execute(
                INSERT_USER, (user.telegram_id,)
            )
            await conn.commit()
    except Exception as e:
        print(f"Unable to add user: {e}")
