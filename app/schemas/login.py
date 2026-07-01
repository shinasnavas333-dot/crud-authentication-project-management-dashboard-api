from pydantic import BaseModel

class LoginRequest(BaseModel):
    uuid: str
    password: str
