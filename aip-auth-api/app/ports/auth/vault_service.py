from abc import ABC, abstractmethod
from typing import Dict, Any

class VaultServicePort(ABC):
    @abstractmethod
    async def get_secret(self, path: str) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    async def verify_permission(self, user_id: str, resource: str, action: str) -> bool:
        pass
