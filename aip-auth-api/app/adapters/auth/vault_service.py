import aiohttp
from typing import Dict, Any
from app.ports.auth.vault_service import VaultServicePort
from app.config.models import VaultSettings

class HashiCorpVaultAdapter(VaultServicePort):
    def __init__(self, settings: VaultSettings):
        self.settings = settings
        self.base_url = settings.url
        self.headers = {"X-Vault-Token": settings.token}
    
    async def get_secret(self, path: str) -> Dict[str, Any]:
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/v1/{path}"
            async with session.get(url, headers=self.headers) as response:
                if response.status != 200:
                    raise Exception(f"Failed to get secret from Vault: {await response.text()}")
                data = await response.json()
                return data.get("data", {})
    
    async def verify_permission(self, user_id: str, resource: str, action: str) -> bool:
        path = f"auth/permissions/{user_id}/{resource}/{action}"
        try:
            result = await self.get_secret(path)
            return result.get("allowed", False)
        except Exception:
            return False
