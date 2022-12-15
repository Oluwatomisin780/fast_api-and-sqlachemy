import email
import re
from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import models, schemas
from sqlalchemy.orm  import Session
from .database import SesssionLocal, engine
from passlib.context import CryptContext
app = FastAPI()

models.Base.metadata.create_all(engine)
def get_db():
    db= SesssionLocal()
    try:
        yield db
    finally:
        db.close

@app.post('/blog',status_code=status.HTTP_201_CREATED)
def create_blog(request:schemas.Blog,db:Session= Depends(get_db)):
    new_blog= models.Blog(title = request.title,body = request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog
@app.get('/blog',status_code=status.HTTP_200_OK,response_model=List[schemas.Show_Blog])
def get_all_blog(db:Session= Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}',status_code=status.HTTP_200_OK,response_model=schemas.Show_Blog)
def get_blog_by_id(id,response:Response,db:Session=Depends(get_db)):
    blog =db.query(models.Blog).filter(models.Blog.id ==id).first()
    if not blog:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f'Blog with {id} not found'   
        )
    return blog


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request:schemas.Blog,db:Session= Depends(get_db)):
    blog= db.query(models.Blog).filter(models.Blog.id)
    if not blog.first():
        raise HTTPException(
            status_code = 404,
            detail= f'Blog with {id} does not exist '
        )
    blog.update(request)
    db.commit()

@app.delete('blog/{id}',status_code=status.HTTP_200_OK)
def delete_blog(id,db:Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(
            status_code= 404,
            detail= f'Blog with {id} does not exist'
        )
    blog.delete(synchronize_session=False)
    db.commit()
    return  'deleted'


## User 

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")
@app.post('/user')
def create_user(request:schemas.User,db:Session= Depends(get_db)):
    hashed_password = pwd_cxt.hash(request.password)
    new_user = models.User(name=request.name,email = request.email,password= hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user