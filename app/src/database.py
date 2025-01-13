from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://user_qr:user_qr_password@localhost:5433/qr_management"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    finally:
        session.close()



# Gestión de tablas
def create_all_tables():
    from models.users import User
    from models.qr_codes import QrCodes
    from models.scans import Scans

    Base.metadata.create_all(bind=engine)
    print("Todas las tablas creadas exitosamente.")

create_all_tables()

