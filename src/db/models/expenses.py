from dataclasses import dataclass
from typing import Optional
from psycopg.rows import class_row
from datetime import date, datetime

INSERT_EXPENSE = "INSERT INTO expenses (user_id, category, amount, description, added_at) VALUES (%s, %s, %s, %s, %s)"

@dataclass
class Expense:
    """
    Class representing an expense record.

    Attr:
        id (Optional[int]): The unique id for the expense.
        user_id (int): The id of the user who made the expense.
        category (str): The category of the expense.
        amount (str): The amount of the expense.
        description (str): The description of the expense.
        added_at (date): The date when the expense was added.
    """
    id: Optional[int]
    user_id: int
    category: str
    amount: str
    description: str
    added_at: date

async def add_expense(pool, expense: Expense):
    try:
        async with pool.connection() as conn:
            await conn.execute(
                INSERT_EXPENSE,
                (expense.user_id, expense.category, expense.amount, expense.description, expense.added_at)
            )
            await conn.commit()
    except Exception as e:
        print(f"Unable to add expense: {e}")