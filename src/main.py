from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from middleware.auth import authenticate

from controllers.user_controller import user_router
from controllers.auth import login_router

app = FastAPI()
app.include_router(user_router)
app.include_router(login_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    return await authenticate(request, call_next)
