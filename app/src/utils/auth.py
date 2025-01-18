from fastapi import HTTPException,status
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

# Confi hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Conf JWT
SECRET_KEY = "mi_secreto_super_seguro"  
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Generar un token JWT
def create_access_token(data: dict, expires_delta: timedelta = None):
    try:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise ValueError(f"Error al generar el token: {e}")


# Decodificar y validar un token JWT
def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        # Maneja el error genérico de JWT
        raise ValueError(f"Token inválido: {e}")
