from fastapi import FastAPI

app = FastAPI(title="MultiStore Gateway")


@app.get("/health")
def health():
    return {"status": "healthy"}

