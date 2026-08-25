import os

POSTGRES = os.getenv("DATABASE_URL")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = os.getenv("PORT", 8000)

if not POSTGRES:
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "password")
    DB_NAME = os.getenv("DB_NAME", "songs")
    DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
    DB_PORT = os.getenv("DB_PORT", "5432")
    POSTGRES = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"