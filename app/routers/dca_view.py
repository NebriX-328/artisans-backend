from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import HTMLResponse
from app.db import get_db
from app.models import DCARecord
import json

# ✅ This should be APIRouter(), not FastAPI()
router = APIRouter()

@router.get("/dca/view/{dca_id}", response_class=HTMLResponse)
def view_dca(dca_id: str, db: Session = Depends(get_db)):
    record = db.query(DCARecord).filter(DCARecord.dca_id == dca_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="DCA not found")

    dca_data = json.loads(record.signed_json)
    img_url = dca_data.get("image_url", "")

    return f"""
    <html>
      <head><title>DCA Verification</title></head>
      <body style="font-family:sans-serif; margin:20px;">
        <h1>DCA Verification</h1>
        <h2>Verified Certificate</h2>
        <p><b>Product ID:</b> {dca_data.get('product_id')}</p>
        <p><b>Artwork Name:</b> {dca_data.get('artwork_name')}</p>
        <p><b>Artist:</b> {dca_data.get('artist_name')}</p>
        <p><b>Verified by:</b> Artisans Certification Authority</p>
        {f"<img src='"+img_url+"'style='max-width:400px;border:1px solid #ccc;'>" if img_url else ""}
      </body>
    </html>
    """
