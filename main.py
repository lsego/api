from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from utils.jwt_manager import create_token
from fastapi.security import HTTPBearer
from config.database import  engine, Base
from middlewares.error_handler import ErrorHandler
from routers.movies import movie_router
# Creamos la variable
app = FastAPI()
app.title = "FastAPI con platzi"

Base.metadata.create_all(bind=engine)
app.add_middleware(ErrorHandler)
app.include_router(movie_router)
movies = [
    {
    "id": 1,
    "title": "Avatar",
    "overview": "Alta peli",
    "year": "2014",
    "rating": 10,
    "category": "accion"
    },
{
    "id": 2,
    "title": "Avatar2",
    "overview": "Alta peli",
    "year": "2014",
    "rating": 10,
    "category": "accion"
 }
]






# ejecutamos la variable con un metodo get
@app.get('/', tags=["Testing"])

def message():
    return HTMLResponse('<h1>Hello World</h1>')

