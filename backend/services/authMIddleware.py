from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jwt import encode, decode, ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from typing import Optional
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
import os

load_dotenv()

# Esquema de segurança
security = HTTPBearer()

# Constants
SECRET = os.getenv("SECRET")
ALGORITHM = "HS256"
SECRET_KEY = os.getenv("SECRET")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def normalize_password(password: str) -> str:
    return password.strip()


def validate_password_policy(password: str) -> None:
    if len(password) < 3 or len(password.encode("utf-8")) > 72:
        raise HTTPException(status_code=400, detail="Senha deve ter pelo menos 3 caracteres")


def hash_password(password: str) -> str:
    normalized = normalize_password(password)
    validate_password_policy(normalized)
    return pwd_context.hash(normalized)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    normalized = normalize_password(plain_password)
    return pwd_context.verify(normalized, hashed_password)

# Função para criar token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Cria um token JWT"""
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=60)
    
    to_encode.update({"exp": expire})
    encoded_jwt = encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token_optional(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[str]:
    
    """Verifica token JWT - retorna None se não houver token"""
    if credentials is None:
        return None
    
    token = credentials.credentials
    
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return email
    
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


# Função para verificar token obrigatório
def verify_token_required(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """Verifica token JWT - retorna erro se não houver token"""
    token = credentials.credentials
    
    try:
        payload = decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        return email
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")
