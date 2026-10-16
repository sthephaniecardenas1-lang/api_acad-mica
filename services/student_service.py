# Los servicios realizan las operaciones de datos que solicitan los routers.
from fastapi import HTTPException
from sqlmodel import Session, select

from models.student import Student
from schemas.student import StudentCreate


def create_student(
    student_data: StudentCreate,
    session: Session
):

    # convierto los datos validados en una entidad Student para poder guardarla
    student = Student(
        name=student_data.name,
        email=student_data.email,
        semester=student_data.semester,
        active=student_data.active
    )

    session.add(student)
    # confirma el INSERT en la base de datos
    session.commit()
    # recarga el registro para tener el id que asignó SQLite
    session.refresh(student)

    return student


def list_students(session: Session):

    # consulta que trae todos los registros de Student
    statement = select(Student)

    students = session.exec(statement).all()

    return students


def get_student(
    student_id: int,
    session: Session
):

    # busca por clave primaria; devuelve None si no existe
    student = session.get(
        Student,
        student_id
    )

    # si no existe respondo 404 con el mensaje que pide el enunciado
    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student
