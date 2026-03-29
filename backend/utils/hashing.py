from passlib.context import CryptContext

_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # Hash password using bcrypt
    return _ctx.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    # Verify plain password against bcrypt hash
    return _ctx.verify(plain, hashed)
