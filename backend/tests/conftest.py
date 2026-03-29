import os

from cryptography.fernet import Fernet

# Set env vars before any backend module is imported
os.environ.setdefault("DATABASE_URL", "postgresql+asyncpg://test:test@localhost/testdb")
os.environ.setdefault("REDIS_URL", "redis://localhost:6379")
os.environ.setdefault("JWT_SECRET", "test-jwt-secret-key-minimum-32-chars-ok!!")
os.environ.setdefault("ENCRYPTION_KEY", Fernet.generate_key().decode())
os.environ.setdefault("OPENAI_API_KEY", "test-openai-key")

os.environ.setdefault("GEMINI_API_KEY", "test-gemini-key")
