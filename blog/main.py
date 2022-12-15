from fastapi import FastAPI,Depends,status,Response,HTTPException
from . import models, schemas
from sqlalchemy.orm  import Session
from .database import SesssionLocal, engine
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
@app.get('/blog',status_code=200)
def get_all_blog(db:Session= Depends(get_db)):
    blogs=db.query(models.Blog).all()
    return blogs

@app.get('/blog/{id}')
def get_by_id(id,response:Response,db:Session=Depends(get_db)):
    blog =db.query(models.Blog).filter(models.Blog.id ==id).first()
    if not blog:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND,
            detail = f'Blog with {id} not found'   
        )
    return blog


@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED)
def update_blog(id,request:schemas.Blog,db:Session= Depends(get_db)):
    pass

@app.delete('blog/{id}',status_code=status.HTTP_200_OK)
def delete_blog(id,db:Session = Depends(get_db)):
    db.query(models.Blog).filter(models.Blog.id == id).delete(synchronize_session=False)
    db.commit()
    return  'deleted'