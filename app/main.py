from fastapi import FastAPI
from app.core.database import Base, engine
from app.routers import timezone

# 1. Crea las tablas físicamente en el archivo banco.db si no existen
Base.metadata.create_all(bind=engine)

# 2. Inicializa la aplicación FastAPI
app = FastAPI(title="App Bank MVP API", version="1.0.0")

# 3. Incluye router de zonas horarias
app.include_router(timezone.router)


@app.get("/")
def read_root():
    return {"message": "¡El Backend del Banco está funcionando correctamente!"}
