import redis.asyncio as Redis
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi import Depends
from decouple import config

REDIS_URI = config("REDIS_URI")
REGISTER_REQ_RATE = int(config("REGISTER_REQ_RATE"))
REGISTER_TIME_WINDOW = int(config("REGISTER_TIME_WINDOW"))

LOGIN_REQ_RATE = int(config("LOGIN_REQ_RATE"))
LOGIN_TIME_WINDOW = int(config("LOGIN_TIME_WINDOW"))

async def init_rate_limiter():
    redis = Redis.from_url(REDIS_URI, encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)



login_limiter = RateLimiter(times=LOGIN_REQ_RATE, seconds=LOGIN_TIME_WINDOW)
register_limiter = RateLimiter(times=REGISTER_REQ_RATE, seconds=REGISTER_TIME_WINDOW)