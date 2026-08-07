from fastapi import FastAPI

app = FastAPI(
    title="AutoSecure Pipeline",
    description="Event-driven secure data processing and automation platform",
    version="1.0.0",
)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AutoSecure Pipeline",
    }