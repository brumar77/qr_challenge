from fastapi import APIRouter


def create_public_router(**kwargs):
    return APIRouter(dependencies=[], **kwargs) #rutas publicas