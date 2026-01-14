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
def create_items(p: Persona):
    df = pd.read_csv(CSV_FILE)

    if p.id in df['id'].values:
        raise HTTPException(status_code=400, detail="ID duplicato")
    
    df.loc[len(df)] = [p.id, p.nome, p.cognome, p.codice_fiscale]
    df.to_csv(CSV_FILE, index=False)

    return p

@app.get("/items/{id}")
def get_item(id: int):
    df = pd.read_csv(CSV_FILE)
    p = df[df['id'] == id]
    if p.empty:
        raise HTTPException(status_code=404, detail="Persona non trovata")
    return p.to_dict(orient="records")[0]

