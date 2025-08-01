from os import getenv
from dotenv import load_dotenv

load_dotenv()

# Configuración de base de datos
DATABASE_USER=getenv("DATABASE_USER")
DATABASE_HOST=getenv("DATABASE_HOST")
DATABASE_PASSWORD=getenv("DATABASE_PASSWORD")
DATABASE_NAME=getenv("DATABASE_NAME")

# Configuración de la base de datos
DATABASE_URL = f"mysql+mysqlconnector://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:3306/{DATABASE_NAME}"

# Configuración de JWT
SECRET_KEY = getenv("SECRET_KEY", "your-secret-key-here")
ALGORITHM = getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

# Configuración de email
MAIL_SERVICE = getenv("MAIL_SERVICE", "smtp")  # "mailgun" or "smtp"

# Configuración de Mailgun
MAILGUN_API_KEY = getenv("MAILGUN_API_KEY")
MAILGUN_DOMAIN = getenv("MAILGUN_DOMAIN")
MAILGUN_BASE_URL = getenv("MAILGUN_BASE_URL", "https://api.mailgun.net/v3")

# Configuración SMTP (alternativa)
SMTP_SERVER = getenv("SMTP_SERVER")
SMTP_PORT = int(getenv("SMTP_PORT", "587"))
SMTP_USER = getenv("SMTP_USER")
SMTP_PASSWORD = getenv("SMTP_PASSWORD")

# Configuración de remitente
MAIL_FROM_EMAIL = getenv("MAIL_FROM_EMAIL", "noreply@chacharitas.com")
MAIL_FROM_NAME = getenv("MAIL_FROM_NAME", "Chacharitas")