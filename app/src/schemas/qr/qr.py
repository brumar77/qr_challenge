# Esquema para la solicitud del QR
from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel, Field, validator


class QRCodeCreate(BaseModel):
    url: str = Field(..., descripcion="La URL del QR", example="https://google.com")
    color: str = Field(..., descripcion="El color del QR, en hexadecimal", pattern="^#([A-Fa-f0-9]{6})$" ,example="#000000")
    size: int = Field(..., descripcion="El tamaño del QR, en pixeles", ge=100, le=1000, example="250")
    user_id: UUID = Field(..., descripcion="El ID del usuario, uuid, puedes usar el presentado", example="3a15d40e-fe70-41f4-b717-c3a09f177e83")

############################################################################################################

class QRCodeUpdate(BaseModel):
    url: Optional[str] = Field(..., descripcion="La URL del QR", example="http://youtube.com")
    color: Optional[str] = Field(..., descripcion="El color del QR, en hexadecimal", pattern="^#([A-Fa-f0-9]{6})$" ,example="#000000")
    size: Optional[int] = Field(..., descripcion="El tamaño del QR, en pixeles", ge=100, le=1000, example="250")
    
############################################################################################################
class QrCodeOut(BaseModel):
    qr_id: UUID
    url: str
    color: str
    size: int
    file_path: str
    
class ResponseQrCodeOut(BaseModel):
    mensaje: str
    data: List[QrCodeOut]
    
############################################################################################################
class ScanDetail(BaseModel):
    ip: str
    country: Optional[str] = None
    city: Optional[str] = None
    current_time_from_ip_client: Optional[str] = None

class QRMetricsResponse(BaseModel):
    qr_id: UUID
    url: str
    scan_count: int
    scan_details: List[ScanDetail]