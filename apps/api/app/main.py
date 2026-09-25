from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from routers.dashboard_router import router as dashboard_router

from routers.claim_router import router as claim_router



app = FastAPI()



# =========================
# ROUTERS
# =========================


app.include_router(
    dashboard_router
)


app.include_router(
    claim_router
)





# =========================
# CORS
# =========================


app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],

)