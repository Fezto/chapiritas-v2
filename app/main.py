# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import lifespan
from app.routers.product import router as products_router


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
    products_router
]

# Incluir todos los routers
for router in routers:
    app.include_router(router)

# Mostrar rutas en consola
for route in app.routes:
    print(f"{route.path} -> {route.name}")
