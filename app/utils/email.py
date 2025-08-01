# app/utils/email.py
import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader
from typing import Optional

from app.config import (
    MAIL_SERVICE, MAILGUN_API_KEY, MAILGUN_DOMAIN, MAILGUN_BASE_URL,
    SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD,
    MAIL_FROM_EMAIL, MAIL_FROM_NAME
)

# Configurar Jinja2 para plantillas
template_env = Environment(
    loader=FileSystemLoader("app/templates/email")
)

class EmailService:
    """Servicio de email que soporta Mailgun API y SMTP"""
    
    @staticmethod
    async def send_mailgun_email(
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ):
        """Enviar email usando Mailgun API"""
        if not all([MAILGUN_API_KEY, MAILGUN_DOMAIN]):
            raise ValueError("Mailgun API Key y Domain son requeridos")
        
        url = f"{MAILGUN_BASE_URL}/{MAILGUN_DOMAIN}/messages"
        
        data = {
            "from": f"{MAIL_FROM_NAME} <{MAIL_FROM_EMAIL}>",
            "to": to_email,
            "subject": subject,
            "html": html_content
        }
        
        if text_content:
            data["text"] = text_content
        
        response = requests.post(
            url,
            auth=("api", MAILGUN_API_KEY),
            data=data
        )
        
        if response.status_code != 200:
            raise Exception(f"Error enviando email: {response.text}")
        
        return response.json()
    
    @staticmethod
    async def send_smtp_email(
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ):
        """Enviar email usando SMTP"""
        if not all([SMTP_SERVER, SMTP_USER, SMTP_PASSWORD]):
            raise ValueError("Configuración SMTP incompleta")
        
        # Crear mensaje
        msg = MIMEMultipart('alternative')
        msg['From'] = f"{MAIL_FROM_NAME} <{MAIL_FROM_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        
        # Agregar contenido de texto plano si existe
        if text_content:
            part1 = MIMEText(text_content, 'plain', 'utf-8')
            msg.attach(part1)
        
        # Agregar contenido HTML
        part2 = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(part2)
        
        # Enviar email
        try:
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            server.quit()
        except Exception as e:
            raise Exception(f"Error enviando email SMTP: {str(e)}")
    
    @staticmethod
    async def send_email(
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ):
        """Enviar email usando el servicio configurado"""
        if MAIL_SERVICE == "mailgun":
            return await EmailService.send_mailgun_email(
                to_email, subject, html_content, text_content
            )
        else:
            return await EmailService.send_smtp_email(
                to_email, subject, html_content, text_content
            )

# Funciones de compatibilidad con el código existente
async def send_simple_email(email: str):
    """Enviar email simple de bienvenida"""
    subject = "Bienvenido a Chacharitas"
    html_content = """
    <html>
        <body>
            <h1>¡Bienvenido a Chacharitas!</h1>
            <p>Gracias por registrarte en nuestra plataforma.</p>
        </body>
    </html>
    """
    text_content = "¡Bienvenido a Chacharitas! Gracias por registrarte en nuestra plataforma."
    
    return await EmailService.send_email(email, subject, html_content, text_content)

async def send_verification_email(
    email: str,
    verify_url: str,
    resend_url: str
):
    """Enviar email de verificación usando template"""
    try:
        # Cargar template
        template = template_env.get_template("verify_email.html")
        
        # Datos para el template
        now = __import__("datetime").datetime.utcnow()
        template_data = {
            "verify_url": verify_url,
            "resend_url": resend_url,
            "year": now.year
        }
        
        # Renderizar HTML
        html_content = template.render(**template_data)
        
        # Contenido de texto plano como fallback
        text_content = f"""
        Verifica tu correo en Chacharitas
        
        Para verificar tu cuenta, haz clic en el siguiente enlace:
        {verify_url}
        
        Si no puedes hacer clic en el enlace, cópialo y pégalo en tu navegador.
        
        Si no solicitaste esta verificación, puedes ignorar este correo.
        
        © {now.year} Chacharitas
        """
        
        subject = "Verifica tu correo en Chacharitas"
        
        return await EmailService.send_email(email, subject, html_content, text_content)
    
    except Exception as e:
        print(f"Error enviando email de verificación: {str(e)}")
        raise e