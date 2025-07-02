# 👟 Chapiritas V2
_La API de Chacharitas para traer tu sitio favorito del navegador a tu celular_

Chapiritas es una  API REST moderna y robusta para el e-commerce de chacharitas, un sitio web que tiene como propósito la compra y venta de productos de cuidado de bebé de segunda mano.

La API está desarrollada con FastAPI y SQLModel. Esta aplicación proporciona todas las funcionalidades necesarias para gestionar un catálogo de productos, usuarios y autenticación, los cuales son los únicos módulos con los que la app móvil estará funcionando por el momento.

##  FAQ

- **"¿Qué pasó con chapiritas V1?"**
  - Fue una versión preliminar también hecha con FastAPI cuando estabamos empezando a aprenderlo. Si bien esta API abarcaba todos los módulos de Chacharitas algunos de los endpoints no funcionaban, además de que varios esquemas y modelos estaban desactualizados conforme a versiones anteriores de la base de datos. Por eso se tomó la decisión de rehacerlo.
- **"¿Qué tecnologías se utilizan en el proyecto?"**
  - La columna vertebral del proyecto se conforma de 2 componentes principales: FastAPI y SQLModel, este último trabajando detrás de bambalinas con SQLAlchemy y Pydantic. Fuera de estas librerías anteriormente mencionadas, el proyecto utiliza otras librerías que ocupan un rol secundario como Jinja2 para las plantillas de los correos y FastAPI Mail para su envío.
- **"¿Hay algo importante que necesite saber antes de ejecutar el proyecto?"**
  - Los modelos de SQLModel dentro del proyecto están hechos para trabajar con las tablas que genera la versión web de Chacharitas por medio de las migraciones de Laravel, por lo que realmente esta API jamás creará por si sola la base de datos. El único motivo por el cual se crearon los modelos fue para poder facilitar la generación de las rutas 
  

## 🚀 Características

- **API REST completa** con FastAPI
- **Autenticación JWT** con verificación por email
- **Gestión de productos** con filtros avanzados
- **Categorización completa** (marcas, categorías, colores, materiales, tallas, géneros)
- **Subida de imágenes** para productos
- **Base de datos MySQL** con SQLModel/SQLAlchemy
- **Validación de datos** con Pydantic
- **Documentación automática** con Swagger UI
- **CORS habilitado** para frontend
- **Arquitectura modular** y escalable

## 📋 Requisitos Previos

- Python 3.9 o superior
- MySQL Server
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

1. **Clona el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd chapiritas-reload
   ```

2. **Crea un entorno virtual**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # En Windows
   # source venv/bin/activate  # En Linux/Mac
   ```

3. **Instala las dependencias**
   ```bash
   pip install fastapi uvicorn sqlmodel mysql-connector-python python-dotenv bcrypt python-jose[cryptography] python-multipart jinja2
   ```

4. **Configura las variables de entorno**
   
   Crea un archivo `.env` en la raíz del proyecto:
   ```env
   DATABASE_USER=tu_usuario_mysql
   DATABASE_HOST=localhost
   DATABASE_PASSWORD=tu_contraseña_mysql
   DATABASE_NAME=chapiritas_db
   SECRET_KEY=tu_clave_secreta_jwt
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   
   # Configuración de email (opcional para verificación)
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=tu_email@gmail.com
   SMTP_PASSWORD=tu_contraseña_app
   ```

5. **Crea la base de datos**
   ```sql
   CREATE DATABASE chapiritas_db;
   ```

## 🚀 Ejecución

1. **Inicia el servidor de desarrollo**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Accede a la documentación**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

## 📁 Estructura del Proyecto

