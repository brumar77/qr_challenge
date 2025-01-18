from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.src.database import get_db
from app.src.middleware.security import get_current_user
from app.src.models.qr_codes import QrCodes
from app.src.models.scans import Scans
from app.src.schemas.qr.qr import QRMetricsResponse, ScanDetail


statistic_routes = APIRouter(
    prefix="/statistic",
    tags=["Statistic"],
    dependencies=[Depends(get_current_user)],
)

############################################################################################################


@statistic_routes.get("/qr-codes/metrics/{qr_id}", response_model=QRMetricsResponse)
def get_qr_metrics(qr_id: UUID, db: Session = Depends(get_db)):
    qr_code = db.query(QrCodes).filter(QrCodes.id == qr_id).first()
    if not qr_code:
        raise HTTPException(status_code=404, detail="QR Code not found")
    
    scan_count = qr_code.scan_count
    
    scans : List[Scans] = db.query(Scans).filter(Scans.qr_uuid == qr_code.id).all()
    scan_details = [ScanDetail(
            ip=scan.ip,
            country=scan.country,
            city=scan.city,
            current_time_from_ip_client=scan.current_time_from_ip_client
        ) for scan in scans]

    response = QRMetricsResponse(
        qr_id=qr_code.id,
        url=qr_code.url,
        scan_count=scan_count,
        scan_details=scan_details
    )

    return response

