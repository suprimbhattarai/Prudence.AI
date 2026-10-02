from fastapi import FastAPI

app = FastAPI(
    title="Prudence AI",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {
        "message": "Prudence AI backend is running",
    }
