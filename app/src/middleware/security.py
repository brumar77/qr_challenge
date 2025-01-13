from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer

from utils.auth import decode_token


def get_current_user(request: Request):
    """
    Obtiene al usuario actual a partir del token en las cabeceras o en las cookies.
    """
    # Intentar obtener el token desde la cabecera
    token = request.headers.get("Authorization")
    if token and token.startswith("Bearer "):
        token = token[7:]  # Remover el prefijo Bearer
    else:
        # Si no hay token en la cabecera, buscar en las cookies
        token = request.cookies.get("access_token")
        if not token:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token no encontrado",
            )
        elif token.startswith("Bearer "):
            token = token[7:]    

    payload = decode_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
        )
    return payload


def verificar_rol(rol_requerido: str):
    def wrapper(payload: dict = Depends(get_current_user)):
        if payload.get("rol") != rol_requerido:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tienes permiso para acceder a esta ruta",
            )
        return payload
    return wrapper
