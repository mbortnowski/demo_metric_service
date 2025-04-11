from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class MLModelBase(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    version: str
    created_at: datetime
    updated_at: Optional[datetime] = None

class MLModelResponse(MLModelBase):
    pass

class MLModelsListResponse(BaseModel):
    models: List[MLModelResponse]
