from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import os

app = FastAPI()
CSV_FILE = "./data.csv"

class Persona(BaseModel):
    id: int
    nome: str
    cognome: str
    codice_fiscale: str

if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["id", "nome", "cognome", "codice_fiscale"])
    df.to_csv(CSV_FILE, index=False)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/")
def get_items():
    df = pd.read_csv(CSV_FILE)
    return df.to_dict(orient="records")

@app.post("/items/")
def create_item(p: Persona):
    df = pd.read_csv(CSV_FILE)

    if p.id in df['id'].values:
        raise HTTPException(status_code=400, detail="ID duplicato")
    
    df.loc[len(df)] = [p.id, p.nome, p.cognome, p.codice_fiscale]
    df.to_csv(CSV_FILE, index=False)

    return p

@app.get("/items/count")
def get_count():
    df = pd.read_csv(CSV_FILE)
    return {"count": len(df)}

@app.get("/items/{id}")
def get_item(id: int):
    df = pd.read_csv(CSV_FILE)

    if id not in df['id'].values:
        raise HTTPException(status_code=400, detail="Persona non trovata")

    p = df[df['id'] == id]

    return p.to_dict(orient="records")[0]

@app.delete("/items/{id}")
def delete_item(id: int):
    df = pd.read_csv(CSV_FILE)
    
    if id not in df['id'].values:
        raise HTTPException(status_code=400, detail="Persona non trovata")
    
    df = df[df['id'] != id]
    df.to_csv(CSV_FILE, index=False)
    
    return {"message": "Persona cancellata con successo"}

@app.put("/items/{id}")
def update_item(id: int, p: Persona):
    df = pd.read_csv(CSV_FILE)
    
    if id not in df['id'].values:
       raise HTTPException(status_code=400, detail="Persona non trovata")
    
    colonne = ["nome", "cognome", "codice_fiscale"]
    dati_aggiornati = [p.nome, p.cognome, p.codice_fiscale]
    df.loc[df['id'] == id, colonne] = dati_aggiornati
    
    df.to_csv(CSV_FILE, index=False)
    return p