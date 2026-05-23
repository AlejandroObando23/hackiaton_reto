from fastapi import FastAPI
from contextlib import asynccontextmanager
import config
from routers.SanaBotRouter import router as sana_bot_router
from database.mongodb import connect_to_mongo, close_mongo_connection
from services.SanaBotService import initialize_chatbot
from fastapi.middleware.cors import CORSMiddleware
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    connect_to_mongo()
    print("[START] Servidor levantado, inicializando servicios en background...")

    async def init_services():
        print("[WAIT] Iniciando carga de modelos...")
        await asyncio.to_thread(initialize_chatbot)
        print("[OK] Modelos de IA listos")

    asyncio.create_task(init_services())

    yield

    print("[STOP] Apagando servidor...")
    close_mongo_connection()

app = FastAPI(title="MediByte API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

import os
from fastapi.staticfiles import StaticFiles

app.include_router(sana_bot_router)

if os.path.exists("static"):
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
else:
    @app.get("/")
    def read_root():
        return {"message": "MediByte API is running (Frontend not built/found)"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
