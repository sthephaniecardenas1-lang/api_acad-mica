# Informe de pruebas — API Académica (Courses y Students)

| Dato | Información |
| --- | --- |
| Estudiante | Sthephanie Cárdenas |
| Fecha de ejecución | 15/10/2026 |
| Versión probada | Rama `main`, commit `b73c13c` (código final de los tres retos) |
| Comando de inicio | `python -m uvicorn main:app --reload` |
| URL base | `http://127.0.0.1:8000` |
| Herramienta | `curl -i` contra Uvicorn local. La petición y la respuesta completas (estado HTTP, cabeceras y cuerpo) quedaron guardadas como texto en la carpeta `evidencias/` |
| Estado inicial de la base | Vacía: `database.db` nueva, sin cursos ni estudiantes |
| Datos | Ficticios |
| Resultado global | **84 de 84 pruebas aprobadas**, 0 fallidas |

## Cómo leer este informe

- Cada fila es **una ejecución**; las variantes de un mismo grupo se identifican con letras (`P01a`, `P01b`, ...).
- Cada variante se ejecutó por separado, manteniendo válidos los demás datos.
- Una prueba donde se esperaba `404` o `422` y se obtuvo ese mismo código está **Aprobada**.
- La columna *Evidencia* indica el archivo de `evidencias/` y la sección (`===== P01a =====`) donde está la salida real de `curl -i`.
- Cuando el cuerpo incluye un texto de 80 u 81 caracteres, aquí se abrevia como `<80 caracteres>`; en la evidencia aparece completo.

## Resumen por grupo

| Grupo | Pruebas | Aprobadas | Fallidas |
| --- | --- | --- | --- |
| P01 — POST /courses | 16 | 16 | 0 |
| P02 — GET /courses | 2 | 2 | 0 |
| P03 — GET /courses/{course_id} | 3 | 3 | 0 |
| P04 — PUT /courses/{course_id} | 21 | 21 | 0 |
| P05 — DELETE /courses/{course_id} | 7 | 7 | 0 |
| P06 — POST /students | 19 | 19 | 0 |
| P07 — GET /students | 2 | 2 | 0 |
| P08 — GET /students/{student_id} | 3 | 3 | 0 |
| P09 — Persistencia e integración | 11 | 11 | 0 |

## Resultados detallados

### P01 — POST /courses

