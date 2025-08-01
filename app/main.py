# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import lifespan
from app.routers.product import router as products_router
from app.routers.auth import router as auth_router
from app.routers.brands import router as brands_router
from app.routers.categories import router as categories_router
from app.routers.size import router as sizes_router
from app.routers.color import router as colors_router
from app.routers.gender import router as gender_router
from app.routers.material import router as material_router
from app.routers.test_email import router as test_email_router

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lista de routers
routers = [
    products_router, auth_router, brands_router, categories_router, 
    sizes_router, colors_router, gender_router, material_router, test_email_router
]

# Incluir todos los routers
for router in routers:
    app.include_router(router)

# Mostrar rutas en consola
for route in app.routes:
    print(f"{route.path} -> {route.name}")
