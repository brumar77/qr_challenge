from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from database import get_db
from models.users import User
from models.qr_codes import QrCodes
from models.scans import Scans

from schemas.auth.auth import Token, UserLogin, UserOut, UserRegistry


from utils.auth import create_access_token, hash_password, verify_password


auth_routes = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@auth_routes.post("/register/", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def registrar_usuario(user: UserRegistry, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="El correo ya está registrado.")
    
    hashed_password = hash_password(user.password)
    new_user = User(
        name=user.name,
        lastname=user.lastname,
        email=user.email,
        hashed_password=hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(new_user)

    user_out = UserOut(
        id=str(new_user.id),
        name=new_user.name,
        lastname=new_user.lastname,
        email=new_user.email,
        rol=new_user.rol,
    )

    return user_out

@auth_routes.post("/login/", response_model=Token)
async def iniciar_sesion(
    body: UserLogin, 
    response: Response,
    db: Session = Depends(get_db)):
    
    # Buscar al usuario en la base de datos
    usuario = db.query(User).filter(User.email == body.email).first()

    # Validar credenciales
    if not usuario or not verify_password(body.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
        )
    
    # Crear el token de acceso
    access_token = create_access_token({"sub": usuario.email, "rol": usuario.rol})

    # Guardar el token en una cookie
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,  # Solo accesible por el servidor
        max_age=3600,  #  1 hora
        secure=False,  # Configurar en True en HTTPS
        samesite="lax",  # Cambiar a "strict" para prod
    )

    return Token(
        access_token=access_token,
        token_type="Bearer",
        user=UserOut(
            id=str(usuario.id),
            name=usuario.name,
            lastname=usuario.lastname,
            email=usuario.email,
            rol=usuario.rol,
        )
    )
