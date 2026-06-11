from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import matches, teams, predictions, bracket

app = FastAPI(
    title="World Cup 2026 Betting Analysis API",
    description="API for World Cup 2026 betting analysis and predictions",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matches.router, prefix="/api")
app.include_router(teams.router, prefix="/api")
app.include_router(predictions.router, prefix="/api")
app.include_router(bracket.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "World Cup 2026 Betting Analysis API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "ok"}
