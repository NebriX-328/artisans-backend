import hashlib
from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import DCARecord

router = APIRouter()

@router.post("/check")
async def verify_product(
    dca_id: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Read uploaded image
    image_bytes = await image.read()
    consumer_hash = hashlib.sha256(image_bytes).hexdigest()

    # Find record
    record = db.query(DCARecord).filter(DCARecord.dca_id == dca_id).first()
    if not record:
        return {"status": "error", "message": "DCA not found"}

    # Compare with artist scan hash
    if consumer_hash == record.artist_scan_hash:
        record.consumer_scan_hash = consumer_hash
        record.is_verified = "Authentic"
        db.commit()
        return {"status": "Authentic", "dca_id": dca_id}
    else:
        record.consumer_scan_hash = consumer_hash
        record.is_verified = "Tampered"
        db.commit()
        return {"status": "Tampered", "dca_id": dca_id}

