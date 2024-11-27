from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum  # Netlify対応用

app = FastAPI()

class InputData(BaseModel):
    key: str
    value: str

@app.get("/")
async def read_root():
    return {"message": "Hello from Netlify!"}

@app.post("/replace")
async def replace_text(data: InputData):
    return {"replaced": data.value.replace("{key}", data.key)}

handler = Mangum(app)

