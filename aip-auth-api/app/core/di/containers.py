from dependency_injector import containers, providers
from app.config.models import AppSettings
from app.adapters.auth.vault_service import HashiCorpVaultAdapter
from app.adapters.storage.oracle_repository import OracleDbAdapter
from app.adapters.messaging.kafka_producer import KafkaProducerAdapter
from app.adapters.messaging.kafka_consumer import KafkaConsumerAdapter
from app.domain.services.auth_service import AuthService
from app.domain.services.ml_model_service import MLModelService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.api"])
    
    config = providers.Singleton(AppSettings)
    
    vault_service = providers.Singleton(
        HashiCorpVaultAdapter,
        settings=config.provided.vault
    )
    
    oracle_repository = providers.Singleton(
        OracleDbAdapter,
        settings=config.provided.db
    )
    
    kafka_producer = providers.Singleton(
        KafkaProducerAdapter,
        settings=config.provided.kafka
    )
    
    kafka_consumer = providers.Singleton(
        KafkaConsumerAdapter,
        settings=config.provided.kafka
    )
    
    auth_service = providers.Singleton(
        AuthService,
        vault_service=vault_service
    )
    
    ml_model_service = providers.Singleton(
        MLModelService,
        repository=oracle_repository,
        kafka_producer=kafka_producer,
        kafka_settings=config.provided.kafka
    )
