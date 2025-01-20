import os
from fastapi import Depends, FastAPI, Request
from alembic.config import Config
from alembic import command
from starlette.middleware.cors import CORSMiddleware

from app.src.database import create_all_tables
from app.src.routes.auth.auth import auth_routes
from app.src.routes.user.user import user_routes
from app.src.routes.user.scan import scan_routes
from app.src.routes.user.statistic import statistic_routes

from app.src.config import APP_TITLE, APP_DESCRIPTION, APP_VERSION
from app.src.middleware.security import get_current_user
from app.src.exceptions.error_handlers import add_error_handlers


app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    dependencies=[Depends(get_current_user)] #default rutas privadas
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if os.getenv("ENVIRONMENT") != "test":
    create_all_tables() 
    

alembic_cfg = Config("alembic.ini")
command.upgrade(alembic_cfg, "head")
    
@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Solicitud entrante: {request.method} {request.url}")
    print("Cabeceras:", request.headers)
    print("Cookies:", request.cookies)
    
    response = await call_next(request)
    return response

add_error_handlers(app)

app.include_router(auth_routes)
app.include_router(user_routes) 
app.include_router(scan_routes)
app.include_router(statistic_routes)
