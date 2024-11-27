# main.py
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class InputData(BaseModel):
    key: str
    value: str

@app.get("/")
async def read_root():
    return {"message": "Hello, API is working!"}

@app.post("/replace")
async def replace_text(data: InputData):
    return {"replaced": data.value.replace("{key}", data.key)}

