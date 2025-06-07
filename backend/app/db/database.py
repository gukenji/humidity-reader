from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# DATABASE_URL = "mysql+pymysql://usuario:senha@localhost:3306/nomedobanco"
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://usuario:senha@localhost:5432/nomedobanco")

# DATABASE_URL = "sqlite:///./app.db"  # Cria o arquivo app.db na raiz do projeto
engine = create_engine(DATABASE_URL)

# engine = create_engine(
#     DATABASE_URL, connect_args={"check_same_thread": False}  # só no SQLite
# )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency para injetar session no FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()