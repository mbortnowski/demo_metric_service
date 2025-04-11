from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional

class OracleRepositoryPort(ABC):
    @abstractmethod
    async def connect(self) -> None:
        pass
    
    @abstractmethod
    async def execute(self, query: str, params: Dict[str, Any] = None) -> None:
        pass
    
    @abstractmethod
    async def fetch_one(self, query: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        pass
    
    @abstractmethod
    async def fetch_all(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        pass
