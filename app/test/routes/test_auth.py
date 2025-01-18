from uuid import UUID
import pytest

from app.test.config import client
from fastapi.testclient import TestClient
from app.src.main import app

client = TestClient(app)


##############################################################################################################
def is_valid_uuid(value: str) -> bool:
    """
    Verifica si un valor es un UUID válido.
    """
    try:
        UUID(value)
        return True
    except ValueError:
        return False


@pytest.mark.auth
@pytest.mark.parametrize("new_user, code_response", [
    # Caso 1: Registro exitoso
    (
        {
            "name": "TestName",
            "lastname": "TestLastName",
            "email": "test@gmail.com",
            "password": "1234",
        },
        201,
    ),
    # Caso 2: Correo electrónico ya registrado
    (
        {
            "name": "DuplicateName",
            "lastname": "DuplicateLastName",
            "email": "test@gmail.com",  # Mismo correo del caso anterior
            "password": "password123",
        },
        400,
    ),
    # Caso 3: Faltan campos obligatorios
    (
        {
            "name": "",
            "lastname": "",
            "email": "",
            "password": "",
        },
        422,
    ),
    # Caso 4: Contraseña muy corta
    (
        {
            "name": "ShortPassword",
            "lastname": "User",
            "email": "shortpassword@gmail.com",
            "password": "12",  # Contraseña inválida
        },
        422,
    ),
    # Caso 5: Correo electrónico inválido
    (
        {
            "name": "InvalidEmail",
            "lastname": "User",
            "email": "invalid-email",  # Formato inválido
            "password": "1234",
        },
        422,
    ),
])
def test_registrar_usuario(new_user: dict, code_response: int):
    response = client.post(url="/auth/register/", json=new_user)

    # Validar tipo de contenido
    assert response.headers["Content-Type"] == "application/json"
    assert response.status_code == code_response

    data = response.json()

    if response.status_code == 201:  # Caso de éxito
        assert is_valid_uuid(data["id"]), f"Invalid UUID: {data['id']}"
        assert data["name"] == new_user["name"]
        assert data["lastname"] == new_user["lastname"]
        assert data["email"] == new_user["email"]
        assert "password" not in data  # La contraseña no debe estar en la respuesta
    elif response.status_code == 400:  # Casos de error
        assert "detail" in data, f"Missing 'detail' in response: {data}"


##############################################################################################################
def test_iniciar_sesion_exitoso(test_user):
    """Test para iniciar sesión exitosamente."""
    body = {"email": "test@gmail.com", "password": test_user["plain_password"]}

    response = client.post("/auth/login/", json=body)
    
    print(response.json())
    
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "Bearer"
    assert data["user"]["email"] == body["email"]
    assert data["user"]["rol"] == "user"

    assert response.cookies.get("access_token") is not None


def test_iniciar_sesion_fallo_credenciales_invalidas():
    """Test para credenciales inválidas."""
    body = {"email":"test@gmail.com" , "password": "wrongpassword"}

    response = client.post("/auth/login/", json=body)
    print(response.json())
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect password"}

def test_iniciar_sesion_fallo_usuario_no_existente():
    """Test para un usuario inexistente."""
    body = {"email": "nonexistent@example.com", "password": "password123"}

    response = client.post("/auth/login/", json=body)
    print(response.json())
    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}