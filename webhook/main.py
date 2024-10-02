from fastapi import FastAPI
from src import person, account

app = FastAPI()

app.include_router(person.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=9980, reload=True)