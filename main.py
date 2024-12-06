from fastapi import FastAPI, Request, status
from slowapi.errors import RateLimitExceeded
from starlette.responses import JSONResponse

from src.api import utils, contacts, auth, users

app = FastAPI()

@app.exception_handler(RateLimitExceeded)
async def rate_limit_exception_handler(request: Request,
                                       exc: RateLimitExceeded):
    return JSONResponse(status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                        content={"detail": "Too many requests"})
app.include_router(utils.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(auth.router, prefix='/api')

app.include_router(users.router, prefix='/api')

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)