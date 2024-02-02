import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIAL_SECRET_KEY = os.getenv("CREDENTIAL_SECRET_KEY", "")
CREDENTIAL_ALGORITHM = os.getenv("CREDENTIAL_ALGORITHM", "")

DB_CONFIG = {
    "rdb": os.getenv("RDB", "postgresql+asyncpg"),
    "db_user": os.getenv("DB_USER", "junseokang"),
    "db_password": os.getenv("DB_PASSWORD", ""),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432"),
    "db": os.getenv("DB", "postgres"),
}

SITE_ENV = os.getenv("SITE_ENV", "local")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
