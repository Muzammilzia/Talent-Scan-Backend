from typing import Union
from dotenv import load_dotenv
from fastapi import FastAPI, Request, status
from app.api.v1.routers import api_router
from fastapi.middleware.cors import CORSMiddleware
from .db.base import connect_to_database
from starlette.responses import JSONResponse
from app.utils.jwt import verify_jwt_token

load_dotenv()

app = FastAPI()

# Allow CORS from anywhere
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.middleware("http")
async def jwt_auth_middleware(request: Request, call_next):
    # Skip specific routes (e.g., login, signup)
    if request.url.path in ["/api/v1/candidate/sign-in", "/api/v1/candidate/sign-up"]:
        return await call_next(request)

    # skip if request is cors preflight request
    if request.method == "OPTIONS":
        return await call_next(request)

    # get authorization header
    authorization: str = request.headers.get("authorization") or request.headers.get("Authorization")
    
    if not authorization:
        return JSONResponse(
            {"detail": "Authorization header missing"},
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    
    token = authorization.split(" ")[1]
    payload = verify_jwt_token(token)
    request.state.user = payload  # Attach the user payload to the request state
    
    return await call_next(request)

connect_to_database()

# Include the API router
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return "Hello World!"