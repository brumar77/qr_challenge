from fastapi import APIRouter, Depends

from middleware.security import get_current_user


admin_routes = APIRouter(
    prefix="/admin",
    tags=["admin"],
    dependencies=[Depends(get_current_user)],
)

