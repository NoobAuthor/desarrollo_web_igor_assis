# Tarea 1 - Desarrollo Web

Este repositorio contiene el prototipo de una aplicación web para gestionar actividades recreativas, desarrollado como parte de la Tarea 1 del curso CC5002. La aplicación está construida únicamente con HTML, CSS y JavaScript, y cumple con los requerimientos especificados en el enunciado.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

```bash
/desarrollo_web_nombre_apellido/
├── index.html                # Portada con bienvenida y últimas 5 actividades
├── actividad.html    # Formulario para agregar una nueva actividad
├── listado.html  # Listado detallado de todas las actividades
├── detalle.html    # Detalles completos de una actividad seleccionada
├── estadisticas.html         # Página con gráficos estáticos de estadísticas
├── styles.css                # Estilos CSS para toda la aplicación
├── script.js                 # Lógica JavaScript para interacciones y validaciones
├── data.js                   # Datos de ejemplo para las actividades
├── fotos/                    # Carpeta con imágenes placeholder
│   ├── foto1.jpg
│   ├── foto2.jpg
│   └── ...
└── README.md                 # Este archivo
```

## Descripción General

La aplicación permite a los usuarios:

- Ver una portada con un mensaje de bienvenida y un resumen de las últimas 5 actividades.
- Agregar nuevas actividades recreativas a través de un formulario con validaciones.
- Ver un listado detallado de todas las actividades.
- Ver los detalles completos de una actividad específica, incluyendo fotos interactivas.
- Acceder a una página de estadísticas con gráficos estáticos.

Este prototipo no requiere un servidor web ni almacena datos de forma persistente; toda la información es manejada en memoria mediante JavaScript.

## Decisiones en `script.js`

El archivo `script.js` contiene la lógica principal para la interacción del usuario y las validaciones del formulario. A continuación, se detallan las decisiones clave tomadas en su implementación:

### 1. **Poblamiento Dinámico de Regiones y Comunas**

- **Qué hace**: Al seleccionar una región en el formulario, las comunas correspondientes se cargan automáticamente en el menú de selección.
- **Implementación**: Se utiliza un objeto `regionesComunas` definido en `data.js` para mapear regiones a comunas, y un evento `change` actualiza el DOM dinámicamente.
- **Justificación**: Mejora la experiencia del usuario al evitar recargas de página y simplifica la gestión de datos geográficos sin necesidad de múltiples archivos HTML.

### 2. **Prellenado de Fechas**

- **Qué hace**: Los campos de fecha y hora de inicio se prellenan con el momento actual, y el término se establece tres horas después.
- **Implementación**: Se usa `new Date()` para obtener la fecha actual y se ajusta el formato para los campos `<input type="datetime-local">`.
- **Justificación**: Reduce el esfuerzo del usuario al ingresar datos y asegura un formato consistente, disminuyendo errores.

### 3. **Gestión de Medios de Contacto**

- **Qué hace**: Permite agregar hasta 5 medios de contacto (ej. correo, teléfono) con campos dinámicos que aparecen según la selección.
- **Implementación**: Un botón "Agregar medio de contacto" crea nuevos elementos en el DOM, con un límite máximo de 5 iteraciones.
- **Justificación**: Ofrece flexibilidad sin abrumar la interfaz inicial, optimizando recursos y manteniendo la usabilidad.

### 4. **Validaciones en JavaScript**

- **Qué hace**: Valida todos los campos del formulario (ej. nombre, fechas, medios de contacto) antes del envío.
- **Implementación**: Se ejecuta una función en el evento `submit` que verifica condiciones específicas y muestra mensajes de error personalizados.
- **Justificación**: Cumple con el requisito de no usar atributos HTML como `required`, permitiendo mayor control y personalización en la validación.

### 5. **Manejo de Fotos**

- **Qué hace**: Permite cargar hasta 5 fotos mediante campos de archivo que se añaden dinámicamente.
- **Implementación**: Similar a los medios de contacto, un botón "Agregar otra foto" inserta nuevos `<input type="file">` con un límite de 5.
- **Justificación**: Mantiene el formulario limpio y escalable, adaptándose a las necesidades del usuario sin sobrecargar la interfaz.

### 6. **Confirmación de Envío**

- **Qué hace**: Antes de procesar el formulario, muestra un mensaje de confirmación; si se acepta, simula un envío exitoso y redirige a `index.html`.
- **Implementación**: Usa `confirm()` para la interacción y `window.location` para la redirección.
- **Justificación**: Simula una experiencia real de envío sin backend, mejorando la percepción de funcionalidad completa.

### 7. **Interactividad en el Listado y Detalles**

- **Qué hace**: Las filas del listado en `listado_actividades.html` son clicables y redirigen a `detalle_actividad.html` con un parámetro en la URL.
- **Implementación**: Eventos `click` en las filas usan `window.location` para pasar un identificador único.
- **Justificación**: Simplifica la navegación sin frameworks complejos, manteniendo la aplicación ligera y funcional.

### 8. **Modal para Fotos en Detalles**

- **Qué hace**: Al hacer clic en una foto en `detalle_actividad.html`, se abre un modal con la imagen ampliada a 800x600 píxeles.
- **Implementación**: Un evento `click` muestra un elemento `<div>` estilizado como modal con la imagen seleccionada.
- **Justificación**: Mejora la visualización de fotos sin abandonar la página, optimizando la experiencia del usuario.

## Notas Adicionales

- **Datos de Ejemplo**: Los datos de las actividades están en `data.js` y se usan para poblar dinámicamente las páginas.
- **Imágenes**: Las imágenes en `fotos/` son placeholders; en una versión real, se implementarían subidas de archivos.
- **Gráficos Estáticos**: En `estadisticas.html`, los gráficos son imágenes fijas; podrían evolucionar a dinámicos con herramientas como Chart.js.

## Instrucciones de Uso

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/NoobAuthor/desarrollo_web_igor_assis.git
   ```

2. Abrir `index.html` en un navegador para explorar la aplicación.

3. Usar el menú para agregar actividades, ver listados, detalles y estadísticas.

## Requerimientos Cumplidos

- Construido solo con HTML5, CSS3 y JavaScript.
- Validaciones exclusivamente en JavaScript, sin atributos HTML nativos.
- Interactividad en formularios, listados y detalles según el enunciado.
- Diseño responsivo y funcionalidad completa.
