from fastapi import APIRouter, Depends

from app.auth.permissions import require_role


router = APIRouter(
    prefix="/admin",
    tags=["admin"]
)


@router.get("/")
def admin_test(
    current_user = Depends(require_role("admin"))
):

    return {
        "message": "Welcome admin",
        "username": current_user.username
    }