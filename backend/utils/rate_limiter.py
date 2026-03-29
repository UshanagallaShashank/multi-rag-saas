from fastapi import Request

from slowapi import Limiter

from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

def tenant_key(request: Request) -> str:
    # Rate-limit by tenant_id from JWT state, fall back to IP
    tenant_id = getattr(request.state, "tenant_id", None)
    return str(tenant_id) if tenant_id else get_remote_address(request)
