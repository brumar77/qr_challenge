import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

if os.getenv("ENVIRONMENT") == "test":
    DATABASE_URL = os.getenv("DATABASE_URL_TEST")  # Base de datos para pruebas
else:
    DATABASE_URL = os.getenv("DATABASE_URL")  # Base de datos para producción

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()

def create_all_tables():
    from app.src.models.users import User
    from app.src.models.qr_codes import QrCodes
    from app.src.models.scans import Scans

    # Crear tablas en la base de datos
    Base.metadata.create_all(bind=engine)
    print("Todas las tablas creadas exitosamente.")
