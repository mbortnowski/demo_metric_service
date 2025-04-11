from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.di.containers import Container
from app.api.routes import auth, ml_models

@asynccontextmanager
async def lifespan(app: FastAPI):
    container = Container()
    
    await container.oracle_repository().connect()
    
    await container.kafka_producer().start()
    
    await container.kafka_consumer().start()
    async def handle_message(message):
        print(f"Recived message: {message}")
    
    await container.kafka_consumer().subscribe(handle_message)
    
    yield
    print("Shutting down application...")
    await container.kafka_producer().stop()
    
    await container.kafka_consumer().stop()

def create_app() -> FastAPI:
    container = Container()
    
    app = FastAPI(
        title=container.config().app_name,
        description="Auth API",
        version="1.0.0",
        lifespan=lifespan
    )
    
    app.include_router(auth.router, prefix="/api", tags=["auth"])
    app.include_router(ml_models.router, prefix="/api", tags=["ml_models"])
    
    return app

app = create_app()
