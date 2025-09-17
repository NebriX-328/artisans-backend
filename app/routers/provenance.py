# backend/app/routers/provenance.py
from fastapi import APIRouter
import uuid

router = APIRouter()

# In-memory ledger for now (later can be DB or blockchain)
ledger = {}

@router.post("/register")
def register_provenance(product_id: str):
    unique_id = str(uuid.uuid4())
    ledger[product_id] = unique_id
    return {
        "message": "Provenance record created",
        "product_id": product_id,
        "provenance_id": unique_id
    }

@router.get("/ledger")
def get_ledger():
    return ledger
