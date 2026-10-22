from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, SessionLocal, engine
from app.db.seed import run_seed


from app.models import(
    account_model,
    activity_model,
    activity_type_model,
    transfer_model,
    user_model
)


from app.routers import (
    account_router,
    activity_router,
    transfer_router,
    user_router,
    auth_router
)


Base.metadata.create_all(bind=engine)


db = SessionLocal()
try:
    run_seed(db)
finally:
    db.close()


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
app.include_router(transfer_router.router)
app.include_router(user_router.router)
app.include_router(auth_router.router)


@app.get("/")
def read_root():
    return {"message": "Backend up and running"}