from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "To działa!"}

@app.get("/items")
def read_items():
    return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}] 