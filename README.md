# API Académica

API educativa para administrar cursos y estudiantes con **FastAPI, SQLModel y SQLite**. El código incluye comentarios en español para estudiar cómo se conectan las rutas HTTP, la validación de datos y la persistencia.

La explicación detallada del proyecto, la práctica con Swagger y los ejercicios están en la [guía para estudiantes](docs.md).

## Funcionalidades

- **Cursos:** CRUD completo. Crear, consultar (lista o por ID), actualizar con `PUT` (actualización completa) y eliminar con `DELETE`.
- **Estudiantes:** crear, listar y consultar por ID, con nombre, correo, semestre y estado activo.
- Validar los datos de entrada y responder con errores HTTP (`404` para recursos inexistentes y `422` para datos inválidos).
- Conservar los registros en una base de datos SQLite local (`database.db`), con una tabla por recurso (`course` y `student`).
- Informe de pruebas con evidencias en la carpeta [entrega-pruebas](entrega-pruebas/informe-pruebas.md).

Quedan fuera del alcance la relación entre estudiantes y cursos, la matrícula, la actualización y eliminación de estudiantes, la autenticación y la paginación.

## Tecnologías

| Herramienta | Uso |
| --- | --- |
| FastAPI | Aplicación web, rutas y documentación interactiva. |
| Uvicorn | Servidor que ejecuta la API. |
| SQLModel | Modelos de tablas y operaciones de base de datos. |
| Pydantic | Esquemas y validación de datos. |
| SQLite | Almacenamiento en el archivo `database.db`. |

Las versiones utilizadas están en [requirements.txt](requirements.txt). El proyecto se ha ejecutado con **Python 3.12**.

## Inicio rápido

Abre una terminal en la carpeta del proyecto, donde está `main.py`.

### 1. Crear y activar el entorno virtual

En Linux o macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

En Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si el entorno `venv` ya existe, basta con activarlo.

### 2. Instalar las dependencias

```bash
python -m pip install -r requirements.txt
```

### 3. Ejecutar la API

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

`main:app` identifica el objeto `app` del archivo `main.py`. La opción `--reload` recarga el servidor cuando editas el código durante el desarrollo. Para detenerlo, presiona `Ctrl+C`.

