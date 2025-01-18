import os
import uuid
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.src.models.users import User
from app.src.database import Base, get_db
from app.src.utils.auth import hash_password
from app.src.main import app

# Crear un archivo temporal para la base de datos
TEST_DB_PATH = "test.db"
SQLALCHEMY_DATABASE_URL = f"sqlite:///{TEST_DB_PATH}"

# Eliminar la base de datos si existe antes de iniciar las pruebas
if os.path.exists(TEST_DB_PATH):
    os.remove(TEST_DB_PATH)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
test_session = TestingSessionLocal()

@pytest.fixture(scope="session", autouse=True)
def setup_test_database():
    """
    Configuración inicial de la base de datos de prueba.
    """
    # Importar todos los modelos para asegurarse de que estén registrados
    from app.src.models import users , qr_codes, scans 
    
    # Crear todas las tablas
    Base.metadata.drop_all(bind=engine)  # Eliminar tablas existentes
    Base.metadata.create_all(bind=engine)  # Crear tablas nuevas
    
    yield
    
    # Limpiar
    test_session.close()
    engine.dispose()
    
    if os.path.exists(TEST_DB_PATH):
        try:
            os.remove(TEST_DB_PATH)
            print(f"\nBase de datos de prueba ({TEST_DB_PATH}) eliminada exitosamente.")
        except Exception as e:
            print(f"\nError al eliminar la base de datos de prueba: {e}")

@pytest.fixture
def test_db():
    """
    Proporciona una sesión de base de datos para las pruebas.
    """
    try:
        yield test_session
    finally:
        # Hacer rollback en lugar de commit para no afectar otras pruebas
        test_session.rollback()

@pytest.fixture
def test_client(test_db):
    """
    Proporciona un cliente de prueba.
    """
    def override_get_db():
        try:
            yield test_db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as client:
        yield client
    
    app.dependency_overrides.clear()

@pytest.fixture
def test_user(test_db):
    """
    Crea un usuario de prueba.
    """
    plain_password = "1234"
    hashed_password = hash_password(plain_password)
    
    user = User(
        name="TestUser",
        lastname="TestLastName",
        email=f"test_{uuid.uuid4().hex[:8]}@example.com",
        hashed_password=hashed_password
    )
    
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    
    return {
        "user_id": user.id,
        "user_email": user.email,
        "plain_password": plain_password
    }
    
@pytest.fixture
def auth_headers(test_client, test_user):
    """
    Proporciona los headers de autenticación necesarios para las pruebas.
    """
    # Hacer login para obtener el token
    login_data = {
        "email": test_user["user_email"],
        "password": test_user["plain_password"]
    }
    response = test_client.post("/auth/login/", json=login_data)
    token = response.json()["access_token"]
    
    # Retornar los headers con el token
    return {"Authorization": f"Bearer {token}"}