# Backend - Crear Paciente

Este repositorio contiene el servicio backend para la gestión y registro de pacientes dentro de la plataforma **ConectaCare**. El servicio expone múltiples endpoints que permiten almacenar información médica, signos vitales, historial clínico, entre otros datos relevantes.

---

## Requisitos Previos

Antes de ejecutar este servicio, asegúrate de tener instalado:

- Python 3.10+
- pip
- MongoDB Atlas o una instancia compatible

---

## Instalación

1. **Clona el repositorio:**

```bash
git clone https://github.com/tu_usuario/backend-crear-paciente.git
cd backend-crear-paciente
```

2. **Instala las dependencias:**

Se recomienda crear un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

Luego instala las librerías necesarias:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuración

1. **Archivo `.env`:**

Debes crear un archivo `.env` en la raíz del proyecto. Para ello:

```bash
cp .env.example .env
```

Abre el archivo `.env` y modifica la variable `MONGO_URI` con la URI de tu instancia de MongoDB, por ejemplo:

```env
MONGO_URI=mongodb+srv://usuario:contraseña@cluster.mongodb.net/?retryWrites=true&w=majority
```

2. **Archivo `client.py`:**

Es **obligatorio** agregar un archivo llamado `client.py` dentro del directorio `app/db`. Este archivo contiene la conexión a la base de datos y debe tener una estructura específica que será proporcionada por el **dueño del proyecto**.

  **Importante:** Si no cuentas con el contenido correcto del archivo `client.py`, solicita el formato directamente al desarrollador responsable del backend.

---

## ▶️ Ejecución del servidor

Para correr el backend localmente:

```bash
uvicorn app.main:app --reload --port 8002
```

>  El puerto `8002` es el recomendado para evitar conflictos con otros servicios en ejecución. Esto está indicado en los comentarios del archivo `main.py`.

---

## 📁 Estructura del proyecto

```
backend-crear-paciente/
│
├── app/
│   ├── db/
│   │   └── client.py       # Debes colocar aquí el archivo con la conexión a MongoDB
│   ├── models/             # Modelos Pydantic usados en las rutas
│   ├── routers/            # Endpoints organizados por funcionalidad
│   ├── schemas/            # Funciones para serializar documentos de MongoDB
│   └── main.py             # Archivo principal de arranque de FastAPI
│
├── .env.example            # Plantilla del archivo de entorno
├── requirements.txt        # Librerías necesarias
└── README.md               # Este archivo
```

---

##  Pruebas

Por ahora, el backend no incluye pruebas automatizadas, pero se recomienda usar herramientas como **Postman** o **Thunder Client** para probar los endpoints disponibles. La documentación de cada ruta está disponible automáticamente al correr el servidor en:

```
http://localhost:8002/docs
```

---

##  Notas finales

- Mantén el archivo `.env` fuera del control de versiones por seguridad.
- Si actualizas las dependencias, no olvides actualizar el `requirements.txt` usando `pip freeze > requirements.txt`.
- En caso de errores con la conexión a MongoDB, revisa que el `MONGO_URI` tenga los permisos correctos y acceso desde tu IP.
