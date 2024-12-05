# app/main.py
from fastapi import FastAPI
from app.routers import accounts, auth, categories, products, users
from app.db.database import connect_db, close_db
from app.routers import sales
from app.routers import reviews



app = FastAPI()
app.include_router(sales.router, prefix="/sales", tags=["Sales"])
app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])

# Include Routers
app.include_router(accounts.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(products.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(reviews.router)

# Startup and Shutdown Events
@app.on_event("startup")
async def startup_db_client():
    await connect_db()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_db()
