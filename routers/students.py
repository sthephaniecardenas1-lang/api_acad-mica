from fastapi import APIRouter, Depends
from sqlmodel import Session

from database.database import get_session
from schemas.student import StudentCreate, StudentResponse

from services.student_service import (
    create_student,
    list_students,
    get_student
)


# Agrupa las rutas bajo /students y la etiqueta Students en Swagger.
router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# POST /students: recibe datos validados y responde con el estudiante creado (201).
@router.post(
    "",
    response_model=StudentResponse,
    status_code=201
)
def create_student_endpoint(
    # FastAPI interpreta StudentCreate como el cuerpo JSON de la petición.
    student: StudentCreate,
    # reutilizo la misma sesión/conexión que usan los cursos
    session: Session = Depends(get_session)
):

    return create_student(
        student,
        session
    )


# GET /students: devuelve todos los estudiantes (lista vacía si no hay ninguno).
@router.get(
    "",
    response_model=list[StudentResponse]
)
def list_students_endpoint(
    session: Session = Depends(get_session)
):

    return list_students(session)


# GET /students/{student_id}: el id de la URL se valida como entero (si no, 422).
@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student_endpoint(
    student_id: int,
    session: Session = Depends(get_session)
):

    return get_student(
        student_id,
        session
    )
