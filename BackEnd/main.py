from fastapi import FastAPI
from app.config.databases import Base, engine
from fastapi.middleware.cors import CORSMiddleware

from app.modules.auth.router import router as auth_router
from app.modules.user.router import router as user_router

from app.modules.product.router import router as product_router
from app.modules.warehouse.router import router as warehouse_router
from app.modules.inventory.router import router as inventory_router
from app.modules.ledger.router import router as ledger_router

from app.modules.receipt.router import router as receipt_router
from app.modules.delivery.router import router as delivery_router
from app.modules.transfer.router import router as transfer_router
from app.modules.adjustment.router import router as adjustment_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="StockSense API",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_PREFIX = "/api/v1"


# AUTH & USER

app.include_router(
    auth_router,
    prefix=API_PREFIX
)

app.include_router(
    user_router,
    prefix=API_PREFIX
)


# MASTER DATA
app.include_router(
    product_router,
    prefix=API_PREFIX
)

app.include_router(
    warehouse_router,
    prefix=API_PREFIX
)


# INVENTORY

app.include_router(
    inventory_router,
    prefix=API_PREFIX
)

app.include_router(
    ledger_router,
    prefix=API_PREFIX
)


# OPERATIONS

app.include_router(
    receipt_router,
    prefix=API_PREFIX
)

app.include_router(
    delivery_router,
    prefix=API_PREFIX
)

app.include_router(
    transfer_router,
    prefix=API_PREFIX
)

app.include_router(
    adjustment_router,
    prefix=API_PREFIX
)


@app.get("/")
def root():

    return {
        "message": "StockSense API is running"
    }