Abre la [documentación interactiva Swagger](http://127.0.0.1:8000/docs) para probar los endpoints con **Try it out → Execute**.

La base de datos y sus tablas se crean al iniciar la aplicación. Ejecuta el comando desde la raíz del proyecto para usar siempre el mismo archivo `database.db`.

## Endpoints

### Courses

| Método | Ruta | Operación | Estado de éxito |
| --- | --- | --- | --- |
| `POST` | `/courses` | Crear un curso. | `201` |
| `GET` | `/courses` | Listar todos los cursos. | `200` |
| `GET` | `/courses/{course_id}` | Consultar un curso por ID. | `200` |
| `PUT` | `/courses/{course_id}` | Actualizar un curso (los tres campos son obligatorios). | `200` |
| `DELETE` | `/courses/{course_id}` | Eliminar un curso; responde `{"message": "Course deleted"}`. | `200` |

### Students

| Método | Ruta | Operación | Estado de éxito |
| --- | --- | --- | --- |
| `POST` | `/students` | Crear un estudiante. | `201` |
| `GET` | `/students` | Listar todos los estudiantes (`[]` si no hay). | `200` |
| `GET` | `/students/{student_id}` | Consultar un estudiante por ID. | `200` |

Un curso o estudiante inexistente devuelve `404` (`Course not found` / `Student not found`). Los datos que incumplen el esquema y los IDs que no son enteros devuelven `422`. La ruta `/` no está definida; utiliza `/docs`.

## Ejemplo de uso

Para crear un curso, envía este cuerpo JSON a `POST /courses` desde Swagger:

```json
{
  "name": "Programación I",
  "credits": 3,
  "active": true
}
```

También puedes hacerlo desde otra terminal con `curl` en Bash:

```bash
curl -i -X POST http://127.0.0.1:8000/courses \
  -H 'Content-Type: application/json' \
  -d '{"name": "Programación I", "credits": 3, "active": true}'
```

La API responde con `201 Created` y el curso guardado:

```json
{
  "id": 1,
  "name": "Programación I",
  "credits": 3,
  "active": true
}
```

El ID es ilustrativo: SQLite lo asigna automáticamente. Usa el valor recibido para consultar el curso en `/courses/{course_id}`. Cada creación válida guarda un nuevo registro.

### Reglas de entrada

| Campo | Regla |
| --- | --- |
| `name` | Obligatorio; entre 3 y 80 caracteres. |
| `credits` | Obligatorio; entero entre 1 y 6. |
| `active` | Opcional; booleano con valor predeterminado `true`. |

`PUT /courses/{course_id}` usa el esquema `CourseUpdate`: `name`, `credits` y `active` son **obligatorios** (con las mismas reglas de nombre y créditos). El `id` no se puede modificar.

### Reglas de entrada de estudiantes

| Campo | Regla |
| --- | --- |
| `name` | Obligatorio; entre 3 y 80 caracteres. |
| `email` | Obligatorio; no puede estar vacío (no se valida el formato). |
| `semester` | Obligatorio; entero entre 1 y 10. |
| `active` | Opcional; booleano con valor predeterminado `true`. |

## Estructura del proyecto

```text
api_acad-mica/
├── main.py                       # Aplicación, ciclo de vida y registro de routers
├── database/database.py          # Motor SQLite y sesiones
├── models/
│   ├── course.py                 # Modelo de la tabla course
│   └── student.py                # Modelo de la tabla student
├── schemas/
│   ├── course.py                 # CourseCreate, CourseUpdate y CourseResponse
│   └── student.py                # StudentCreate y StudentResponse
├── routers/
│   ├── courses.py                # Endpoints HTTP de cursos
│   └── students.py               # Endpoints HTTP de estudiantes
├── services/
│   ├── course_service.py         # Crear, listar, consultar, actualizar y eliminar cursos
│   └── student_service.py        # Crear, listar y consultar estudiantes
├── entrega-pruebas/
│   ├── informe-pruebas.md        # Informe con todas las pruebas realizadas
│   └── evidencias/               # Salida real de cada ejecución
├── requirements.txt              # Dependencias
├── docs.md                       # Guía didáctica detallada
├── ejercicio.md                  # Retos de la actividad
└── README.md                     # Presentación e inicio rápido
```

El flujo principal es: **petición HTTP → router y validación (schema) → servicio → modelo y sesión → SQLite → respuesta JSON**. La lógica de datos vive en los servicios; los routers solo reciben la petición y delegan.

Los cursos y los estudiantes comparten el mismo motor y el mismo archivo `database.db`, que contiene las tablas `course` y `student`. El archivo no se sube al repositorio (está en `.gitignore`).

Para seguir el código paso a paso, comprender `Depends`, `Session`, `commit()` y `refresh()`, o resolver problemas de ejecución, consulta [docs.md](docs.md).
# 
# TALLER: FASTAPI, SQLMODEL Y ARQUITECTURA EN CAPAS
# 

# 1. ¿Cuál es la función de un router?
# El router es el que recibe la petición HTTP. Ahí declaro cada endpoint 
# con su método y su ruta (por ejemplo @router.put("/{course_id}")), y con 
# APIRouter le pongo un prefijo (/courses o /students) y una etiqueta para que 
# en Swagger salgan agrupados. Lo importante es que el router no tiene la lógica 
# de datos: solo recibe lo que llega, deja que FastAPI lo valide con el schema, 
# llama a la función del service y devuelve la respuesta. Y para que funcione 
# hay que registrarlo en main.py con include_router; si no, la ruta no aparece 
# en Swagger.


# 2. ¿Cuál es la diferencia entre un schema y un model?
# El schema (por ejemplo CourseCreate o StudentResponse) es una clase de 
# Pydantic y sirve para validar el JSON que llega y para definir cómo se ve la 
# respuesta; no toca la base de datos. El model (Course o Student) es una clase 
# de SQLModel con table=True, o sea que representa una tabla real con sus columnas. 
# Se nota la diferencia en el id: CourseCreate no lo tiene porque el cliente no 
# lo manda, pero el model Course sí, como clave primaria, porque lo genera 
# SQLite al guardar. Y CourseResponse sí lo incluye porque es lo que le devuelvo 
# al cliente.


# 3. ¿Por qué la lógica de DELETE debe estar en el service?
# Porque cada capa tiene su trabajo. El router se encarga de la parte 
# web y el service de la lógica: buscar el curso, lanzar el 404 si no existe, 
# borrarlo y confirmar el cambio. Si metiera eso en el router, quedaría todo 
# mezclado y el día que cambie cómo se guardan los datos tendría que tocar los 
# endpoints. Además así el código se puede reutilizar: en mi delete_course 
# reutilicé get_course, que ya sabe lanzar el "Course not found", y no tuve que 
# repetir esa validación.

def delete_course(course_id: int, session: Session):
    course = get_course(course_id, session)   # Si no existe, lanza el 404
    session.delete(course)                    # Marca el registro para borrarlo
    session.commit()                          # Confirma el borrado en la base
    return {"message": "Course deleted"}


# 4. ¿Qué función cumple Session?
# La Session es el objeto con el que el service habla con la base de 
# datos. Con ella hago session.add() para agregar, session.get() para buscar 
# por clave primaria, session.exec(select(...)) para consultar, session.delete() 
# para borrar y session.commit() para confirmar. Los cambios quedan pendientes 
# en la sesión hasta que hago commit. Se abre una por petición y se cierra sola 
# cuando termina.


# 5. ¿Para qué sirve session.commit()?
# Cuando hago add, delete o modifico un objeto, el cambio solo está en 
# la sesión, todavía no en la base. El commit es el que lo confirma y lo escribe 
# de verdad en el archivo database.db. Si me olvido del commit, la API puede 
# responder bien pero el dato no persiste: por ejemplo, un DELETE que dice 
# "Course deleted" pero el curso sigue apareciendo después. Por eso en mi código 
# el mensaje de éxito se devuelve después del commit.


# 6. ¿Por qué utilizamos session.refresh() después de crear un registro?
# Cuando creo el objeto Course o Student, el id todavía es None porque 
# lo asigna SQLite al insertarlo. Después del commit hago refresh() para que el 
# objeto se vuelva a cargar con lo que quedó guardado, y así ya trae el id 
# generado. Si no lo hiciera, la respuesta del POST no traería el id correcto. 
# También lo uso en el PUT para devolver el curso tal cual quedó actualizado.


# 7. ¿Qué hace Depends(get_session)?
# Depends es la inyección de dependencias de FastAPI. Cuando el endpoint 
# tiene el parámetro session: Session = Depends(get_session), FastAPI ejecuta 
# get_session, que abre la sesión con el engine, se la pasa al endpoint y cuando 
# la petición termina la cierra automáticamente, porque la función usa con (with) 
# y yield. Con eso no tengo que crear ni cerrar la sesión a mano en cada endpoint, 
# y los cursos y los estudiantes usan exactamente la misma función.

def get_session():
    with Session(engine) as session:
        yield session


# 8. ¿Qué significa table=True?
# Con class Course(SQLModel, table=True) le digo a SQLModel que esa clase 
# representa una tabla: los campos tipados (name, credits, active) se vuelven 
# columnas y el id con primary_key=True es la clave primaria. Gracias a eso, 
# create_all() crea la tabla al iniciar la app. Sin table=True sería un modelo 
# normal de validación, sin tabla detrás.


# 9. ¿Por qué los datos continúan existiendo después de reiniciar Uvicorn?
# A diferencia del taller anterior, donde los equipos vivían en una lista 
# de Python que se perdía al apagar el servidor, aquí los datos se guardan en el 
# archivo database.db con SQLite. El commit los escribe ahí, y cuando reinicio 
# Uvicorn, create_all() solo crea las tablas que no existen, no borra las que ya 
# están. Un detalle: hay que arrancar el servidor desde la misma carpeta, porque 
# la ruta de la base es relativa (sqlite:///database.db); si lo corro desde otra 
# carpeta, crearía otro archivo vacío. Eso lo comprobé en las pruebas P09.


# 10. ¿Por qué CourseCreate y CourseUpdate son schemas diferentes?
# En CourseCreate el campo active es opcional y vale true por defecto, 
# porque al crear un curso nuevo tiene sentido que quede activo. En CourseUpdate, 
# como la actualización es completa, name, credits y active son obligatorios y 
# active no tiene valor predeterminado. Así, si alguien omite active en un PUT, 
# FastAPI responde 422 en vez de poner true en silencio y pisar el valor que 
# tenía el curso. Si dejara enviar solo uno de los campos, ya sería una 
# actualización parcial (PATCH): los campos sean opcionales y el service tendría 
# que cambiar únicamente los que lleguen.


# 11. ¿Por qué actualizar un curso no debe generar un nuevo ID?
# En update_course busco el curso existente con get_course y le asigno 
# los valores nuevos a ese mismo objeto (course.name = ..., course.credits = ..., 
# course.active = ...). Como SQLModel sabe que ese objeto ya viene de la base, 
# el commit hace un UPDATE sobre esa fila y el id se conserva. Si en cambio 
# construyera un Course nuevo y lo agregara con add, sería un INSERT y aparecería 
# un curso duplicado con otro id. Además CourseUpdate no incluye el id, así que 
# el cliente ni siquiera puede cambiarlo. En las pruebas P04c y P04d verifiqué 
# que el id seguía igual y que la cantidad de cursos no aumentaba.

course = get_course(course_id, session)   # El curso que ya existe
course.name = course_data.name            # Modifico ese mismo objeto
course.credits = course_data.credits
course.active = course_data.active        # False también se guarda
session.add(course)
session.commit()
session.refresh(course)


# 12. ¿Cómo agregaste la tabla Student a la aplicación?
# Primero creé models/student.py con table=True, después schemas/student.py 
# (StudentCreate y StudentResponse), services/student_service.py y 
# routers/students.py, sin mezclarlo con Course. Luego en main.py importé el 
# router de
