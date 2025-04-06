import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import auth, tasks, users

# Konfiguracja loggera
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Utworzenie tabel w bazie danych
Base.metadata.create_all(bind=engine)

# Utworzenie aplikacji FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Konfiguracja CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # W produkcji należy ograniczyć do konkretnych domen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dołączenie routerów
app.include_router(auth.router, prefix=settings.API_V1_STR)
app.include_router(users.router, prefix=settings.API_V1_STR)
app.include_router(tasks.router, prefix=settings.API_V1_STR)


@app.get("/")
def root():
    """
    Endpoint główny, zwracający informacje o API.
    
    Returns:
        Informacje o API.
    """
    return {
        "message": "Witaj w API Listy Zadań",
        "docs_url": "/docs",
        "api_prefix": settings.API_V1_STR
    }


if __name__ == "__main__":
    logger.info("Uruchamianie serwera API...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 