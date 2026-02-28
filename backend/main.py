from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import userRouter
from schemas import userSchema
from routers import cryptoRouter

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://bitcoin-viewer.vercel.app"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#para rodar o código use o comando: docker-compose up --build

app.include_router(userRouter.router, prefix="/api/user", tags=["user"])
app.include_router(cryptoRouter.router, prefix="/crypto", tags=["crypto"])