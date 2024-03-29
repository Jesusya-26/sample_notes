from fastapi import Request, Response
from fastapi_cache import FastAPICache
from typing import Optional


def my_key_builder(
 func,
 namespace: Optional[str] = "",
 request: Request = None,
 response: Response = None,
 *args,
 **kwargs,
):
    prefix = FastAPICache.get_prefix()
    cache_key = f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{args}:{kwargs}"
    return cache_key
