import uvicorn
from fastapi import FastAPI
from src.apis import text_api


app = FastAPI()

app.include_router(text_api.router)

if __name__ == "__main__":
    uvicorn.run("main:src", host="0.0.0.0", reload=True,  port=5000)
