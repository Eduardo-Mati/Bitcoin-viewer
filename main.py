from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import userRouter
from schemas import userSchema


app = FastAPI()

origins = [
    "http://localhost"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#para rodar o código use o comando: uvicorn main:app --reload

app.include_router(userRouter.router)


