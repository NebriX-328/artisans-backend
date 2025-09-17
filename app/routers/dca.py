from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from app.db import get_db
from app.models import DCARecord
import json, os, socket, io, requests
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import qrcode

router = APIRouter()

# --- 🔹 Replace with your real domain ---
PUBLIC_DOMAIN = "https://artisans-backend-t0ne.onrender.com"  # e.g. "certs.artsite.com"


def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


@router.get("/{dca_id}/pdf")
def get_dca_pdf(dca_id: str, db: Session = Depends(get_db)):
    """
    Generates a landscape DCA certificate PDF with a working QR code and art image.
    """
    record = db.query(DCARecord).filter(DCARecord.dca_id == dca_id).first()
    if not record:
        raise HTTPException(status_code=404, detail="DCA not found")

    dca_data = json.loads(record.signed_json)
    img_url = dca_data.get("image_url")

    # --- Build QR Link ---
    if PUBLIC_DOMAIN:  # Use public domain if provided
        qr_data = f"https://artisans-backend-t0ne.onrender.com/dca/view/{dca_id}"
    else:  # fallback for local network testing
        local_ip = get_local_ip()
        qr_data = f"http:// 192.168.1.8:8000/dca/view/{dca_id}"

    # --- Generate QR Code ---
    qr_img = qrcode.make(qr_data)
    qr_path = f"qr_{dca_id}.png"
    qr_img.save(qr_path)

    # --- Create PDF ---
    pdf_filename = f"dca_{dca_id}.pdf"
    c = canvas.Canvas(pdf_filename, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Header
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(width / 2, height - 60, "Digital Certificate of Authenticity")

    # Decorative line
    c.setLineWidth(2)
    c.line(50, height - 75, width - 50, height - 75)

    # Fields
    c.setFont("Helvetica", 14)
    y = height - 130
    c.drawString(80, y, f"Product ID: {dca_data.get('product_id', '')}")
    y -= 25
    c.drawString(80, y, f"Artwork Name: {dca_data.get('artwork_name', '')}")
    y -= 25
    c.drawString(80, y, f"Artist: {dca_data.get('artist_name', '')}")
    y -= 25
    c.drawString(80, y, f"Verified By: Artisans Certification Authority")

    # ✅ Art image (fixed)
    if img_url:
        try:
            # Fetch the image bytes from the URL
            response = requests.get(img_url)
            response.raise_for_status()
            art_image = ImageReader(io.BytesIO(response.content))
            c.drawImage(art_image, 80, 100, width=250, height=250)
        except Exception as e:
            print("Could not add image to PDF:", e)

    # QR code bottom right
    c.drawImage(qr_path, width - 200, 80, width=120, height=120)
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(width - 210, 70, "Scan to verify online")

    c.showPage()
    c.save()

    # Cleanup QR temp file
    if os.path.exists(qr_path):
        os.remove(qr_path)

    return FileResponse(pdf_filename, media_type="application/pdf", filename=pdf_filename)
