from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import userRouter
from schemas import userSchema
from database import close_mongo_connection


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

app.use(mid)
# Event handlers para conexão com MongoDB
@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

#para rodar o código use o comando: uvicorn main:app --reload

app.include_router(userRouter.router)


