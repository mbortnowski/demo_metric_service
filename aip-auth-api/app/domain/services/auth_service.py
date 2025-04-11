from app.ports.auth.vault_service import VaultServicePort

class AuthService:
    def __init__(self, vault_service: VaultServicePort):
        self.vault_service = vault_service
    
    async def verify_user_permission(self, user_id: str, resource: str, action: str) -> bool:
        return await self.vault_service.verify_permission(user_id, resource, action)
