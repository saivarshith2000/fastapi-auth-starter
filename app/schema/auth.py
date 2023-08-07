from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class UserSchema(BaseModel):
    email: str
    first_name: str
    last_name: str

    class Config:
        from_attributes = True

class SignUpSchema(UserSchema):
    password: str