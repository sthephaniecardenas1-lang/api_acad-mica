from sqlmodel import SQLModel, Field


# table=True hace que Student sea su propia tabla dentro de la misma database.db
class Student(SQLModel, table=True):

    # clave primaria generada por SQLite, no se pide al crear el estudiante
    id: int | None = Field(
        default=None,
        primary_key=True
    )

    name: str

    # por ahora el correo se guarda como texto simple
    email: str

    semester: int

    # un estudiante nuevo queda activo si no se indica otro valor
    active: bool = True
