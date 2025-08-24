from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    # embedding será enviado como base64 string
    embedding: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True
