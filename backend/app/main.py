from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import humidity
from db.database import engine, Base
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from db.database import engine, Base
from db import models  # ou onde estiver seu HumidityReading etc.
import time


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,           # Ou ["*"] se quiser liberar tudo no dev
    allow_credentials=True,
    allow_origin_regex=r"^http://(localhost|127\.0\.0\.1|192\.168\.\d{1,3}\.\d{1,3}|10\.\d{1,3}\.\d{1,3}\.\d{1,3})(:\d+)?$",
    allow_methods=["*"],
    allow_headers=["*"],
)


def wait_for_db(max_tries=10, delay=2):
    for i in range(max_tries):
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print("✅ Banco de dados pronto!")
            return
        except OperationalError as e:
            print(f"⏳ Tentativa {i+1}/{max_tries} - Banco ainda não pronto. Esperando {delay}s...")
            time.sleep(delay)
    raise Exception("🚨 Falha ao conectar ao banco de dados após várias tentativas.")



wait_for_db()
Base.metadata.create_all(bind=engine)

app.include_router(humidity.router)