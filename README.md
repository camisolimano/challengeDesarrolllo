# Gestor de cursos
Este es un sistema de administración de cursos desarrollado para DBlandIT. El proyecto está implementado con Django como backend y Bootstrap como framework de diseño frontend. El objetivo es gestionar cursos, alumnos, sedes y permitir operaciones administrativas como la creación, eliminación y visualización de los datos.


El sistema tiene las siguientes funcionalidades:

1. **Administración de Alumnos**:
   - Listar alumnos con filtros por nombre, apellido, fecha de nacimiento y edad.
   - Obtener los datos detallados de un alumno.
   - Crear y eliminar alumnos.

2. **Administración de Cursos**:
   - Listar cursos con filtros por duración, año, fecha de inicio, sede y costo.
   - Crear y eliminar cursos.
   - Agregar y eliminar alumnos de cursos.
   - Ver los detalles de un curso con los alumnos que están inscriptos.

3. **Administración de Sedes**:
   - Listar sedes con filtros por ciudad y nombre.
   - Ver los detalles de una sede y los cursos que se dictan en ella.

### Otras funcionalidades

1. **Notas de los Cursos**:
   - Incluir las notas de los alumnos en cada curso (aprobación y nota promedio).
   - Indicar si los cursos son activos o finalizados.

2. **Historial de Cursos de Alumnos**:
   - Obtener el listado de cursos actuales de un alumno, con nombre, fecha de inicio y sede.
   - Ver el historial completo de cursos tomados por el alumno.

3. **Operaciones Avanzadas**:
   - Permitir modificar las notas de los alumnos.
   - Incluir paginación en los listados de alumnos, cursos y sedes.

4. **Sistema de Login**:
   - Restringir el acceso a ciertas funciones del sistema mediante un sistema de autenticación.

###  Adicionales

1. **Búsqueda de DNI**:
   - Un botón en el campo de DNI que permita buscar información en cuitonline.com.

2. **Base de Datos**:
   - Utilización de PostgreSQL para almacenar los datos de la aplicación, con manejo de variables de entorno para la configuración de la base de datos.
