from fastapi import APIRouter
from fastapi import  Body, Path, Query
from fastapi.responses import  JSONResponse
from pydantic import BaseModel, Field
from typing import Optional
from fastapi.security import HTTPBearer
from config.database import Session, engine, Base
from models.movie import Movie as MovieModel
from fastapi.encoders import jsonable_encoder
from middlewares.error_handler import ErrorHandler
from services.movie import MovieService
from schemas.movie import Movie

movie_router = APIRouter()






@movie_router.get('/movies/{id}', tags=['movies'])
def get_movie(id: int = Path(ge=1, le=2000)):
    for item in movies:
        if item["id"] == id:
            return item
        
    return []

@movie_router.get('/movies/', tags=['movies'])
def get_movies_by_category(category: str = Query(min_length=5, max_length=15)):
    return [movie for movie in movies if movie['category'] == category]


@movie_router.post('/movies', tags=['movies'])
def create_movie(id: int = Body(), tittle: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    
    movies.append(
        {
        "id": id,
        "title": tittle,
        "overview": overview,
        "year": year,
        "rating": rating,
        "category": category
        }
    )
    return movies


@movie_router.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
    
    for item in movies:
        if item["id"] == id:
            item['title'] = title,
            item['overview'] = overview,
            item['year'] = year,
            item['rating'] = rating,
            item['category'] = category

            return movies

@movie_router.delete('/movies/{id}', tags=['movies'])
def delete_movie(id: int):
       # Recorro la lista de peliculas
       for item in movies:
        # Verifico si el id ingreso coincide con algun id de pelicula
        if item["id"] == id:
            # si coincide, elimino ese esa pelicula.
            movies.remove(item)
            # retorno la lista de peliculas, que me mostrara todas menos la borrada.
            return movies
        

@movie_router.put('/movies/{id}', tags=['movies'])
def update_movie(id: int, movie: Movie):
    # Recorro la lista de películas, si encuentro el {id} realizó la modificación.
    for item in movies:
        if item["id"] == id:
            item['title'] = movie.title
            item['overview'] = movie.overview
            item['year'] = movie.year
            item['rating'] = movie.rating
            item['category'] = movie.category
            
            return movies

@movie_router.post('/new_movies', tags=['movies'], response_model=dict, status_code=201)
def create_movie_new(movie: Movie) -> dict:
    db = Session()
    MovieService(db).create_movie(movie)
    #movies.append(movie)
    return JSONResponse(status_code=201, content={"message": " Se ha registrado la pelicula"})
    

@movie_router.get('/new_movies', tags=['movies'], response_model=list[Movie], status_code= 200)
def get_movies_new() -> list[Movie]:
    # Establesco la sesion sql
    db = Session()
    result = MovieService(db).get_movies()
    #Obtengo todos los datos y los guardo en una variable
    #result = db.query(MovieModel).all()
    #Obtengo los datos en formato json
    return JSONResponse(status_code=200, content=jsonable_encoder(result))
    

@movie_router.get('/new_movies/{id}', tags=['movies'], response_model=Movie)
def get_movie(id: int = Path(ge=1, le=2000)) -> Movie:
    db = Session()
    #result = db.query(MovieModel).filter(MovieModel.id == id).first()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "No encontrado"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))

@movie_router.get('/new_movies/', tags=['movies'], response_model=list[Movie])
def get_movie_new_category(category: str = Query(min_length=5, max_length=15)) -> list[Movie]:
    db = Session()
    #result = db.query(MovieModel).filter(MovieModel.category == category).first()
    result = MovieService(db).get_movie_for_category(category)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Categoria no encontrada"})
    return JSONResponse(status_code=200, content=jsonable_encoder(result))



@movie_router.put('/new_movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def update_movie_new(id: int, movie: Movie) -> dict:
    db = Session()
    #result = db.query(MovieModel).filter(MovieModel.id == id).first()
    result = MovieService(db).get_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Pelicula no encontrada"})
    MovieService(db).update_movie(id, movie)
    return JSONResponse(status_code=200, content={"message": "Se ha modificado correctamente"})

@movie_router.delete('/new_movies/{id}', tags=['movies'], response_model=dict, status_code=200)
def delete_movie_new(id: int) -> dict:
    db = Session()
    #result = db.query(MovieModel).filter(MovieModel.id == id).first()
    result = MovieService(db).delete_movie(id)
    if not result:
        return JSONResponse(status_code=404, content={"message": "Pelicula no encontrada"})
    db.delete(result)
    db.commit()
    return JSONResponse(status_code=200, content={"message": "Se ha eliminado correctamente"})
