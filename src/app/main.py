from fastapi import FastAPI
from config.settings import settings
from app.services import router as text_router


app = FastAPI(title=settings.PROJECT_NAME)
app.include_router(text_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)