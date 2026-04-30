from database import users_collection
from schemas.userSchema import CreateUser, UpdateUser, LoginCredentials
from fastapi import HTTPException
from services.authMIddleware import create_access_token, hash_password, verify_password
from datetime import timedelta

def _sanitize_user(user_data: dict) -> dict:
    return {key: value for key, value in user_data.items() if key not in {"_id", "password"}}


async def create(user_data: CreateUser):
    """Criar um novo usuário"""
    try:
        if await users_collection.find_one({"email": user_data.email}):
            raise HTTPException(status_code=400, detail="Email já cadastrado")

        await users_collection.insert_one(
            {
                "name": user_data.name,
                "email": user_data.email,
                "password": hash_password(user_data.password),
            }
        )
        return {"message": "Usuário criado com sucesso"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao criar usuário")

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
                _sanitize_user(user_item)
                for user_item in users
            ]
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar usuários")


async def getOne(email: str):
    """Obter um usuário por email"""
    try:
        user_data = await users_collection.find_one({"email": email})
        if not user_data:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return _sanitize_user(user_data)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao buscar usuário")

async def updateOne(email: str, user_data: UpdateUser):
    """Atualizar um usuário"""
    try:
        update_payload = user_data.model_dump()
        update_payload["password"] = hash_password(user_data.password)

        if update_payload["email"] != email:
            existing_user = await users_collection.find_one({"email": update_payload["email"]})
            if existing_user:
                raise HTTPException(status_code=400, detail="Email já cadastrado")

        result = await users_collection.update_one(
            {"email": email},
            {"$set": update_payload}
        )
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"message": "Usuário atualizado com sucesso"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao atualizar usuário")

async def deleteOne(email: str):
    """Deletar um usuário"""
    try:
        result = await users_collection.delete_one({"email": email})
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Usuário não encontrado")
        return {"message": "Usuário deletado com sucesso"}
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao deletar usuário")

async def login(credentials: LoginCredentials):
    """Fazer login do usuário"""
    try:
        user_data = await users_collection.find_one({"email": credentials.email})

        if not user_data or not verify_password(credentials.password, user_data.get("password", "")):
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

        access_token = create_access_token(
            data={"sub": user_data.get("email")},
            expires_delta=timedelta(hours=1)
        )

        return {
            "access_token": access_token,
            "email": user_data.get("email"),
            "message": "Login realizado com sucesso"
        }
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="Erro ao realizar login")