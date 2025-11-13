from fastapi import FastAPI, Query
from app.database import get_db_pool, save_transformation
from app.transform import mirror_word

app = FastAPI(title="Mirror API", version="1.0.0")

# Database pool gets initialized on startup
db_pool = None

@app.on_event("startup")
async def startup():
    global db_pool
    db_pool = await get_db_pool()

@app.on_event("shutdown")
async def shutdown():
    if db_pool:
        await db_pool.close()

@app.get("/api/health")
async def health_check():
    """Simple health check - just returns ok"""
    return {"status": "ok"}

@app.get("/api/mirror")
async def mirror(word: str = Query(..., description="Word to transform")):
    """
    Takes a word, flips the case of each letter, then reverses it.
    Example: fOoBar25 -> 52RAbOoF
    
    Also saves the original and transformed word to the database.
    """
    transformed = mirror_word(word)
    
    # Save to database (fire and forget style for now)
    if db_pool:
        await save_transformation(db_pool, word, transformed)
    
    return {"transformed": transformed}
