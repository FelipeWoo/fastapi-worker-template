from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.boot import boot
from app.workers.billing_ticket.routes import router as billing_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    config = boot("main")
    app.state.config = config
    print(f"Application: {config.name}")
    yield
    # shutdown logic here if needed


app = FastAPI(
    lifespan=lifespan,
    title="Basic API template",
    description="Basic configurations using FastAPI.",
    version="0.1.0",
)

@app.get("/health")
def health():
    return {"status": "ok"}


app.include_router(billing_router)
