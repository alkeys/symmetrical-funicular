from fastapi import FastAPI, Depends
from router.gasolineras import router as gasolineras_router
from router.rol import router as rol_router
from router.log import router as log_router
from router.usuarios import router as usuarios_router
from router.vehiculos import router as vehiculos_router
from router.bitacora import router as bitacora_router
from router.proyecto import router as proyecto_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia "*" por el dominio específico si no quieres permitir todos
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)


app.include_router(gasolineras_router, prefix="/gasolineras", tags=["gasolineras"])
app.include_router(rol_router, prefix="/rol", tags=["rol"])
app.include_router(log_router, prefix="/log", tags=["log"])
app.include_router(usuarios_router, prefix="/usuarios", tags=["usuarios"])
app.include_router(vehiculos_router, prefix="/vehiculos", tags=["vehiculos"])
app.include_router(bitacora_router, prefix="/bitacora", tags=["bitacora"])
app.include_router(proyecto_router, prefix="/proyecto", tags=["proyecto"])

@app.get("/")
def read_root():
    return {"API": "Proyecto Final API Mariadb"}

