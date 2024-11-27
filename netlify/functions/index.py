from fastapi import FastAPI
from pydantic import BaseModel
from mangum import Mangum  # Netlify Functions対応用

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

# Netlify Functions対応用ハンドラ
handler = Mangum(app)

# ローカル実行用
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

