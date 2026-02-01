from fastapi import APIRouter
from controllers import userController
from schemas.userSchema import user

router = APIRouter()

@router.delete('/{email}')
async def delete_one(email: str):
	return await userController.deleteOne(email)

@router.get('/{email}')
async def get_one(email: str):
	return await userController.getOne(email)

@router.put('/{email}')
async def update_one(email: str, user_data: user):
	return await userController.updateOne(email, user_data)

@router.get('/')
async def get_all():
	return await userController.getAll()

@router.post('/login')
async def login(credentials: dict):
	return await userController.login(credentials)

@router.post('/register')
async def create(user_data: user):
	return await userController.create(user_data)
