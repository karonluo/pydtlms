from fastapi import APIRouter, Depends

from app.core.rbac import require_permissions
from app.schemas.auth import Principal
from app.schemas.dashboard import DashboardOverview
from app.services.dashboard_service import get_dashboard_overview


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/overview", response_model=DashboardOverview)
def overview(principal: Principal = Depends(require_permissions("dashboard:read"))) -> DashboardOverview:
    return get_dashboard_overview()
