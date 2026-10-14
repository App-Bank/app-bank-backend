from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import timezone_router, transfer_router

# 1. Crea las tablas físicamente en el archivo banco.db si no existen
Base.metadata.create_all(bind=engine)

# 2. Inicializa la aplicación FastAPI
app = FastAPI(title="App Bank MVP API", version="1.0.0")

# 3. Incluye los routers del bloque
app.include_router(timezone_router.router)
app.include_router(transfer_router.router)  # <-- ¡Solucionado el bloqueo!


@app.get("/")
def read_root():
    return {"message": "¡El Backend del Banco está funcionando correctamente!"}

