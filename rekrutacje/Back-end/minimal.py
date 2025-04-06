from fastapi import FastAPI
import uvicorn

print("Tworzenie aplikacji FastAPI...")
app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    print("Uruchamianie serwera na http://127.0.0.1:8001/")
    uvicorn.run(app, host="127.0.0.1", port=8001) 