from pydantic import BaseModel

class AuthRequest(BaseModel):
    user_id: str
    resource: str
    action: str

class AuthResponse(BaseModel):
    allowed: bool
    message: str

