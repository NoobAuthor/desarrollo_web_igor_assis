# Tarea 2 - CC5002

## Resumen del Proyecto

Aplicación web para la gestión de actividades recreativas, desarrollada con Flask y MySQL. Permite agregar, listar y ver detalles de actividades, cumpliendo con los requisitos de la Tarea 2 del curso.

## Funcionalidades Implementadas

- **Portada:** Muestra mensaje de bienvenida, menú y últimas 5 actividades.
- **Agregar Actividad:** Formulario con validaciones (JS y servidor), carga de fotos, contactos múltiples, y guardado en la base de datos.
- **Listado de Actividades:** Listado paginado (5 por página), con navegación y acceso a detalle.
- **Detalle de Actividad:** Visualización completa de la actividad, contactos y fotos.
- **Estadísticas:** Página placeholder, como indica el enunciado.
- **AJAX:** Carga dinámica de comunas según región seleccionada.

## Instalación y Setup

1. Instala las dependencias:
   ```
   pip install -r requirements.txt
   ```
2. Crea la base de datos y carga los datos:
   - Ejecuta `tarea2.sql` y luego `region-comuna.sql` en tu MySQL:
     ```
     mysql -u cc5002 -p < tarea2.sql
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
- **Estadísticas:** `/estadisticas` (placeholder)

## Notas

- **Validación:** Todos los formularios cumplen HTML5/CSS3 y deben validarse en [W3C HTML](https://validator.w3.org/) y [W3C CSS](https://jigsaw.w3.org/css-validator/).
- **Estadísticas:** La sección estará disponible en la próxima entrega, como indica el enunciado.

## Entrega

- Sube el código a un repositorio público en GitHub, rama `Tarea 2`.
- Incluye este README y los scripts SQL.
- Entrega la URL del repositorio en u-cursos.
- (Opcional) Adjunta un zip como respaldo.

## Autor

- Igor Assis Passos de Souza

## Estructura

- `app.py`: Aplicación principal Flask
- `models.py`: Modelos SQLAlchemy (por crear)
- `static/`: Archivos estáticos (CSS, fotos)
- `templates/`: Plantillas HTML Jinja2

## Notas

- Reutiliza los formularios y validaciones de la Tarea 1.
- Ver instrucciones en el enunciado para detalles de entrega y requisitos.
