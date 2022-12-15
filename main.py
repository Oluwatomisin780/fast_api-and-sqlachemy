from typing import Optional
from fastapi import FastAPI 
from pydantic import BaseModel
app  = FastAPI()

@app.get('/')
def index():
    return {
        'data':{
            'tomi':'oluwatomisin',
            'name':'good',
            'food':"gogg"
        }
    }  

#Query parameter
@app.get('/blog')
def index(limit,published:bool,sort:Optional[str]=None):
    if published:
        return {'data':f'{limit}published blogs from the db'}
    else:
        return {'data':f'{limit} blogs from the db'}
@app.get('/{id}')
def about(id):
    return{'data':id}

class Blog(BaseModel):
    title:str
    body:str
    published:Optional[bool]=True
@app.post('/blog')
def create_blog(blog:Blog):
    return {'data':f"blog is created at with title as {blog.title}"}