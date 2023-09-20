#importaciones necesarias
from fastapi import FastAPI ,  HTTPException 
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List

#instanciamos nuestra API
app = FastAPI(title="Notes", version="0.0.1")

#creamos nuestra clase modelo
class Note(BaseModel):
    #definimos nuestros atributos
    id_note : int 
    title: str 
    content: str
    content_at: str

    #configuracion de nuestra clase por defecto
    class Config:
        schema_extra = {
            "example": {
                "id_note":0,
                "title": "aventura", 
                "content": "Un dia tuve una gran aventura",
                "content_at": "fecha"

            }
        }
        
notes = [
    {
        "id_note":0,
        "title": "mi viaje al parque", 
        "content": "Un dia tuve una gran aventura en un parque ",
        "content_at": "25 de enero"
    }
]

currend_id = 1 # inicializamos con el anterior id_note


#retornaremos un html response para que se vea mas cool

@app.get('/', response_class=HTMLResponse, tags=["home"])
def message():
    return """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API REST</title>
    <h1>Darkcode CRUD API REST<h1/>

</head>

"""
#metodo post
@app.post('/notes', tags=['notes'], response_model=dict, status_code=201)
def create_note(note: Note):
    global currend_id
    note.id_note = currend_id
    currend_id += 1
    notes.append(note.dict())
    return {"message": "Se ha registrado la nota"}


#metodo get para mirar nuestras notas
@app.get('/notes', tags=['notes'],response_model=List[Note], status_code=200)
def get_notes():
    return notes


#metodo get para filtrar nuestras notas por el id
#habia un pequeno error, debemos pasar el parametro id_note para filtrar
@app.get('/notes/{id_note}', tags=['notes'],response_model=Note, status_code=200)
def get_note(id_note:int ):
    for item in notes:
        if item["id_note"] == id_note:
            return item
    #de lo contrario
    raise HTTPException(status_code=404 , detail="Nota no encontrada")

@app.put('/notes/{id_note}', tags=['notes'], response_model=dict, status_code=200)
def update_note(id_note:int , note:Note):
    for item in notes:
        if item["id_note"]== id_note:
            item.update(note.dict())
            return {"message":"se ha modificado la nota"}
    raise HTTPException(status_code=404, detail="nota no encontrada")

#por ultimo el delete

@app.delete('/notes/{id_note}', tags=['notes'], response_model=dict, status_code=200)
def delete_note(id_note:int):
    for item in notes:
        if item["id_note"]==id_note:
            notes.remove(item)
            return {"message":"Nota eliminada con exito"}
    raise HTTPException(status_code=404, detail="Nota no encontrada")

#ejecutamos en nuestro archivo principal

if __name__=="__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

    #okeeey ahora probemos
    #end
    #ahora subiremos la app a github
    