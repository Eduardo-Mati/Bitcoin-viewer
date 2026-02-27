from pydantic import BaseModel, field_validator


def _normalize_email(value: str) -> str:
    normalized = value.strip().lower()
    if "@" not in normalized:
        raise ValueError("Email inválido")
    return normalized


def _normalize_password(value: str) -> str:
    normalized = value.strip()
    if len(normalized) < 3 or len(normalized.encode("utf-8")) > 72:
        raise ValueError("Senha deve ter pelo menos 3 caracteres")
    return normalized


class UserBase(BaseModel):
    name: str
    email: str

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Nome é obrigatório")
        return normalized

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return _normalize_email(value)


class CreateUser(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return _normalize_password(value)


class UpdateUser(UserBase):
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        return _normalize_password(value)


class LoginCredentials(BaseModel):
    email: str
    password: str

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        return _normalize_email(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("Senha é obrigatória")
        return normalized


class user(CreateUser):
    pass

    