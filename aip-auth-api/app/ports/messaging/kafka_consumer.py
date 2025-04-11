from abc import ABC, abstractmethod
from typing import Callable, Awaitable, Dict, Any

class KafkaConsumerPort(ABC):
    @abstractmethod
    async def start(self) -> None:
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        pass
    
    @abstractmethod
    async def subscribe(self, callback: Callable[[Dict[str, Any]], Awaitable[None]]) -> None:
        pass
