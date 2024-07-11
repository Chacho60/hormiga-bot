from dataclasses import dataclass
from typing import Optional
from psycopg.rows import class_row
from datetime import date, datetime

SELECT_TEMPLATE = "SELECT * FROM prompt_templates WHERE name = %s"

@dataclass
class Template:
    """
    Class for the prompt templates stored in db.

    Attributes:
        id (Optional[int]): The unique id of the template.
        name (str): The name of the template.
        content (str): The content of the template.
    """
    id: Optional[int]
    name: str
    content: str

async def get_template(pool, template_name):
    try:
        async with pool.connection() as conn, conn.cursor(
            row_factory=class_row(Template)
        ) as cursor:
            await cursor.execute(
                SELECT_TEMPLATE, (template_name,)
            )
            return await cursor.fetchone()
    except Exception as e:
        print(f"Unable to fetch prompt template: {e}")