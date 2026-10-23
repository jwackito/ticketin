from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1.router import api_router
from app.db.session import get_db

app = FastAPI(title="ticketin API", version="0.1.0")
app.include_router(api_router, prefix="/api/v1")

DbSession = Annotated[Session, Depends(get_db)]


@app.get("/health")
def health(db: DbSession) -> JSONResponse:
    """Report liveness plus database reachability."""
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        return JSONResponse(
            status_code=503,
            content={"status": "degraded", "database": "unreachable"},
        )
    return JSONResponse(status_code=200, content={"status": "ok", "database": "ok"})
