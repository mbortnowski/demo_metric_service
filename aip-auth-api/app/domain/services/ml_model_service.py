from typing import List, Dict, Any, Optional
from app.ports.storage.oracle_repository import OracleRepositoryPort
from app.ports.messaging.kafka_producer import KafkaProducerPort
from app.config.models import KafkaSettings

class MLModelService:
    def __init__(
        self, 
        repository: OracleRepositoryPort, 
        kafka_producer: KafkaProducerPort,
        kafka_settings: KafkaSettings
    ):
        self.repository = repository
        self.kafka_producer = kafka_producer
        self.kafka_settings = kafka_settings
    
    async def get_model_info(self, model_id: str) -> Optional[Dict[str, Any]]:
        query = "SELECT * FROM ml_models WHERE id = :id"
        return await self.repository.fetch_one(query, {"id": model_id})
    
    async def list_models(self, user_id: str) -> List[Dict[str, Any]]:
        query = """
        SELECT m.* 
        FROM ml_models m
        JOIN user_model_permissions p ON m.id = p.model_id
        WHERE p.user_id = :user_id
        """
        return await self.repository.fetch_all(query, {"user_id": user_id})
    
    async def notify_model_access(self, user_id: str, model_id: str) -> None:
        message = {
            "event_type": "model_access",
            "user_id": user_id,
            "model_id": model_id,
            "timestamp": "2025-04-07T20:51:00Z"
        }
        await self.kafka_producer.send_message(self.kafka_settings.producer_topic, message)
