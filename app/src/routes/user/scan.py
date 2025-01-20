import datetime
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session

from app.src.database import get_db
from app.src.middleware.security import get_current_user
from app.src.models.qr_codes import QrCodes
from app.src.models.scans import Scans
from app.src.schemas.qr.qr import QRMetricsResponse, ScanDetail
from app.src.utils.scan import get_country_from_ip


scan_routes = APIRouter(
    prefix="/scan",
    tags=["Scan"],
)

############################################################################################################

@scan_routes.get("/qr-codes/scan/{qr_id}",summary="Scan QR Code - Use Postman")
def scan_qr_code(qr_id: str, request: Request, db: Session = Depends(get_db)):
    
    qr_code = db.query(QrCodes).filter(QrCodes.id == qr_id).first()
    if not qr_code:
        raise HTTPException(status_code=404, detail="QR Code not found")

    # IP del cliente
    client_ip = request.client.host
    
    # client_ip="190.27.240.0"  # Colombia Bogota

    # Obtener país desde la IP con ipstack
    country_name, city, current_time = get_country_from_ip(client_ip)

    timestamp = datetime.datetime.now()

    scan = Scans(
        ip=client_ip,
        current_time_from_ip_client=current_time,
        timestamp=timestamp, 
        country=country_name,
        city=city,
        qr_uuid=qr_code.id
    )
    
    db.add(scan)

    qr_code.scan_count += 1

    db.commit()

    #funciona en postman
    return RedirectResponse(url=qr_code.url, status_code=302)

############################################################################################################