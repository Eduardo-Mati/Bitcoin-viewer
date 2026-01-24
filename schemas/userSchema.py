from pydantic import BaseModel, field_validator

class user(BaseModel):
    name: str
    email: str
    password: str

    