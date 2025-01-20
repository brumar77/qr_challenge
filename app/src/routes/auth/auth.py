from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.src.database import get_db
from app.src.models.users import User
from app.src.models.qr_codes import QrCodes
from app.src.models.scans import Scans

from app.src.schemas.auth.auth import Token, UserLogin, UserOut, UserRegistry


from app.src.utils.auth import create_access_token, hash_password, verify_password
from app.src.utils.routes.public_routes import create_public_router

auth_routes = create_public_router(
    prefix="/auth",
    tags=["auth"],
)

@auth_routes.post("/register/", 
                  status_code=status.HTTP_201_CREATED, 
                  response_model=UserOut,
)
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
    
    user_out = UserOut(
        id=str(new_user.id),
        name=new_user.name,
        lastname=new_user.lastname,
        email=new_user.email,
        rol=new_user.rol,
    )

    return user_out

#####################################################################################

@auth_routes.post("/login/", response_model=Token)
async def iniciar_sesion(
    body: UserLogin, 
    response: Response,
    db: Session = Depends(get_db)):
    
    usuario = db.query(User).filter(User.email == body.email).first()

    
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    if not verify_password(body.password, usuario.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    
    access_token = create_access_token({"sub": usuario.email, "rol": usuario.rol})

    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True, 
        max_age=3600,  
        secure=False,  
        samesite="lax",  
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
