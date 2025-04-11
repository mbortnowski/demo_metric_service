from fastapi import APIRouter, Depends, HTTPException
from app.api.models.ml_models import MLModelResponse, MLModelsListResponse
from app.domain.services.ml_model_service import MLModelService
from app.domain.services.auth_service import AuthService
from dependency_injector.wiring import inject, Provide
from app.core.di.containers import Container

router = APIRouter()

@router.get("/models", response_model=MLModelsListResponse)
@inject
async def list_models(
    user_id: str,
    ml_model_service: MLModelService = Depends(Provide[Container.ml_model_service]),
    auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    # Weryfikacja uprawnień
    allowed = await auth_service.verify_user_permission(user_id, "models", "list")
    if not allowed:
        raise HTTPException(status_code=403, detail="Brak dostępu")
    
    models = await ml_model_service.list_models(user_id)
    return MLModelsListResponse(models=[MLModelResponse(**model) for model in models])

@router.get("/models/{model_id}", response_model=MLModelResponse)
@inject
async def get_model(
    model_id: str,
    user_id: str,
    ml_model_service: MLModelService = Depends(Provide[Container.ml_model_service]),
    auth_service: AuthService = Depends(Provide[Container.auth_service])
):
    # Weryfikacja uprawnień
    allowed = await auth_service.verify_user_permission(user_id, f"models/{model_id}", "read")
    if not allowed:
        raise HTTPException(status_code=403, detail="Brak dostępu")
    
    model = await ml_model_service.get_model_info(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model nie znaleziony")
    
    # Powiadomienie o dostępie do modelu
    await ml_model_service.notify_model_access(user_id, model_id)
    
    return MLModelResponse(**model)
