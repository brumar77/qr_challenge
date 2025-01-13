from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserRegistry(BaseModel):
    name: str = Field(..., description="El nombre del usuario", min_length=2, max_length=50, example="Roberto")
    lastname: str = Field(..., description="El apellido del usuario", min_length=2, max_length=50, example="Gómez")
    email: EmailStr = Field(..., description="El correo electrónico del usuario", example="roberto.gomez@example.com")
    password: str = Field(..., description="La contraseña del usuario", min_length=4, max_length=100, example="1234")
    
class UserLogin(BaseModel):
    email: EmailStr = Field(..., description="El correo electrónico del usuario", example="roberto.gomez@example.com")
    password: str = Field(..., description="La contraseña del usuario", min_length=4, max_length=100, example="1234")
    
class UserOut(BaseModel):
    id: UUID = Field(..., description="El identificador único del usuario", example="12345")
    name: str = Field(..., description="El nombre del usuario", min_length=2, example="Martín")
    lastname: str = Field(..., description="El apellido del usuario", min_length=2, example="Pérez")
    email: EmailStr = Field(..., description="El correo electrónico del usuario", example="martin.perez@example.com")
    rol: str = Field(..., description="El rol del usuario (admin o estándar)", example="admin")


class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    user: UserOut
