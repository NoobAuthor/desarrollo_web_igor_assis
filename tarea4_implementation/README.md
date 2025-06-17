# Tarea 4 - CC5002

## Resumen del Proyecto

Aplicación web para la gestión de actividades recreativas, desarrollada con Flask y MySQL. Permite agregar, listar, ver detalles, comentar y valorar actividades, cumpliendo con los requisitos de la Tarea 4 del curso.

## Funcionalidades Implementadas

- **Portada:** Muestra mensaje de bienvenida, menú y últimas 5 actividades con valoraciones.
- **Agregar Actividad:** Formulario con validaciones (JS y servidor), carga de fotos, contactos múltiples, y guardado en la base de datos.
- **Listado de Actividades:** Listado paginado (5 por página), con navegación, acceso a detalle y valoraciones.
- **Detalle de Actividad:** Visualización completa de la actividad, contactos, fotos, comentarios y sistema de valoración.
- **Sistema de Comentarios:** Funcionalidad AJAX para agregar y visualizar comentarios en tiempo real.
- **Sistema de Valoraciones:** Calificación de actividades de 1 a 5 estrellas con promedio dinámico.
- **Estadísticas:** Gráficos interactivos incluyendo estadísticas de valoraciones por actividad.
- **AJAX:** Carga dinámica de comunas, comentarios y valoraciones.

## Instalación y Setup

1. Instala las dependencias:

   ```
   pip install -r requirements.txt
   ```

2. Crea la base de datos y carga los datos:
   - Ejecuta `tarea2.sql`, `tabla-comentario.sql`, `tabla-nota.sql` y luego `region-comuna.sql` en tu MySQL:

     ```
     mysql -u cc5002 -p < tarea2.sql
     mysql -u cc5002 -p tarea2 < tabla-comentario.sql
     mysql -u cc5002 -p tarea2 < tabla-nota.sql
     mysql -u cc5002 -p tarea2 < region-comuna.sql
     ```

3. Ejecuta la app:

   ```
   python app.py
   ```

## Uso

- **Portada:** [http://localhost:5000/](http://localhost:5000/)
- **Agregar Actividad:** `/agregar`
- **Listado de Actividades:** `/listado`
- **Detalle de Actividad:** `/actividad/<id>`
- **Estadísticas:** `/estadisticas` (con gráficos de valoraciones)

## Nuevas Funcionalidades Tarea 4

### Sistema de Comentarios
- Permite agregar comentarios a cualquier actividad
- Validación de nombre (3-80 caracteres) y texto (mínimo 5 caracteres)
- Carga dinámica de comentarios sin recargar la página

### Sistema de Valoraciones
- Calificación de actividades de 1 a 5 estrellas
- Cálculo automático del promedio de valoraciones
- Visualización de estrellas en listados y detalles
- Estadísticas de valoraciones en la página de estadísticas

### APIs REST (AJAX)
- `GET/POST /api/comentarios/<id>`: Gestión de comentarios
- `GET/POST /api/notas/<id>`: Gestión de valoraciones
- `GET /api/estadisticas/promedio_notas`: Estadísticas de valoraciones

## Notas

- **Validación:** Todos los formularios cumplen HTML5/CSS3 y deben validarse en [W3C HTML](https://validator.w3.org/) y [W3C CSS](https://jigsaw.w3.org/css-validator/).
- **Base de Datos:** Se agregaron las tablas `comentario` y `nota` para la funcionalidad de la Tarea 4.
- **AJAX:** Todas las funcionalidades de comentarios y valoraciones funcionan sin recargar la página.

## Autor

- Igor Assis Passos de Souza

## Estructura

- `app.py`: Aplicación principal Flask con APIs REST
- `models.py`: Modelos SQLAlchemy (Actividad, Comentario, Nota, etc.)
- `static/`: Archivos estáticos (CSS, JS, fotos)
- `templates/`: Plantillas HTML Jinja2
- `tabla-comentario.sql`: Script para crear tabla de comentarios
- `tabla-nota.sql`: Script para crear tabla de valoraciones
- `tarea2.sql`: Script principal de base de datos
- `region-comuna.sql`: Datos de regiones y comunas
