"""
Expense Processor Module

This module provides functions to indentify and categorize the messages received by the bot.
Whenever a valid expense message is received, the expense is processed and added to db.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
from db.models.expenses import Expense, add_expense
from db.models.templates import get_template
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

api_key=os.getenv('OPEN_API_KEY')

# Initialize the LLM, in this case OpenAI
llm = ChatOpenAI(api_key=api_key)
output_parser = StrOutputParser()

async def identify_expense(pool, message):
    try:
        template = await get_template(pool, 'expense_check_prompt')
        prompt = PromptTemplate.from_template(
            template.content
        )
        chain = prompt | llm | output_parser
        response = chain.invoke({"message": message})
        return "Expense: True" in response
    except Exception as e:
        print(f"Failed to identify expense: {e}")

async def categorize_expense(pool, message):
    try:
        template = await get_template(pool, 'expense_categorize_prompt')
        prompt = PromptTemplate.from_template(
            template.content
        )
        chain = prompt | llm | output_parser
        response = chain.invoke({"message": message})
        category = response.split("Category:")[-1].strip()
        return category
    except Exception as e:
        print(f"Failed to identify expense category: {e}")

async def extract_amount(pool, message):
    try:
        template = await get_template(pool, 'expense_amount_prompt')
        prompt = PromptTemplate.from_template(
            template.content
        )
        chain = prompt | llm | output_parser
        response = chain.invoke({"message": message})
        amount = response.split("Amount:")[-1].strip()
        return amount
    except Exception as e:
        print(f"Failed to extract message amount : {e}")

async def process_expense(pool, message, user_id):
    try:
        if await identify_expense(pool, message):
            # If it is an expense, get the category and extract amount
            category = await categorize_expense(pool, message)
            added_at = datetime.now()
            amount = await extract_amount(pool, message)

            expense = Expense(id=None, user_id=user_id, category=category, amount=amount, description=message, added_at=added_at)

            await add_expense(pool, expense)
            return f"{category} expense added ✅"
        else:
            return ""
    except Exception as e:
        print(f"Failed to process expense: {e}")