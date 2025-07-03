# 👟 Chapiritas Reload

Una API REST moderna y robusta para e-commerce de calzado, desarrollada con FastAPI y SQLModel. Esta aplicación
proporciona todas las funcionalidades necesarias para gestionar un catálogo de productos, usuarios, autenticación y más.

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

- Python 3.12 o superior
- MySQL Server
- pip (gestor de paquetes de Python)

## 🛠️ Instalación

### I. ¿Chacharitas Web funciona?

**Asegurate** de tener la versión web (Laravel) de chacharitas corriendo correctamente, ya que la base de datos con la que interactúa esta API **se crea a partir de las migraciones de Laravel**
 
1. Verifica que la base de datos que utiliza la página existe dentro de tu Sistema Gestor de Base de Datos local (como Workbench)
   ```sql
   USE chacharitas; -- El nombre de la base de datos puede variar
   ```
2. Si existe la base de datos, Ejecuta npm run dev para correr el servidor de pruebas de Vite
   ```bash
   npm run dev
   ```
2. Ejecuta php artisan serve para correr la página perse
    ```bash
    php artisan serve
    ```
   
3. Interactúa con la  página y verifica en general si funciona. En caso de que no, revisa la documentación de Chacharitas (Web) para ver paso a paso como instalar el programa y los posibles pitfalls en el proceso.

### II. Ejecutando la API

Para poder alimentar con la base de datos de Laravel a Chacharitas App se creó una API que le proporcione a la aplicación móvil toda la información que pudiese llegar a necesitar. Su instalación es la siguiente

1. Clona el repositorio
   ```bash
   git clone https://github.com/Fezto/chapiritas-v2.git
   ```
2. Genera un entorno virtual e instala todas las dependencias
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecuta la API
    ```bash
    fastapi run
    ```
4. Dentro de la raíz del proyecto, genera tu archivo .env y llena la siguiente información
    ```dotenv
    DATABASE_USER=root
    DATABASE_HOST=localhost
    DATABASE_PASSWORD='<Inserta tu contraseña de MySQL aquí>'
    DATABASE_NAME=chacharitas # Puede variar si colocaste otro nombre

    JWT_SECRET='<Coloca un string cualquiera aquí>'
    JWT_ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTE=15
    REFRESH_TOKEN_EXPIRE_DAYS=7

    MAIL_HOST=smtp.mailgun.org
    MAIL_PORT=587
    MAIL_USERNAME='<Cámbialo con lo que se te comparta'
    MAIL_PASSWORD='<Cámbialo con lo que se te comparta'
    MAIL_ENCRYPTION=tls
    MAIL_FROM_ADDRESS=postmaster@mail.chacharitas.org
    MAIL_FROM_NAME="Chacharitas"

    #API_URL=https://api.chacharitas.org
    API_URL=http://localhost:8000
    ```
5. Accede a la documentación
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
