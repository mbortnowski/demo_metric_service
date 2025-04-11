import oracledb
from typing import Dict, Any, List, Optional
from app.ports.storage.oracle_repository import OracleRepositoryPort
from app.config.models import DatabaseSettings

class OracleDbAdapter(OracleRepositoryPort):
    def __init__(self, settings: DatabaseSettings):
        self.settings = settings
        self.pool = None
    
    async def connect(self) -> None:
        if self.pool is None:
            self.pool = oracledb.create_pool(
                user=self.settings.user,
                password=self.settings.password,
                dsn=self.settings.dsn,
                min=self.settings.min_size,
                max=self.settings.max_size
            )
    
    async def execute(self, query: str, params: Dict[str, Any] = None) -> None:
        if not self.pool:
            await self.connect()
        
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, params or {})
                await connection.commit()
    
    async def fetch_one(self, query: str, params: Dict[str, Any] = None) -> Optional[Dict[str, Any]]:
        if not self.pool:
            await self.connect()
        
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, params or {})
                result = await cursor.fetchone()
                if result:
                    columns = [col[0] for col in cursor.description]
                    return dict(zip(columns, result))
                return None
    
    async def fetch_all(self, query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        if not self.pool:
            await self.connect()
        
        async with self.pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute(query, params or {})
                results = await cursor.fetchall()
                if results:
                    columns = [col[0] for col in cursor.description]
                    return [dict(zip(columns, row)) for row in results]
                return []
