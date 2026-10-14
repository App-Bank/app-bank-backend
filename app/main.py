from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine


from app.models import(
    account_model,
    activity_model,
    activity_type_model,
    timezone_model,
    transfer_model,
    user_model
)


from app.routers import (
    account_router,
    activity_router,
    activity_type_router,
    timezone_router,
    transfer_router,
    user_router
)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Bank App API",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(account_router.router)
app.include_router(activity_router.router)
app.include_router(activity_type_router.router)
app.include_router(timezone_router.router)
app.include_router(transfer_router.router)
app.include_router(user_router.router)


@app.get("/")
def read_root():
    return {"message": "Backend up and running"}