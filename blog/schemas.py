from pydantic import BaseModel,EmailStr

class Blog(BaseModel):
    title:str
    body:str

class Show_Blog(BaseModel):
    title:str
    body: str
    class Config():
        orm_mode= True


class User(BaseModel):
    name:str
    email: str
    password:str