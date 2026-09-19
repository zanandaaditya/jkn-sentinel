from fastapi import FastAPI

from app.routers import health


app = FastAPI(

    title="JKN SENTINEL API",

    version="0.1.0"

)



app.include_router(

    health.router

)


@app.get("/")

def root():

    return {

        "message":

        "JKN SENTINEL API Running"

    }
