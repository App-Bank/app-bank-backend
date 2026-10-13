from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine


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


from app.routers import (
    user_router
)


app.include_router(user_router)


@app.get("/")
def read_root():
    return {"message": "Backend up and running"}