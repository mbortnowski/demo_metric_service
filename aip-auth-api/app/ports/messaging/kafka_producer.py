from abc import ABC, abstractmethod
from typing import Dict, Any

class KafkaProducerPort(ABC):
    @abstractmethod
    async def start(self) -> None:
        pass
    
    @abstractmethod
    async def stop(self) -> None:
        pass
    
    @abstractmethod
    async def send_message(self, topic: str, message: Dict[str, Any]) -> None:
        pass
