# app/utils.py
import os, socket
from app.config import PUBLIC_DOMAIN

def get_local_ip() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    finally:
        s.close()

def build_image_url(filename: str, port: int = 8000) -> str:
    """Builds the correct public URL for a file in /uploads"""
    filename = os.path.basename(filename)
    if PUBLIC_DOMAIN:
        return f"https://{PUBLIC_DOMAIN}/uploads/{filename}"
    return f"http://{get_local_ip()}:{port}/uploads/{filename}"
