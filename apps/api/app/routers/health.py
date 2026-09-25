from fastapi import APIRouter

from sqlalchemy import text

from app.core.database import engine


router = APIRouter()



@router.get("/health")

def health_check():

    database_status="unknown"


    try:

        with engine.connect() as conn:

            conn.execute(text("SELECT 1"))

            database_status="connected"


    except Exception as e:
        database_status=str(e)



    return {

        "status":"ok",

        "application":

        "JKN SENTINEL API",

        "database":

        database_status

    }
