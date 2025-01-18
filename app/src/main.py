from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from app.src.database import create_all_tables
from app.src.routes.auth.auth import auth_routes
from app.src.routes.user.user import user_routes
from app.src.routes.user.scan import scan_routes
from app.src.routes.user.statistic import statistic_routes

from app.src.config import APP_TITLE, APP_DESCRIPTION, APP_VERSION


app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_all_tables()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    print(f"Solicitud entrante: {request.method} {request.url}")
    print("Cabeceras:", request.headers)
    print("Cookies:", request.cookies)
    
    response = await call_next(request)
    return response


app.include_router(auth_routes)
app.include_router(user_routes) 
app.include_router(scan_routes)
app.include_router(statistic_routes)
