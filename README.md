# Desarrollo Web - Igor Assis

Este repositorio contiene las implementaciones de las tareas del curso CC5002 - Desarrollo de Aplicaciones Web.

## Autor
Igor Assis Passos de Souza

## Estructura del Proyecto

```
desarrollo_web_igor_assis/
├── README.md          # Este archivo
├── tarea3/           # Implementación de la Tarea 3
│   ├── app.py
│   ├── models.py
│   ├── static/
│   ├── templates/
│   └── ...
└── tarea4/           # Implementación de la Tarea 4 (ACTUAL)
    ├── app.py
    ├── models.py
    ├── database/     # Scripts SQL
    ├── docs/         # Documentación
    ├── scripts/      # Scripts de utilidad
    ├── static/       # CSS, JS, imágenes
    └── templates/    # Plantillas HTML
```

## Tareas Implementadas

### Tarea 3 - Sistema de Comentarios
- ✅ Aplicación web Flask para gestión de actividades recreativas
- ✅ Sistema de comentarios AJAX
- ✅ Validación de formularios
- ✅ Carga dinámica de regiones/comunas
- ✅ Estadísticas con gráficos

### Tarea 4 - Sistema de Valoraciones (ACTUAL)
- ✅ Todas las funcionalidades de Tarea 3
- ✅ Sistema de valoraciones de 1-5 estrellas
- ✅ Promedio de calificaciones
- ✅ Estadísticas de valoraciones
- ✅ APIs REST para comentarios y valoraciones
- ✅ Interfaz mejorada con ratings visuales

## Instalación Rápida - Tarea 4

### Opción 1: Script Automático
```bash
cd tarea4
chmod +x setup.sh
./setup.sh
```

### Opción 2: Manual
```bash
cd tarea4

# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
mysql -u root -p < database/tarea2.sql
mysql -u cc5002 -p tarea2 < database/tabla-comentario.sql
mysql -u cc5002 -p tarea2 < database/tabla-nota.sql
mysql -u cc5002 -p tarea2 < database/region-comuna.sql

# Ejecutar aplicación
python app.py
```

## Uso

1. **Acceder a la aplicación**: http://localhost:5000
2. **Agregar actividades**: Formulario con validación y carga de fotos
3. **Valorar actividades**: Sistema de 1-5 estrellas
4. **Comentar actividades**: Sistema AJAX en tiempo real
5. **Ver estadísticas**: Gráficos interactivos con Highcharts

## Funcionalidades Principales

- 📝 **Gestión de Actividades**: Crear, listar, ver detalles
- ⭐ **Sistema de Valoraciones**: Calificar actividades de 1-5 estrellas
- 💬 **Sistema de Comentarios**: Comentarios en tiempo real
- 📊 **Estadísticas**: Gráficos interactivos de actividades y valoraciones
- 🌍 **Localización**: Regiones y comunas de Chile
- 📱 **Responsive**: Diseño adaptativo
- 🔒 **Seguridad**: Validación de formularios, CSRF protection

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Base de Datos**: MySQL
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Gráficos**: Highcharts
- **ORM**: SQLAlchemy
- **Validación**: Flask-WTF

## Documentación

- `tarea4/README.md` - Documentación específica de la Tarea 4
- `tarea4/SETUP.md` - Guía detallada de instalación
- `tarea4/docs/` - Documentación adicional y enunciados

## Estructura de Base de Datos

### Tablas principales:
- `actividad` - Actividades recreativas
- `comentario` - Comentarios de usuarios
- `nota` - Valoraciones de actividades
- `region` / `comuna` - Datos geográficos de Chile
- `foto` - Imágenes de actividades

## APIs Disponibles

### Comentarios
- `GET /api/comentarios/<id>` - Obtener comentarios
- `POST /api/comentarios/<id>` - Agregar comentario

### Valoraciones
- `GET /api/notas/<id>` - Obtener promedio de valoraciones
- `POST /api/notas/<id>` - Agregar valoración

### Estadísticas
- `GET /api/estadisticas/actividades_por_dia`
- `GET /api/estadisticas/actividades_por_tipo`
- `GET /api/estadisticas/promedio_notas`

## Requisitos del Sistema

- Python 3.7+
- MySQL 5.7+ o MariaDB
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

## Contribución

Este es un proyecto académico para el curso CC5002. Las mejoras y correcciones son bienvenidas.

## Licencia

Proyecto académico - Universidad de Chile