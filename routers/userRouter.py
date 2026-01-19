from flask import Blueprint
from controllers import userController

router = Blueprint('users', __name__)

@router.route('/<id>', methods=['DELETE'])
def delete_one(id):
	return userController.deleteOne(id)

@router.route('/<id>', methods=['GET'])
def get_one(id):
	return userController.getOne(id)

@router.route('/<id>', methods=['PUT'])
def update_one(id):
	return userController.updateOne(id)

@router.route('/', methods=['GET'])
def get_all():
	return userController.getAll()

@router.route('/login', methods=['POST'])
def login():
	return userController.login()

@router.route('/register', methods=['POST'])
def create():
	return userController.create()
