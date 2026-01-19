from database import users_collection
from bson import ObjectId
from schemas.userSchema import user
from fastapi import HTTPException

async def create(user_data: user):
    """Criar um novo usuário"""
    try:
        result = await users_collection.insert_one(user_data.dict())
        return {"email": user_data.email, "message": "Usuário criado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def getAll():
    """Obter todos os usuários"""
    try:
        users = await users_collection.find().to_list(length=None)
        return [{k: v for k, v in user.items() if k != "_id"} for user in users]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def getOne(email: str):
    """Obter um usuário por email"""
    try:
        user = await users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {k: v for k, v in user.items() if k != "_id"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def updateOne(email: str, user_data: user):
    """Atualizar um usuário"""
    try:
        result = await users_collection.update_one(
            {"email": email},
            {"$set": user_data.dict()}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"message": "Usuário atualizado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def deleteOne(email: str):
    """Deletar um usuário"""
    try:
        result = await users_collection.delete_one({"email": email})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"message": "Usuário deletado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def login(credentials: dict):
    """Fazer login do usuário"""
    try:
        user = await users_collection.find_one({"email": credentials.get("email")})
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
        return {
            "email": user.get("email"),
            "message": "Login realizado com sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))