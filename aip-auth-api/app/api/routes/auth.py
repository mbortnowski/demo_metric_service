from fastapi import APIRouter, Depends, HTTPException
from app.api.models.auth import AuthRequest, AuthResponse
from app.domain.services.auth_service import AuthService
from dependency_injector.wiring import inject, Provide
from app.core.di.containers import Container

router = APIRouter()

@router.post("/auth", response_model=AuthResponse)
@inject
async def verify_auth(
    request: AuthRequest,
    auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    allowed = await auth_service.verify_user_permission(
        request.user_id, request.resource, request.action
    )
    
    if allowed:
        return AuthResponse(allowed=True, message="Dostęp przyznany")
    else:
        return AuthResponse(allowed=False, message="Dostęp zabroniony")
