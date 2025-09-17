from sqlalchemy import Column, String, Integer, Text
from app.db import Base

class DCARecord(Base):
    __tablename__ = "dca_records"

    id = Column(Integer, primary_key=True, index=True)
    dca_id = Column(String, unique=True, index=True)
    product_id = Column(Integer, nullable=False)
    artwork_name = Column(String, nullable=False)
    artist_name = Column(String, nullable=False)
    artist_scan_hash = Column(String, nullable=False)
    signed_json = Column(Text, nullable=False)
    consumer_scan_hash = Column(String, nullable=True)
    is_verified = Column(String, default="Pending")
