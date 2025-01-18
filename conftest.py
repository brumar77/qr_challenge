import uuid
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.src.models.users import User
from app.src.database import Base
from app.src.utils.auth import hash_password

TEST_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def db():
    """Fixture para configurar la base de datos de pruebas."""
    Base.metadata.create_all(bind=engine)  
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback() 
        db.close()
        Base.metadata.drop_all(bind=engine) 

@pytest.fixture
def test_user(db):
    """Fixture para crear un usuario de prueba."""
    
    plain_password = "1234"
    hashed_password = hash_password(plain_password)

    user: User = User(
        name="TestNameMemory",
        lastname= "TestLastNameMemory",
        email= f"testmemory_{uuid.uuid4().hex[:8]}@gmail.com",
        hashed_password=hashed_password,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {
        "user_email" : user.email, 
        "plain_password" : plain_password
    }
