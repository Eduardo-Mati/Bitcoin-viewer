from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import userRouter
from schemas import userSchema
from routers import cryptoRouter

app = FastAPI()

origins = [
    "http://localhost","http://127.0.0.1:8000","http://localhost:3000","http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#para rodar o código use o comando: docker-compose up --build

app.include_router(userRouter.router, prefix="/api/user", tags=["user"])
app.include_router(cryptoRouter.router, prefix="/crypto", tags=["crypto"])