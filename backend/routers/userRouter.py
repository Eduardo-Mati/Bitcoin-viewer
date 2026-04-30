from fastapi import APIRouter, Request
from controllers import userController
from schemas.userSchema import CreateUser, UpdateUser, LoginCredentials
from services.rateLimiter import limiter

router = APIRouter()


@router.delete('/{email}')
@limiter.limit("5/minute")
async def delete_one(request: Request, email: str):
	return await userController.deleteOne(email)

@router.get('/{email}')
@limiter.limit("5/minute")
async def get_one(request: Request, email: str):
	return await userController.getOne(email)

@router.put('/{email}')
@limiter.limit("5/minute")
async def update_one(request: Request, email: str, user_data: UpdateUser):
	return await userController.updateOne(email, user_data)

@router.get('/')
@limiter.limit("5/minute")
async def get_all(request: Request):
	return await userController.getAll()

@router.post('/login')
@limiter.limit("10/minute")
async def login(request: Request, credentials: LoginCredentials):
	return await userController.login(credentials)

@router.post('/register')
@limiter.limit("5/minute")
async def create(request: Request, user_data: CreateUser):
	return await userController.create(user_data)
