from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "To działa!"}

@app.get("/items")
def read_items():
    return [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]

# Aby uruchomić ten plik bezpośrednio:
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app3:app", host="127.0.0.1", port=8001, reload=True) 