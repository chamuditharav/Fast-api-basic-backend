from fastapi import FastAPI

from routers import root
from routers.user import register, login


app = FastAPI()
URL_PREFIX = "/api/v1"

app.include_router(root.router, prefix= URL_PREFIX)
app.include_router(register.router, prefix= URL_PREFIX)
app.include_router(login.router, prefix= URL_PREFIX)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
