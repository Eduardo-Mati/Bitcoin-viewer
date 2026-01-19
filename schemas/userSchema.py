from pydantic import BaseModel

class user(BaseModel):
    name: str
    email: str
    password: str