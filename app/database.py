from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from urllib.parse import quote_plus
from dotenv import load_dotenv

load_dotenv()

# Raw password
DB_USER = "root"
DB_PASS = "Manira2909*"  # your actual password with *
DB_HOST = "localhost"
DB_NAME = "credit_card_db"

# Auto encode the password
ENCODED_PASS = quote_plus(DB_PASS)

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{ENCODED_PASS}@{DB_HOST}:3306/{DB_NAME}"

# Or if you use .env, this also works:
# DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

print(f"Connected to: {DB_NAME} with encoded password")