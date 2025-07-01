# app/utils/email.py
import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig

conf = ConnectionConfig(
    MAIL_USERNAME   = os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD   = os.getenv("MAIL_PASSWORD"),
    MAIL_FROM       = os.getenv("MAIL_FROM_ADDRESS"),
    MAIL_PORT       = int(os.getenv("MAIL_PORT", 587)),
    MAIL_SERVER     = os.getenv("MAIL_HOST"),
    USE_CREDENTIALS = True,
    MAIL_FROM_NAME  = os.getenv("MAIL_FROM_NAME", "Chacharitas"),
    MAIL_STARTTLS   = True,   # porque usas TLS sobre el puerto 587
    MAIL_SSL_TLS    = False,  # no SSL directo
    TEMPLATE_FOLDER="app/templates/email",  # aquí le indicas dónde están tus jinja templates
)

fm = FastMail(conf)

async def send_simple_email(email: str):
    message = MessageSchema(
        subject="Bienvenido a Chacharitas",
        recipients=[email],
        body="hola",
        subtype="plain",
    )
    await fm.send_message(message)

async def send_verification_email(
    email: str,
    verify_url: str,
    resend_url: str
):
    now = __import__("datetime").datetime.utcnow()
    message = MessageSchema(
        subject="Verifica tu correo en Chacharitas",
        recipients=[email],
        template_body={
            "verify_url": verify_url,
            "resend_url": resend_url,
            "year": now.year
        },
        subtype="html",
    )
    await fm.send_message(message, template_name="verify_email.html")