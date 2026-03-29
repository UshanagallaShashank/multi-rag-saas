import bcrypt

def hash_password(password: str) -> str:
    # Hash password using bcrypt with auto-generated salt
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    # Verify plain password against bcrypt hash
    return bcrypt.checkpw(plain.encode(), hashed.encode())
