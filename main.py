from fastapi import FastAPI
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
    return df.to_dict(orient="")