from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.db import Base, engine
from app.routers import dispatch, verify, dca, provenance, dca_view

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Artisans API")

@app.get("/")
def root():
    return {"message": "Backend is running!"}

# ✅ Mount static uploads directory
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# ✅ Include routers
app.include_router(dispatch.router, prefix="/dispatch", tags=["Dispatch"])
app.include_router(verify.router, prefix="/verify", tags=["Verify"])
app.include_router(dca.router, prefix="/dca", tags=["DCA"])
app.include_router(provenance.router, prefix="/provenance", tags=["Provenance"])
app.include_router(dca_view.router)  # Make sure dca_view.py has router = APIRouter()
