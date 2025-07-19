## [1.0.0] - 2025-07-19
### Añadido
- Estructura inicial del servicio `backend-crear-paciente` usando **FastAPI**.
- Creación del archivo `.env.example` como plantilla para configurar la conexión con MongoDB.
- Inclusión del archivo `README.md` con instrucciones claras de uso e instalación.
- Carpeta `app/routers` con endpoints para la gestión de pacientes.
- Carpeta `app/models` con modelos de Pydantic para representar entidades del sistema.
- Middleware de seguridad JWT para autenticación con token.
- Validación del esquema de pacientes y subdocumentos (meals, signos vitales, etc).
- Documentación automática de endpoints vía Swagger/OpenAPI.
- **Dependencia `get_current_user`**:
  - Ubicada en `app/dependencies/auth.py`.
  - Valida el token JWT recibido en el header `Authorization`.
  - Decodifica el token y retorna el ID del usuario autenticado.

- **Observabilidad con Prometheus**:
  - Contadores de peticiones por endpoint.
  - Tiempos de respuesta por ruta.
  - Conteo de errores por endpoint.
  - Exposición del endpoint `/metrics` para integración con Prometheus.

### Cambios
- Se requiere incluir un archivo `client.py` dentro de `app/db/` con una estructura específica para inicializar la base de datos. Este archivo **no está incluido** en el repositorio público y debe solicitarse al dueño del proyecto.
- El archivo `.env.example` debe ser renombrado a `.env` y debe contener la URI de MongoDB.
- Se recomienda ejecutar el backend en el puerto especificado en los comentarios del archivo `main.py` para evitar conflictos con otros servicios.

### Dependencias
- Se debe instalar todo lo listado en `requirements.txt` para asegurar compatibilidad.
