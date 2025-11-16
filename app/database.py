import os
import asyncpg
from typing import Optional

async def get_db_pool() -> Optional[asyncpg.Pool]:
    """
    Create a connection pool to PostgreSQL.
    Falls back gracefully if DB isn't available (for local testing).
    """
    db_url = os.getenv("DATABASE_URL")
    
    # If DATABASE_URL not set, try to build it from individual components
    if not db_url:
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_host = os.getenv("DB_HOST", "localhost")
        db_port = os.getenv("DB_PORT", "5432")
        db_name = os.getenv("DB_NAME", "mirrordb")
        
        if db_user and db_password:
            db_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
            print(f"✅ Built DATABASE_URL from components")
        else:
            print("⚠️  No DATABASE_URL or DB credentials set - running without database")
            return None
    
    try:
        pool = await asyncpg.create_pool(db_url, min_size=2, max_size=10)
        print("✅ Connected to database")
        return pool
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

async def save_transformation(pool: asyncpg.Pool, original: str, transformed: str):
    """
    Save the word transformation pair to the database.
    Schema: transformations(id, original_word, transformed_word, created_at)
    """
    try:
        async with pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO transformations (original_word, transformed_word, created_at)
                VALUES ($1, $2, NOW())
                """,
                original,
                transformed
            )
    except Exception as e:
        # Don't crash the API if DB write fails
        print(f"⚠️  Failed to save transformation: {e}")