| Caso | Método y URL | Datos enviados | Resultado esperado | Resultado obtenido | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| P01a | `POST /courses` | `{"name": "Desarrollo Web II", "credits": 3, "active": true}` | 201 e ID generado | 201 — {"id":1,"name":"Desarrollo Web II","credits":3,"active":true} | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01a |
| P01b | `POST /courses` | `{"name": "Bases de Datos", "credits": 4}` | 201 y active = true por defecto | 201 — {"id":2,"name":"Bases de Datos","credits":4,"active":true} | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01b |
| P01c | `POST /courses` | `{"name": "Redes", "credits": 3, "active": false}` | 201 y active = false | 201 — {"id":3,"name":"Redes","credits":3,"active":false} | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01c |
| P01d | `POST /courses` | `{"name": "Mat", "credits": 2}` | 201 (nombre de 3 caracteres, límite válido) | 201 — {"id":4,"name":"Mat","credits":2,"active":true} | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01d |
| P01e | `POST /courses` | `{"name": "<80 caracteres>", "credits": 2}` | 201 (nombre de 80 caracteres, límite válido) | 201 — {"id":5,"name":"CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC","credits"... | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01e |
| P01f | `POST /courses` | `{"name": "Cálculo I", "credits": 1}` | 201 (créditos = 1, límite válido) | 201 — {"id":6,"name":"Cálculo I","credits":1,"active":true} | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01f |
| P01g | `POST /courses` | `{"name": "Cálculo II", "credits": 6}` | 201 (créditos = 6, límite válido) | 201 — {"id":7,"name":"Cálculo II","credits":6,"active":true} | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01g |
| P01h | `POST /courses` | `{"name": "Ab", "credits": 3}` | 422 (nombre de 2 caracteres) | 422 — {"detail":[{"type":"string_too_short","loc":["body","name"],"msg":"String should have at least 3 characters... | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01h |
| P01i | `POST /courses` | `{"name": "<81 caracteres>", "credits": 3}` | 422 (nombre de 81 caracteres) | 422 — {"detail":[{"type":"string_too_long","loc":["body","name"],"msg":"String should have at most 80 characters"... | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01i |
| P01j | `POST /courses` | `{"name": "Física", "credits": 0}` | 422 (créditos = 0) | 422 — {"detail":[{"type":"greater_than_equal","loc":["body","credits"],"msg":"Input should be greater than or equ... | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01j |
| P01k | `POST /courses` | `{"name": "Física", "credits": 7}` | 422 (créditos = 7) | 422 — {"detail":[{"type":"less_than_equal","loc":["body","credits"],"msg":"Input should be less than or equal to ... | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01k |
| P01l | `POST /courses` | `{"credits": 3}` | 422 (falta name) | 422 — {"detail":[{"type":"missing","loc":["body","name"],"msg":"Field required","input":{"credits":3}}]} | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01l |
| P01m | `POST /courses` | `{"name": "Física"}` | 422 (falta credits) | 422 — {"detail":[{"type":"missing","loc":["body","credits"],"msg":"Field required","input":{"name":"Física"}}]} | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01m |
| P01n | `POST /courses` | `{"name": "Física", "credits": "abc"}` | 422 (credits con texto) | 422 — {"detail":[{"type":"int_parsing","loc":["body","credits"],"msg":"Input should be a valid integer, unable to... | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01n |
| P01o | `POST /courses` | `{"name": "Física", "credits": 3, "active": "invalido"}` | 422 (active con texto) | 422 — {"detail":[{"type":"bool_parsing","loc":["body","active"],"msg":"Input should be a valid boolean, unable to... | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01o |
| P01p | `GET /courses` | — | 200 y siguen 7 cursos (las peticiones rechazadas no crearon registros) | 200 — [{"id":1,"name":"Desarrollo Web II","credits":3,"active":true},{"id":2,"name":"Bases de Datos","credits":4,... | Aprobado | [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) · P01p |

### P02 — GET /courses

| Caso | Método y URL | Datos enviados | Resultado esperado | Resultado obtenido | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| P02a | `GET /courses` | — | 200 y [] | 200 — [] | Aprobado | [P02-listar-cursos.txt](evidencias/P02-listar-cursos.txt) · P02a |
| P02b | `GET /courses` | — | 200 y lista con 7 cursos, activos e inactivos | 200 — [{"id":1,"name":"Desarrollo Web II","credits":3,"active":true},{"id":2,"name":"Bases de Datos","credits":4,... | Aprobado | [P02-listar-cursos.txt](evidencias/P02-listar-cursos.txt) · P02b |

### P03 — GET /courses/{course_id}

| Caso | Método y URL | Datos enviados | Resultado esperado | Resultado obtenido | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| P03a | `GET /courses/1` | — | 200 y el curso 1 | 200 — {"id":1,"name":"Desarrollo Web II","credits":3,"active":true} | Aprobado | [P03-consultar-curso.txt](evidencias/P03-consultar-curso.txt) · P03a |
| P03b | `GET /courses/9999` | — | 404 y {"detail": "Course not found"} | 404 — {"detail":"Course not found"} | Aprobado | [P03-consultar-curso.txt](evidencias/P03-consultar-curso.txt) · P03b |
| P03c | `GET /courses/abc` | — | 422 (el id debe ser entero) | 422 — {"detail":[{"type":"int_parsing","loc":["path","course_id"],"msg":"Input should be a valid integer, unable ... | Aprobado | [P03-consultar-curso.txt](evidencias/P03-consultar-curso.txt) · P03c |

### P04 — PUT /courses/{course_id}

| Caso | Método y URL | Datos enviados | Resultado esperado | Resultado obtenido | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| P04a | `GET /courses/1` | — | 200: estado ANTES del PUT (Desarrollo Web II, 3, true) | 200 — {"id":1,"name":"Desarrollo Web II","credits":3,"active":true} | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04a |
| P04b | `PUT /courses/1` | `{"name": "Programación II", "credits": 4, "active": false}` | 200, mismo ID y nuevos valores | 200 — {"id":1,"name":"Programación II","credits":4,"active":false} | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04b |
| P04c | `GET /courses/1` | — | 200: los cambios aparecen y el ID se conserva | 200 — {"id":1,"name":"Programación II","credits":4,"active":false} | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04c |
| P04d | `GET /courses` | — | 200 y la cantidad de cursos sigue siendo 7 | 200 — [{"id":1,"name":"Programación II","credits":4,"active":false},{"id":2,"name":"Bases de Datos","credits":4,"... | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04d |
| P04e | `PUT /courses/2` | `{"name": "Bases de Datos", "credits": 4, "active": false}` | 200 y active cambia de true a false | 200 — {"id":2,"name":"Bases de Datos","credits":4,"active":false} | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04e |
| P04f | `PUT /courses/3` | `{"name": "Web", "credits": 3, "active": true}` | 200 (nombre de 3 caracteres, límite válido) | 200 — {"id":3,"name":"Web","credits":3,"active":true} | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04f |
| P04g | `PUT /courses/3` | `{"name": "<80 caracteres>", "credits": 3, "active": true}` | 200 (nombre de 80 caracteres, límite válido) | 200 — {"id":3,"name":"CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC","credits"... | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04g |
| P04h | `PUT /courses/3` | `{"name": "Física I", "credits": 1, "active": true}` | 200 (créditos = 1, límite válido) | 200 — {"id":3,"name":"Física I","credits":1,"active":true} | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04h |
| P04i | `PUT /courses/3` | `{"name": "Física II", "credits": 6, "active": true}` | 200 (créditos = 6, límite válido) | 200 — {"id":3,"name":"Física II","credits":6,"active":true} | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04i |
| P04j | `PUT /courses/3` | `{"name": "Zz", "credits": 3, "active": true}` | 422 (nombre de 2 caracteres) | 422 — {"detail":[{"type":"string_too_short","loc":["body","name"],"msg":"String should have at least 3 characters... | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04j |
| P04k | `PUT /courses/3` | `{"name": "<81 caracteres>", "credits": 3, "active": true}` | 422 (nombre de 81 caracteres) | 422 — {"detail":[{"type":"string_too_long","loc":["body","name"],"msg":"String should have at most 80 characters"... | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04k |
| P04l | `PUT /courses/3` | `{"name": "Química", "credits": 0, "active": true}` | 422 (créditos = 0) | 422 — {"detail":[{"type":"greater_than_equal","loc":["body","credits"],"msg":"Input should be greater than or equ... | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04l |
| P04m | `PUT /courses/3` | `{"name": "Química", "credits": 7, "active": true}` | 422 (créditos = 7) | 422 — {"detail":[{"type":"less_than_equal","loc":["body","credits"],"msg":"Input should be less than or equal to ... | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04m |
| P04n | `PUT /courses/3` | `{"credits": 3, "active": true}` | 422 (falta name) | 422 — {"detail":[{"type":"missing","loc":["body","name"],"msg":"Field required","input":{"credits":3,"active":tru... | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04n |
| P04o | `PUT /courses/3` | `{"name": "Química", "active": true}` | 422 (falta credits) | 422 — {"detail":[{"type":"missing","loc":["body","credits"],"msg":"Field required","input":{"name":"Química","act... | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04o |
| P04p | `PUT /courses/3` | `{"name": "Química", "credits": 3}` | 422 (falta active, obligatorio en el PUT) | 422 — {"detail":[{"type":"missing","loc":["body","active"],"msg":"Field required","input":{"name":"Química","cred... | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04p |
| P04q | `PUT /courses/3` | `{"name": "Química", "credits": "abc", "active": true}` | 422 (credits con texto) | 422 — {"detail":[{"type":"int_parsing","loc":["body","credits"],"msg":"Input should be a valid integer, unable to... | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04q |
| P04r | `PUT /courses/3` | `{"name": "Química", "credits": 3, "active": "invalido"}` | 422 (active con texto) | 422 — {"detail":[{"type":"bool_parsing","loc":["body","active"],"msg":"Input should be a valid boolean, unable to... | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04r |
| P04s | `GET /courses/3` | — | 200: el curso 3 conserva los valores de P04i (las peticiones rechazadas no lo cambiaron) | 200 — {"id":3,"name":"Física II","credits":6,"active":true} | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04s |
| P04t | `PUT /courses/9999` | `{"name": "Química", "credits": 3, "active": true}` | 404 y {"detail": "Course not found"} | 404 — {"detail":"Course not found"} | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04t |
| P04u | `PUT /courses/abc` | `{"name": "Química", "credits": 3, "active": true}` | 422 (el id debe ser entero) | 422 — {"detail":[{"type":"int_parsing","loc":["path","course_id"],"msg":"Input should be a valid integer, unable ... | Aprobado | [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) · P04u |

### P05 — DELETE /courses/{course_id}

| Caso | Método y URL | Datos enviados | Resultado esperado | Resultado obtenido | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| P05a | `GET /courses/7` | — | 200: el curso 7 existe antes de eliminarlo | 200 — {"id":7,"name":"Cálculo II","credits":6,"active":true} | Aprobado | [P05-eliminar-curso.txt](evidencias/P05-eliminar-curso.txt) · P05a |
| P05b | `DELETE /courses/7` | — | 200 y {"message": "Course deleted"} | 200 — {"message":"Course deleted"} | Aprobado | [P05-eliminar-curso.txt](evidencias/P05-eliminar-curso.txt) · P05b |
| P05c | `GET /courses/7` | — | 404 (el curso eliminado ya no existe) | 404 — {"detail":"Course not found"} | Aprobado | [P05-eliminar-curso.txt](evidencias/P05-eliminar-curso.txt) · P05c |
| P05d | `GET /courses` | — | 200: la lista ya no incluye el 7 y los cursos 1 al 6 permanecen | 200 — [{"id":1,"name":"Programación II","credits":4,"active":false},{"id":2,"name":"Bases de Datos","credits":4,"... | Aprobado | [P05-eliminar-curso.txt](evidencias/P05-eliminar-curso.txt) · P05d |
| P05e | `DELETE /courses/7` | — | 404 al repetir el DELETE del mismo ID | 404 — {"detail":"Course not found"} | Aprobado | [P05-eliminar-curso.txt](evidencias/P05-eliminar-curso.txt) · P05e |
| P05f | `DELETE /courses/9999` | — | 404 (ID inexistente) | 404 — {"detail":"Course not found"} | Aprobado | [P05-eliminar-curso.txt](evidencias/P05-eliminar-curso.txt) · P05f |
| P05g | `DELETE /courses/abc` | — | 422 (el id debe ser entero) | 422 — {"detail":[{"type":"int_parsing","loc":["path","course_id"],"msg":"Input should be a valid integer, unable ... | Aprobado | [P05-eliminar-curso.txt](evidencias/P05-eliminar-curso.txt) · P05g |

### P06 — POST /students

| Caso | Método y URL | Datos enviados | Resultado esperado | Resultado obtenido | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| P06a | `POST /students` | `{"name": "Ana Pérez", "email": "ana@universidad.edu", "semester": 4, "active": true}` | 201 e ID generado | 201 — {"id":1,"name":"Ana Pérez","email":"ana@universidad.edu","semester":4,"active":true} | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06a |
| P06b | `POST /students` | `{"name": "Luis Gómez", "email": "luis@universidad.edu", "semester": 2}` | 201 y active = true por defecto | 201 — {"id":2,"name":"Luis Gómez","email":"luis@universidad.edu","semester":2,"active":true} | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06b |
| P06c | `POST /students` | `{"name": "Marta Ruiz", "email": "marta@universidad.edu", "semester": 6, "active": false}` | 201 y active = false | 201 — {"id":3,"name":"Marta Ruiz","email":"marta@universidad.edu","semester":6,"active":false} | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06c |
| P06d | `POST /students` | `{"name": "Eva", "email": "eva@universidad.edu", "semester": 3}` | 201 (nombre de 3 caracteres, límite válido) | 201 — {"id":4,"name":"Eva","email":"eva@universidad.edu","semester":3,"active":true} | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06d |
| P06e | `POST /students` | `{"name": "<80 caracteres>", "email": "larga@universidad.edu", "semester": 3}` | 201 (nombre de 80 caracteres, límite válido) | 201 — {"id":5,"name":"EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE","email":"... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06e |
| P06f | `POST /students` | `{"name": "Pedro Ríos", "email": "pedro@universidad.edu", "semester": 1}` | 201 (semestre = 1, límite válido) | 201 — {"id":6,"name":"Pedro Ríos","email":"pedro@universidad.edu","semester":1,"active":true} | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06f |
| P06g | `POST /students` | `{"name": "Sara León", "email": "sara@universidad.edu", "semester": 10}` | 201 (semestre = 10, límite válido) | 201 — {"id":7,"name":"Sara León","email":"sara@universidad.edu","semester":10,"active":true} | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06g |
| P06h | `POST /students` | `{"name": "Jo", "email": "jo@universidad.edu", "semester": 3}` | 422 (nombre de 2 caracteres) | 422 — {"detail":[{"type":"string_too_short","loc":["body","name"],"msg":"String should have at least 3 characters... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06h |
| P06i | `POST /students` | `{"name": "<81 caracteres>", "email": "x@universidad.edu", "semester": 3}` | 422 (nombre de 81 caracteres) | 422 — {"detail":[{"type":"string_too_long","loc":["body","name"],"msg":"String should have at most 80 characters"... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06i |
| P06j | `POST /students` | `{"name": "Juan Mora", "email": "juan@universidad.edu", "semester": 0}` | 422 (semestre = 0) | 422 — {"detail":[{"type":"greater_than_equal","loc":["body","semester"],"msg":"Input should be greater than or eq... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06j |
| P06k | `POST /students` | `{"name": "Juan Mora", "email": "juan@universidad.edu", "semester": 11}` | 422 (semestre = 11) | 422 — {"detail":[{"type":"less_than_equal","loc":["body","semester"],"msg":"Input should be less than or equal to... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06k |
| P06l | `POST /students` | `{"name": "Juan Mora", "email": "", "semester": 3}` | 422 (email vacío) | 422 — {"detail":[{"type":"string_too_short","loc":["body","email"],"msg":"String should have at least 1 character... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06l |
| P06m | `POST /students` | `{"name": "Juan Mora", "email": "   ", "semester": 3}` | 422 (email con solo espacios) | 422 — {"detail":[{"type":"string_too_short","loc":["body","email"],"msg":"String should have at least 1 character... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06m |
| P06n | `POST /students` | `{"email": "juan@universidad.edu", "semester": 3}` | 422 (falta name) | 422 — {"detail":[{"type":"missing","loc":["body","name"],"msg":"Field required","input":{"email":"juan@universida... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06n |
| P06o | `POST /students` | `{"name": "Juan Mora", "semester": 3}` | 422 (falta email) | 422 — {"detail":[{"type":"missing","loc":["body","email"],"msg":"Field required","input":{"name":"Juan Mora","sem... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06o |
| P06p | `POST /students` | `{"name": "Juan Mora", "email": "juan@universidad.edu"}` | 422 (falta semester) | 422 — {"detail":[{"type":"missing","loc":["body","semester"],"msg":"Field required","input":{"name":"Juan Mora","... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06p |
| P06q | `POST /students` | `{"name": "Juan Mora", "email": "juan@universidad.edu", "semester": "abc"}` | 422 (semester con texto) | 422 — {"detail":[{"type":"int_parsing","loc":["body","semester"],"msg":"Input should be a valid integer, unable t... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06q |
| P06r | `POST /students` | `{"name": "Juan Mora", "email": "juan@universidad.edu", "semester": 3, "active": "invalido"}` | 422 (active con texto) | 422 — {"detail":[{"type":"bool_parsing","loc":["body","active"],"msg":"Input should be a valid boolean, unable to... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06r |
| P06s | `GET /students` | — | 200 y siguen 7 estudiantes (las peticiones rechazadas no crearon registros) | 200 — [{"id":1,"name":"Ana Pérez","email":"ana@universidad.edu","semester":4,"active":true},{"id":2,"name":"Luis ... | Aprobado | [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) · P06s |

### P07 — GET /students

| Caso | Método y URL | Datos enviados | Resultado esperado | Resultado obtenido | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| P07a | `GET /students` | — | 200 y [] | 200 — [] | Aprobado | [P07-listar-estudiantes.txt](evidencias/P07-listar-estudiantes.txt) · P07a |
| P07b | `GET /students` | — | 200 y lista con 7 estudiantes, activos e inactivos | 200 — [{"id":1,"name":"Ana Pérez","email":"ana@universidad.edu","semester":4,"active":true},{"id":2,"name":"Luis ... | Aprobado | [P07-listar-estudiantes.txt](evidencias/P07-listar-estudiantes.txt) · P07b |

### P08 — GET /students/{student_id}

| Caso | Método y URL | Datos enviados | Resultado esperado | Resultado obtenido | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| P08a | `GET /students/1` | — | 200 y el estudiante 1 | 200 — {"id":1,"name":"Ana Pérez","email":"ana@universidad.edu","semester":4,"active":true} | Aprobado | [P08-consultar-estudiante.txt](evidencias/P08-consultar-estudiante.txt) · P08a |
| P08b | `GET /students/9999` | — | 404 y {"detail": "Student not found"} | 404 — {"detail":"Student not found"} | Aprobado | [P08-consultar-estudiante.txt](evidencias/P08-consultar-estudiante.txt) · P08b |
| P08c | `GET /students/abc` | — | 422 (el id debe ser entero) | 422 — {"detail":[{"type":"int_parsing","loc":["path","student_id"],"msg":"Input should be a valid integer, unable... | Aprobado | [P08-consultar-estudiante.txt](evidencias/P08-consultar-estudiante.txt) · P08c |

### P09 — Persistencia e integración

| Caso | Método y URL | Datos enviados | Resultado esperado | Resultado obtenido | Estado | Evidencia |
| --- | --- | --- | --- | --- | --- | --- |
| P09a | `GET /courses` | — | 200: cursos ANTES de reiniciar (se guarda la foto) | 200 — [{"id":1,"name":"Programación II","credits":4,"active":false},{"id":2,"name":"Bases de Datos","credits":4,"... | Aprobado | [P09-persistencia.txt](evidencias/P09-persistencia.txt) · P09a |
| P09b | `GET /students` | — | 200: estudiantes ANTES de reiniciar (se guarda la foto) | 200 — [{"id":1,"name":"Ana Pérez","email":"ana@universidad.edu","semester":4,"active":true},{"id":2,"name":"Luis ... | Aprobado | [P09-persistencia.txt](evidencias/P09-persistencia.txt) · P09b |
| P09c | `GET /courses` | — | 200: los cursos son idénticos a los de antes del reinicio (incluye cambios de PUT y sin el curso 7) | 200 — [{"id":1,"name":"Programación II","credits":4,"active":false},{"id":2,"name":"Bases de Datos","credits":4,"... | Aprobado | [P09-persistencia.txt](evidencias/P09-persistencia.txt) · P09c |
| P09d | `GET /students` | — | 200: los estudiantes son idénticos a los de antes del reinicio | 200 — [{"id":1,"name":"Ana Pérez","email":"ana@universidad.edu","semester":4,"active":true},{"id":2,"name":"Luis ... | Aprobado | [P09-persistencia.txt](evidencias/P09-persistencia.txt) · P09d |
| P09e | `GET /courses/1` | — | 200: el PUT del curso 1 permanece (Programación II, 4, false) | 200 — {"id":1,"name":"Programación II","credits":4,"active":false} | Aprobado | [P09-persistencia.txt](evidencias/P09-persistencia.txt) · P09e |
| P09f | `GET /courses/7` | — | 404: el curso eliminado sigue ausente | 404 — {"detail":"Course not found"} | Aprobado | [P09-persistencia.txt](evidencias/P09-persistencia.txt) · P09f |
| P09g | `POST /courses` | `{"name": "Curso de integración", "credits": 2, "active": true}` | 201: se crea un curso nuevo (para comprobar que no afecta a estudiantes) | 201 — {"id":7,"name":"Curso de integración","credits":2,"active":true} | Aprobado | [P09-persistencia.txt](evidencias/P09-persistencia.txt) · P09g |
| P09h | `GET /students` | — | 200: la lista de estudiantes no cambió tras crear un curso | 200 — [{"id":1,"name":"Ana Pérez","email":"ana@universidad.edu","semester":4,"active":true},{"id":2,"name":"Luis ... | Aprobado | [P09-persistencia.txt](evidencias/P09-persistencia.txt) · P09h |
| P09i | `POST /students` | `{"name": "Estudiante integración", "email": "integra@universidad.edu", "semester": 5}` | 201: se crea un estudiante nuevo (para comprobar que no afecta a los cursos) | 201 — {"id":8,"name":"Estudiante integración","email":"integra@universidad.edu","semester":5,"active":true} | Aprobado | [P09-persistencia.txt](evidencias/P09-persistencia.txt) · P09i |
| P09j | `GET /courses` | — | 200: los cursos solo incluyen el curso creado en P09g (los anteriores no cambiaron) | 200 — [{"id":1,"name":"Programación II","credits":4,"active":false},{"id":2,"name":"Bases de Datos","credits":4,"... | Aprobado | [P09-persistencia.txt](evidencias/P09-persistencia.txt) · P09j |
| P09k | `database.db (archivos .db y tablas)` | — | Un solo archivo database.db con las tablas course y student (sin students.db) | Archivos: database.db. Tablas: course, student | Aprobado | [P09-persistencia.txt](evidencias/P09-persistencia.txt) · P09k |

## Fichas de las pruebas principales

Para no repetir información, el resto de las ejecuciones se describen en las tablas anteriores. Estas fichas explican paso a paso las pruebas que representan cada operación.

### P01a — Crear un curso válido

- Fecha y hora: 15/10/2026 20:40:48 (hora de Colombia)
- Objetivo: comprobar que se puede crear un curso con datos válidos y que la API le asigna un ID.
- Preparación: base de datos vacía (la lista de cursos devolvió `[]` en P02a).
- Método y URL: POST http://127.0.0.1:8000/courses
- Datos enviados: `{"name": "Desarrollo Web II", "credits": 3, "active": true}`
- Pasos: se envió el JSON a `POST /courses` y se revisó el estado y el cuerpo de la respuesta.
- Resultado esperado: 201 e ID generado
- Resultado obtenido: `201 — {"id":1,"name":"Desarrollo Web II","credits":3,"active":true}`
- Comprobación posterior: P03a consulta `GET /courses/1` y devuelve el mismo curso.
- Estado: Aprobado
- Observaciones: ninguna; el ID lo generó SQLite, no se envió en la petición.
- Evidencia: [P01-crear-curso.txt](evidencias/P01-crear-curso.txt) (sección P01a)

### P04b — Actualizar un curso existente con PUT

- Fecha y hora: 15/10/2026 20:40:48 (hora de Colombia)
- Objetivo: modificar un curso sin crear otro registro y sin cambiar su ID.
- Preparación: el curso 1 existía con los valores `Desarrollo Web II`, 3 créditos y `active: true` (P04a, consulta antes del PUT).
- Método y URL: PUT http://127.0.0.1:8000/courses/1
- Datos enviados: `{"name": "Programación II", "credits": 4, "active": false}`
- Pasos: se envió el cuerpo completo (los tres campos) a `PUT /courses/1`.
- Resultado esperado: 200, mismo ID y nuevos valores
- Resultado obtenido: `200 — {"id":1,"name":"Programación II","credits":4,"active":false}`
- Comprobación posterior: P04c consulta `GET /courses/1` (mismos valores nuevos, mismo ID) y P04d confirma que siguen siendo 7 cursos, con los mismos IDs.
- Estado: Aprobado
- Observaciones: el valor `false` en `active` se guardó correctamente; no se descarta por ser falso.
- Evidencia: [P04-actualizar-curso.txt](evidencias/P04-actualizar-curso.txt) (sección P04b)

### P05b — Eliminar un curso existente

- Fecha y hora: 15/10/2026 20:40:48 (hora de Colombia)
- Objetivo: eliminar un curso por su ID y comprobar que el cambio queda guardado.
- Preparación: el curso 7 existía (P05a devolvió 200).
- Método y URL: DELETE http://127.0.0.1:8000/courses/7
- Datos enviados: `—`
- Pasos: se envió `DELETE /courses/7` sin cuerpo.
- Resultado esperado: 200 y {"message": "Course deleted"}
- Resultado obtenido: `200 — {"message":"Course deleted"}`
- Comprobación posterior: P05c: `GET /courses/7` devuelve 404; P05d: la lista contiene solo los cursos 1 al 6; P05e: repetir el DELETE devuelve 404.
- Estado: Aprobado
- Observaciones: el mensaje se devuelve después de confirmar la transacción con `commit()`.
- Evidencia: [P05-eliminar-curso.txt](evidencias/P05-eliminar-curso.txt) (sección P05b)

### P06a — Crear un estudiante válido

- Fecha y hora: 15/10/2026 20:40:48 (hora de Colombia)
- Objetivo: comprobar que se puede crear un estudiante en su propia tabla.
- Preparación: lista de estudiantes vacía (P07a devolvió `[]`); los cursos ya existían.
- Método y URL: POST http://127.0.0.1:8000/students
- Datos enviados: `{"name": "Ana Pérez", "email": "ana@universidad.edu", "semester": 4, "active": true}`
- Pasos: se envió el JSON a `POST /students`.
- Resultado esperado: 201 e ID generado
- Resultado obtenido: `201 — {"id":1,"name":"Ana Pérez","email":"ana@universidad.edu","semester":4,"active":true}`
- Comprobación posterior: P08a consulta `GET /students/1` y devuelve el mismo estudiante.
- Estado: Aprobado
- Observaciones: ninguna; el estudiante usa la misma `database.db` que los cursos.
- Evidencia: [P06-crear-estudiante.txt](evidencias/P06-crear-estudiante.txt) (sección P06a)

### P09c — Persistencia después de reiniciar Uvicorn

- Fecha y hora: 15/10/2026 20:40:50 (hora de Colombia)
- Objetivo: demostrar que los datos no viven solo en memoria.
- Preparación: P09a y P09b guardaron una foto de los cursos y estudiantes. Después se detuvo Uvicorn con Ctrl+C y se volvió a iniciar desde la misma carpeta (los logs de ambos eventos están en la evidencia).
- Método y URL: GET http://127.0.0.1:8000/courses
- Datos enviados: `—`
- Pasos: se consultó `GET /courses` tras el reinicio y se comparó con la foto anterior.
- Resultado esperado: 200: los cursos son idénticos a los de antes del reinicio (incluye cambios de PUT y sin el curso 7)
- Resultado obtenido: `200 — [{"id":1,"name":"Programación II","credits":4,"active":false},{"id":2,"name":"Bases de Datos","credits":4,"...`
- Comprobación posterior: P09d (estudiantes idénticos), P09e (el PUT del curso 1 permanece) y P09f (el curso 7 eliminado sigue ausente).
- Estado: Aprobado
- Observaciones: la comparación fue exacta, registro por registro.
- Evidencia: [P09-persistencia.txt](evidencias/P09-persistencia.txt) (sección P09c)

## Observaciones

- **Reutilización de ID tras eliminar el último registro:** al eliminar el curso 7 (que era el último) y crear después un curso nuevo (P09g), SQLite le asignó otra vez el ID 7. Es el comportamiento normal de una clave primaria sin `AUTOINCREMENT`: toma el máximo existente más uno. No es un fallo del proyecto.
- **Email de estudiantes:** se valida que no esté vacío (también si solo tiene espacios, P06m). El formato del correo y su unicidad quedan fuera del alcance básico, según el enunciado.
- **Nombres de cursos repetidos:** el proyecto base no exige nombres únicos, así que no se probó como regla.
- **Una sola base de datos:** P09k comprueba que solo existe `database.db`, con las tablas `course` y `student`, y que no se creó `students.db`.
- No hubo pruebas fallidas, por lo que no fue necesario repetir ninguna ejecución.
