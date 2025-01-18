import os
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, JSONResponse

from sqlalchemy.orm import Session

from app.src.models.users import User
from app.src.models.qr_codes import QrCodes
from app.src.models.scans import Scans

from app.src.database import get_db

from app.src.middleware.security import get_current_user, verificar_rol

from app.src.schemas.qr.qr import QRCodeCreate, QRCodeUpdate, QrCodeOut, ResponseQrCodeOut
from app.src.utils.qr import generate_qr_code


user_routes = APIRouter(
    prefix="/user",
    tags=["User"],
    dependencies=[Depends(get_current_user)],
)


@user_routes.post("/qr-codes/")
async def create_qr_code(data: QRCodeCreate,db: Session = Depends(get_db)):
    
    # Verificar si el usuario existe
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
        # raise {"error": f"User with {data.user_id} not found"}  
        
    file_path = generate_qr_code(data.url, data.color, data.size)
    
    if not file_path:
        raise HTTPException(status_code=500, detail="Error generating QR code")
    
    qr_code = QrCodes(
        url=data.url,
        color=data.color,
        size=data.size,
        file_path=file_path,
        user_id=data.user_id
    )
    db.add(qr_code)
    db.commit()
    db.refresh(qr_code)
    
    return FileResponse(
        file_path, 
        media_type="image/png", 
        headers={"Content-Disposition": f"attachment; filename=qr_code.png"})
    
    
############################################################################################################

@user_routes.get("/qr-codes/user/{user_id}", response_model=ResponseQrCodeOut)
def list_qr_codes(user_id: UUID, db: Session = Depends(get_db)):
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    qr_codes = db.query(QrCodes).filter(QrCodes.user_id == user_id).all()
    
    data = [
        QrCodeOut(
            qr_id=qr.id, 
            url=qr.url, 
            color=qr.color, 
            size=qr.size, 
            file_path=qr.file_path
        ) for qr in qr_codes
    ]
    
    return ResponseQrCodeOut(
        mensaje="List of QR Codes", 
        data=data
    )
    
############################################################################################################    

@user_routes.put("/qr-codes/{qr_id}", response_model=dict)
def update_qr_code(qr_id: UUID, data: QRCodeUpdate, db: Session = Depends(get_db)):
    
    qr_code = db.query(QrCodes).filter(QrCodes.id == qr_id).first()
    
    if not qr_code:
        raise HTTPException(status_code=404, detail="QR Code not found")
    
    if data.url:
        qr_code.url = data.url
    if data.color:
        qr_code.color = data.color
    if data.size:
        qr_code.size = data.size

    # Guardar la ruta del archivo antiguo para eliminarlo después
    old_file_path = qr_code.file_path

    # Regenerar el QR y actualizar la ruta en la base de datos
    new_file_path = generate_qr_code(qr_code.url, qr_code.color, qr_code.size)
    qr_code.file_path = new_file_path

    db.add(qr_code)
    db.flush()
    db.commit()  
    db.refresh(qr_code)

    if old_file_path and os.path.exists(old_file_path):
        os.remove(old_file_path)

    return {"qr_id": str(qr_code.id), "file_path": new_file_path}

############################################################################################################