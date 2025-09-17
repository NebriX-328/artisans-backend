import uuid
import hashlib
import json
import shutil
import os
from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models import DCARecord

router = APIRouter()

@router.post("/register")
async def register_dispatch(
    product_id: int = Form(...),
    artwork_name:str = Form(...),
    artist_name: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # ensure uploads dir exists
    os.makedirs("uploads", exist_ok=True)

    # default values
    image_url = ""
    scan_hash = ""

    # Save uploaded image to /uploads and compute hash (read ONCE)
    if image:
        filename = f"{uuid.uuid4()}_{image.filename}"
        file_path = f"uploads/{filename}"

        # Read the file bytes once
        image_bytes = await image.read()

        # Compute hash from the same bytes
        scan_hash = hashlib.sha256(image_bytes).hexdigest()

        # Write the same bytes to disk
        with open(file_path, "wb") as buffer:
            buffer.write(image_bytes)

        # Public URL for FastAPI static mount
        image_url = f"http://127.0.0.1:8000/uploads/{filename}"

    # Generate new DCA ID
    dca_id = str(uuid.uuid4())

    # JSON payload
    dca_json = {
        "dca_id": dca_id,
        "product_id": product_id,
        "artwork_name":artwork_name,
        "artist_name": artist_name,
        "scan_hash": scan_hash,
        "image_url": image_url,
    }

    # Save in DB
    rec = DCARecord(
        dca_id=dca_id,
        product_id=product_id,
        artwork_name=artwork_name,
        artist_name=artist_name,
        artist_scan_hash=scan_hash,
        signed_json=json.dumps(dca_json)
    )
    db.add(rec)
    db.commit()
    db.refresh(rec)

    return {"dca_id": dca_id, "image_url": image_url}
