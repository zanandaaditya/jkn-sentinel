from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.claim_router import router as claim_router
from app.routers.investigator_router import router as investigator_router

from app.services.sla_runner import (
    start_sla_scheduler,
    stop_sla_scheduler
)
app = FastAPI(
    title="JKN Sentinel API"
)
@app.on_event("startup")
async def startup_background_jobs():

    await start_sla_scheduler()


@app.on_event("shutdown")
async def shutdown_background_jobs():

    await stop_sla_scheduler()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(claim_router)
app.include_router(investigator_router)