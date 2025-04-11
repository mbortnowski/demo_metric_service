from aiokafka import AIOKafkaProducer
import json
from typing import Dict, Any
from app.ports.messaging.kafka_producer import KafkaProducerPort
from app.config.models import KafkaSettings

class KafkaProducerAdapter(KafkaProducerPort):
    def __init__(self, settings: KafkaSettings):
        self.settings = settings
        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
    
    async def start(self) -> None:
        await self.producer.start()
    
    async def stop(self) -> None:
        await self.producer.stop()
    
    async def send_message(self, topic: str, message: Dict[str, Any]) -> None:
        await self.producer.send_and_wait(topic, message)
