from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserRegistry(BaseModel):
    name: str = Field(min_length=2, max_length=50, json_schema_extra={
        "description": "El nombre del usuario",
        "example": "Roberto"
    })
    lastname: str = Field(min_length=2, max_length=50, json_schema_extra={
        "description": "El apellido del usuario",
        "example": "Gómez"
    })
    email: EmailStr = Field( min_length=3, max_length=100 ,json_schema_extra={
        "description": "El correo electrónico del usuario",
        "example": "roberto.gomez@example.com"
    })
    password: str = Field(min_length=4, max_length=100, json_schema_extra={
        "description": "La contraseña del usuario",
        "example": "1234"
    })
    
class UserLogin(BaseModel):
    email: EmailStr = Field(json_schema_extra={
        "description": "El correo electrónico del usuario",
        "example": "roberto.gomez@example.com"
    })
    password: str = Field(min_length=4, max_length=100, json_schema_extra={
        "description": "La contraseña del usuario",
        "example": "1234"
    })
    
class UserOut(BaseModel):
    id: UUID = Field(json_schema_extra={
        "description": "El identificador único del usuario",
        "example": "123e4567-e89b-12d3-a456-426614174000"
    })
    name: str = Field(min_length=2, json_schema_extra={
        "description": "El nombre del usuario",
        "example": "Martín"
    })
    lastname: str = Field(min_length=2, json_schema_extra={
        "description": "El apellido del usuario",
        "example": "Pérez"
    })
    email: EmailStr = Field(json_schema_extra={
        "description": "El correo electrónico del usuario",
        "example": "martin.perez@example.com"
    })
    rol: str = Field(json_schema_extra={
        "description": "El rol del usuario (admin o estándar)",
        "example": "admin"
    })


class Token(BaseModel):
    access_token: str
    token_type: str = Field(default="Bearer")
    user: UserOut
