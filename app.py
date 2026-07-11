from fastapi import FastAPI

from routes import router

app = FastAPI(
    title="IRIS Server v1.0",
    version="1.0"
)


@app.get("/")
def root():

    return {
        "status": "online",
        "name": "IRIS Server v1.0",
        "message": "IRIS Cloud Brain is running."
    }


app.include_router(router)
