from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    dsn: str = Field(..., alias="DB_DSN")
    user: str = Field(..., alias="DB_USER")
    password: str = Field(..., alias="DB_PASSWORD")
    min_size: int = Field(1, alias="DB_POOL_MIN_SIZE")
    max_size: int = Field(10, alias="DB_POOL_MAX_SIZE")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

class KafkaSettings(BaseSettings):
    bootstrap_servers: str = Field(..., alias="KAFKA_BOOTSTRAP_SERVERS")
    consumer_group: str = Field(..., alias="KAFKA_CONSUMER_GROUP")
    consumer_topic: str = Field(..., alias="KAFKA_CONSUMER_TOPIC")
    producer_topic: str = Field(..., alias="KAFKA_PRODUCER_TOPIC")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

class VaultSettings(BaseSettings):
    url: str = Field(..., alias="VAULT_URL")
    token: str = Field(..., alias="VAULT_TOKEN")
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

class AppSettings(BaseSettings):
    app_name: str = Field("ML Models Management API", alias="APP_NAME")
    debug: bool = Field(False, alias="DEBUG")
    db: DatabaseSettings = DatabaseSettings()
    kafka: KafkaSettings = KafkaSettings()
    vault: VaultSettings = VaultSettings()
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )
