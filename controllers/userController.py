from database import users_collection
from bson import ObjectId
from schemas.userSchema import user
from fastapi import HTTPException
from passlib.context import CryptContext
from services.authMIddleware import create_access_token
from datetime import timedelta

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


async def create(user_data: user):
    """Criar um novo usuário"""

    if await users_collection.find_one({"email": user_data.email}):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    
    user_data.password = user_data.password.strip()
    if len(user_data.password) < 3 or len(user_data.password.encode('utf-8')) > 72:
        raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 3 caracteres")
    else:
        try:
            hashed_password = pwd_context.hash(user_data.password)
            await users_collection.insert_one(
                {
                    "name": user_data.name,
                    "email": user_data.email,
                    "password": hashed_password,
                }
            )
            return {"message": "Usuário criado com sucesso"}
            
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

async def getAll():
    """Obter todos os usuários"""
    try:
        users = await users_collection.find().to_list(length=None)
        if users == []:
            return [
                {"message": "Nenhum usuário encontrado"}
            ]
        else:
            return [
                {k: v for k, v in user.items() if k not in {"_id", "password"}}
                for user in users
            ]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


async def getOne(email: str):
    """Obter um usuário por email"""
    try:
        user = await users_collection.find_one({"email": email})
        if not user:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {k: v for k, v in user.items() if k not in {"_id", "password"}}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

async def updateOne(email: str, user_data: user):
    """Atualizar um usuário"""
    try:
        update_payload = user_data.model_dump()
        update_payload["password"] = pwd_context.hash(user_data.password)

        result = await users_collection.update_one(
            {"email": email},
            {"$set": update_payload}
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
        user_data = await users_collection.find_one({"email": credentials.get("email")})
        if not user_data:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")

        # Verifica se a senha enviada confere com o hash armazenado
        if not pwd_context.verify(credentials.get("password", ""), user_data.get("password", "")):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")
        
        # Cria o token JWT
        access_token = create_access_token(
            data={"sub": user_data.get("email")},
            expires_delta=timedelta(hours=1)
        )
        
        return {
            "access_token": access_token,
            "email": user_data.get("email"),
            "message": "Login realizado com sucesso"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))