```
app/
├── __init__.py          # Inicialización del paquete
├── main.py              # Aplicación principal FastAPI
├── config.py            # Configuración y variables de entorno
├── database.py          # Configuración de base de datos
├── session.py           # Gestión de sesiones de BD
├── seeder.py            # Datos de prueba (seeders)
│
├── models/              # Modelos de base de datos (SQLModel)
│   ├── __init__.py
│   ├── base.py          # Modelo base
│   ├── user.py          # Modelo de usuario
│   ├── product.py       # Modelo de producto
│   ├── brand.py         # Modelo de marca
│   ├── category.py      # Modelo de categoría
│   ├── color.py         # Modelo de color
│   ├── gender.py        # Modelo de género
│   ├── material.py      # Modelo de material
│   ├── size.py          # Modelo de talla
│   └── image.py         # Modelo de imagen
│
├── routers/             # Rutas de la API
│   ├── __init__.py
│   ├── auth.py          # Autenticación y registro
│   ├── product.py       # Gestión de productos
│   └── user.py          # Gestión de usuarios
│
├── schemas/             # Esquemas Pydantic (serialización)
│   ├── __init__.py
│   ├── auth.py          # Esquemas de autenticación
│   ├── product.py       # Esquemas de producto
│   ├── user.py          # Esquemas de usuario
│   └── image.py         # Esquemas de imagen
│
├── utils/               # Utilidades
│   ├── __init__.py
│   ├── email.py         # Envío de emails
│   ├── hash.py          # Funciones de hash
│   ├── tokens.py        # Gestión de JWT
│   ├── user.py          # Utilidades de usuario
│   └── verifier.py      # Verificación de tokens
│
└── templates/           # Plantillas HTML
    └── email/
        └── verify_email.html
```

## 🔌 Endpoints Principales

### Autenticación
- `POST /auth/register` - Registro de usuario
- `POST /auth/login` - Inicio de sesión
- `GET /auth/verify-email` - Verificación de email

### Productos
- `GET /products/` - Listar productos
- `GET /products/filter` - Filtrar productos
- `POST /products/` - Crear producto
- `GET /products/{id}` - Obtener producto por ID
- `PUT /products/{id}` - Actualizar producto
- `DELETE /products/{id}` - Eliminar producto

### Usuarios
- `GET /users/me` - Perfil del usuario actual
- `PUT /users/me` - Actualizar perfil

## 🔍 Filtros de Productos

La API permite filtrar productos por:
- **Categorías** (IDs de categorías)
- **Géneros** (IDs de géneros)
- **Rango de precios** (mínimo y máximo)
- **Ordenamiento** (precio, nombre, fecha)

Ejemplo de uso:
```bash
GET /products/filter?categories=1,2&min_price=50&max_price=200&order_by=1
```

## 🏗️ Modelos de Datos

### Usuario (User)
- ID, nombre, email, contraseña
- Estado de verificación de email
- Timestamps de creación/actualización

### Producto (Product)
- Información básica (nombre, precio, cantidad, descripción)
- Relaciones con marca, categoría, usuario
- Múltiples imágenes, colores, materiales, tallas, géneros

### Entidades Relacionadas
- **Brand**: Marcas de productos
- **Category**: Categorías de productos
- **Color**: Colores disponibles
- **Gender**: Géneros (masculino, femenino, unisex)
- **Material**: Materiales de fabricación
- **Size**: Tallas disponibles
- **Image**: Imágenes de productos

## 🔐 Seguridad

- **Autenticación JWT** con tokens de acceso
- **Hash de contraseñas** con bcrypt
- **Verificación de email** obligatoria
- **CORS configurado** para desarrollo
- **Validación de datos** en todos los endpoints

## 🚀 Despliegue

### Usando Docker (Recomendado)

1. **Crea un Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   
   COPY requirements.txt .
   RUN pip install -r requirements.txt
   
   COPY . .
   
   EXPOSE 8000
   
   CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Construye y ejecuta**
   ```bash
   docker build -t chapiritas-api .
   docker run -p 8000:8000 --env-file .env chapiritas-api
   ```

### Usando un servidor

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## 🧪 Testing

Para ejecutar pruebas (cuando estén disponibles):
```bash
pytest
```

## 📝 Variables de Entorno

| Variable | Descripción | Requerido |
|----------|-------------|-----------|
| `DATABASE_USER` | Usuario de MySQL | ✅ |
| `DATABASE_HOST` | Host de MySQL | ✅ |
| `DATABASE_PASSWORD` | Contraseña de MySQL | ✅ |
| `DATABASE_NAME` | Nombre de la base de datos | ✅ |
| `SECRET_KEY` | Clave secreta para JWT | ✅ |
| `ALGORITHM` | Algoritmo de JWT (HS256) | ❌ |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Expiración del token (30) | ❌ |
| `SMTP_SERVER` | Servidor SMTP para emails | ❌ |
| `SMTP_PORT` | Puerto SMTP (587) | ❌ |
| `SMTP_USER` | Usuario SMTP | ❌ |
| `SMTP_PASSWORD` | Contraseña SMTP | ❌ |

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto

Para preguntas o sugerencias, puedes contactar al desarrollador.

---

**¡Gracias por usar Chapiritas Reload API! 👟✨**
