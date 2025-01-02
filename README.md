# Gestor de cursos
Este es un sistema de administración de cursos. El proyecto está implementado con Django como backend y Bootstrap como framework de diseño frontend. El objetivo es facilitar la gestión de cursos, alumnos, sedes y permitir operaciones administrativas como la creación, eliminación y visualización de los datos.


El sistema tiene las siguientes funcionalidades:

1. **Administración de Alumnos**:
   - Crear y eliminar alumnos.
   - Verificar su identidad en cuitonline.
   - Obtener los datos detallados de un alumno.
   - Listar alumnos con filtros por nombre, apellido, fecha de nacimiento y edad.
   - Agregar o modificar notas.
     
2. **Administración de Cursos**:
   - Crear y eliminar cursos.
   - Agregar y eliminar alumnos de cursos.
   - Listar cursos con filtros por duración, año, fecha de inicio, sede y costo.
   - Ver los detalles de un curso con los alumnos que están inscriptos.

3. **Administración de Sedes**:
   - Listar sedes con filtros por ciudad y nombre.
   - Ver los detalles de una sede y los cursos que se dictan en ella.

### Otras funcionalidades

1. **Cursos**:
   - Incluir las notas de los alumnos en cada curso (aprobación y nota promedio).
   - Estado de los cursos (activo-finalizado-aún no comenzó).

2. **Historial de Cursos de Alumnos**:
   - Listado de cursos actuales de un alumno, con nombre, fecha de inicio y sede.
   - Historial completo de cursos tomados por el alumno.

3. **Operaciones Avanzadas**:
   - Paginación en los listados de alumnos, cursos y sedes.

4. **Sistema de Login**:
   - Restringir el acceso a ciertas funciones del sistema mediante un sistema de autenticación.

###  Adicionales

1. **Búsqueda de DNI**:
   - Facilita la verificacion de datos en cuitonline.com.

2. **Base de Datos**:
   - Utilización de PostgreSQL para almacenar los datos de la aplicación.
