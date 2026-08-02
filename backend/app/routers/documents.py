from fastapi import APIRouter

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)

@router.post("/upload")
def upload():
    return {"message": "Document uploaded successfully"}