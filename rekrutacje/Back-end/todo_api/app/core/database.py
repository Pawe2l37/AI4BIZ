from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Utworzenie silnika SQLAlchemy
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, connect_args={"check_same_thread": False}
)

# Sesja do komunikacji z bazą danych
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Bazowa klasa dla modeli SQLAlchemy
Base = declarative_base()


def get_db():
    """
    Generator dostarczający sesję bazy danych dla endpointów.
    Zapewnia zamknięcie sesji po zakończeniu zapytania.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 