from fastapi import FastAPI

app = FastAPI(title="Sistema de Gestión de Eventos API")

@app.get("/")
def read_root():
    return {"message": "Bienvenido al Sistema de Gestión de Eventos Backend"}
