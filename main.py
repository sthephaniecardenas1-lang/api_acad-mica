# Punto de entrada: conecta la aplicación FastAPI con las rutas y la base de datos.
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database.database import create_db_and_tables
from routers.courses import router as courses_router
from routers.students import router as students_router


# FastAPI ejecuta lo anterior a yield al iniciar y lo posterior al apagar.
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Los modelos Course y Student ya se registraron al importar sus routers y servicios,
    # por eso create_all crea las dos tablas dentro de la misma database.db.
    create_db_and_tables()
    yield


# lifespan prepara las tablas antes de aceptar peticiones.
app = FastAPI(title="API Académica", lifespan=lifespan)
# Incorpora los endpoints de cursos a la aplicación.
app.include_router(courses_router)
# Incorpora los endpoints de estudiantes; usa el mismo motor SQLite que los cursos.
app.include_router(students_router)
