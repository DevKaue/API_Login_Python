from fastapi import FastAPI
from routes import router

app = FastAPI(title="Minha API Python com JWT e SQL Server")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
