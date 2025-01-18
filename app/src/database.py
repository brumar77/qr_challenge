import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


load_dotenv()

if os.getenv("ENVIRONMENT") == "test":
    DATABASE_URL = os.getenv("DATABASE_URL_TEST")  
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    session = SessionLocal()
    try:
        yield session
        # session.commit()
    finally:
        session.close()

def create_all_tables(bind=None):
    """
    Crea todas las tablas en la base de datos usando el motor proporcionado.
    Si no se proporciona un motor, se usa el motor por defecto (`engine`).
    """
    from app.src.models.users import User
    from app.src.models.qr_codes import QrCodes
    from app.src.models.scans import Scans

    try:
        # Usa el motor proporcionado o el motor por defecto
        bind = bind or engine
        Base.metadata.create_all(bind=bind)
        print("Todas las tablas creadas exitosamente.")
    except Exception as e:
        print(f"Error al crear las tablas: {str(e)}")
        raise