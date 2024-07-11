"""
Database Connection Module

This module creates an async connection pool to a PostgreSQL database.
"""

import os
from psycopg_pool import AsyncConnectionPool
from dotenv import load_dotenv

load_dotenv()

user=os.getenv('DB_USER')
password=os.getenv('DB_PASSWORD')
host=os.getenv('DB_HOST')
port=os.getenv('DB_PORT')
dbname=os.getenv('DB_NAME')

conninfo = f"user={user} password={password} host={host} port={port} dbname={dbname}"

async def get_async_pool():
    try:
        return AsyncConnectionPool(conninfo=conninfo)
    except Exception as e:
        print(f"Failed to start pool: {e}")
