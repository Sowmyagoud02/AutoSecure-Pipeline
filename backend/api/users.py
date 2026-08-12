from fastapi import APIRouter, Depends

from backend.models.user import User
from backend.security.dependencies import get_current_user, require_roles
from backend.security.roles import UserRole

from backend.schemas.user import UserResponse


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.get("/admin-test")
def admin_test(
    current_user: User = Depends(require_roles(UserRole.ADMIN)),
):
    return {
        "message": "Admin access granted",
        "username": current_user.username,
    }