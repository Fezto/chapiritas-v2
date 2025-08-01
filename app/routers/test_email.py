# app/routers/test_email.py
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from app.utils.email import send_simple_email, send_verification_email, EmailService

router = APIRouter(prefix="/test", tags=["testing"])

class EmailTest(BaseModel):
    email: EmailStr
    subject: str = "Email de prueba desde Chacharitas API"
    message: str = "Este es un email de prueba enviado desde la API de FastAPI"

@router.post("/send-simple-email")
async def test_simple_email(email: EmailStr):
    """Probar envío de email simple"""
    try:
        result = await send_simple_email(email)
        return {
            "success": True,
            "message": f"Email de bienvenida enviado a {email}",
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error enviando email: {str(e)}"
        )

@router.post("/send-verification-email")
async def test_verification_email(email: EmailStr):
    """Probar envío de email de verificación"""
    try:
        verify_url = f"https://tu-app.com/verify?email={email}&token=test-token-123"
        resend_url = f"https://tu-app.com/resend?email={email}"
        
        result = await send_verification_email(email, verify_url, resend_url)
        return {
            "success": True,
            "message": f"Email de verificación enviado a {email}",
            "verify_url": verify_url,
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error enviando email de verificación: {str(e)}"
        )

@router.post("/send-custom-email")
async def test_custom_email(email_data: EmailTest):
    """Probar envío de email personalizado"""
    try:
        html_content = f"""
        <html>
            <body>
                <h2>{email_data.subject}</h2>
                <p>{email_data.message}</p>
                <hr>
                <p><small>Enviado desde Chacharitas API - FastAPI</small></p>
            </body>
        </html>
        """
        
        text_content = f"{email_data.subject}\n\n{email_data.message}\n\n---\nEnviado desde Chacharitas API - FastAPI"
        
        result = await EmailService.send_email(
            to_email=email_data.email,
            subject=email_data.subject,
            html_content=html_content,
            text_content=text_content
        )
        
        return {
            "success": True,
            "message": f"Email personalizado enviado a {email_data.email}",
            "subject": email_data.subject,
            "result": result
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error enviando email personalizado: {str(e)}"
        )

@router.get("/email-config")
async def get_email_config():
    """Obtener configuración actual de email (sin credenciales sensibles)"""
    from app.config import (
        MAIL_SERVICE, MAILGUN_DOMAIN, MAILGUN_BASE_URL,
        SMTP_SERVER, SMTP_PORT, MAIL_FROM_EMAIL, MAIL_FROM_NAME
    )
    
    config = {
        "mail_service": MAIL_SERVICE,
        "mail_from_email": MAIL_FROM_EMAIL,
        "mail_from_name": MAIL_FROM_NAME,
    }
    
    if MAIL_SERVICE == "mailgun":
        config.update({
            "mailgun_domain": MAILGUN_DOMAIN,
            "mailgun_base_url": MAILGUN_BASE_URL,
            "mailgun_api_key_configured": bool(MAILGUN_DOMAIN and len(str(MAILGUN_DOMAIN)) > 0)
        })
    else:
        config.update({
            "smtp_server": SMTP_SERVER,
            "smtp_port": SMTP_PORT,
            "smtp_configured": bool(SMTP_SERVER and SMTP_PORT)
        })
    
    return config
