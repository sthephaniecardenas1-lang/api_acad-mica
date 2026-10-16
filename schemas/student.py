from pydantic import BaseModel, ConfigDict, Field


# Esquema de entrada: valida el cuerpo JSON del POST /students.
class StudentCreate(BaseModel):
    # quita espacios al inicio y al final, así un email con solo espacios cuenta como vacío
    model_config = ConfigDict(str_strip_whitespace=True)

    # el nombre debe tener entre 3 y 80 caracteres
    name: str = Field(min_length=3, max_length=80)
    # obligatorio y no vacío (la validación del formato queda como ampliación)
    email: str = Field(min_length=1)
    # semestre entre 1 y 10
    semester: int = Field(ge=1, le=10)
    # si no lo envían queda en true
    active: bool = True


# Esquema de salida: lo que devuelve la API, incluido el id generado.
class StudentResponse(BaseModel):
    id: int
    name: str
    email: str
    semester: int
    active: bool
