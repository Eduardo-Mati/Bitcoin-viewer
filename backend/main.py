from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import userRouter
from schemas import userSchema
from routers import cryptoRouter
import os

app = FastAPI()

raw_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:7463,https://bitcoin-viewer.vercel.app",
)
allowed_origins = [origin.strip() for origin in raw_origins.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https://.*\.vercel\.app$",
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#para rodar o código use o comando: docker-compose up --build

app.include_router(userRouter.router, prefix="/api/user", tags=["user"])
app.include_router(cryptoRouter.router, prefix="/crypto", tags=["crypto"])