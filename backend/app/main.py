from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.endpoints import humidity, plant
from db.database import engine, Base
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
import time


def ensure_timestamp_is_timestamptz():
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT data_type 
            FROM information_schema.columns 
            WHERE table_name = 'humidity_readings' 
              AND column_name = 'timestamp';
        """))
        column_type = result.scalar()
        
        if column_type != "timestamp with time zone":
            print("⏳ Fixing 'timestamp' column type...")
            conn.execute(text("""
                ALTER TABLE humidity_readings
                ALTER COLUMN timestamp TYPE TIMESTAMPTZ
                USING timestamp::timestamptz;
            """))
            print("✅ 'Timestamp' column type fixed.")
        else:
            print("✅ 'Timestamp' column is already correct.")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
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
            print("✅ DB is ready!!")
            return
        except OperationalError:
            print(f"⏳ Attempt {i + 1}/{max_tries} - DB is not ready. Waiting {delay}s...")
            time.sleep(delay)
    raise Exception("🚨 Failed to connect to the database after multiple attempts.")


wait_for_db()
Base.metadata.create_all(bind=engine)
ensure_timestamp_is_timestamptz()

app.include_router(humidity.router)
app.include_router(plant.router)