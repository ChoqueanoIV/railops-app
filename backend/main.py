from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.auth_router import router as auth_router
from app.routers.passagem_router import router as passagem_router

app = FastAPI(title="RailOps API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(passagem_router)


@app.get("/health", tags=["Infraestrutura"])
def health_check():
    return {"status": "ok"}
