# 📧 Configuración de Mailgun para Chacharitas API

Esta guía te ayudará a configurar Mailgun en tu API de FastAPI usando las mismas credenciales que tu aplicación Laravel.

## 🔧 Configuración

### 1. Variables de Entorno para Mailgun API

Basándote en tu configuración Laravel existente, agrega estas variables a tu archivo `.env`:

```env
# Configuración de Email - Mailgun API (RECOMENDADO)
MAIL_SERVICE=mailgun
MAILGUN_API_KEY=tu_mailgun_api_key_aqui
MAILGUN_DOMAIN=tu_dominio.mailgun.org
MAILGUN_BASE_URL=https://api.mailgun.net/v3
MAIL_FROM_EMAIL=noreply@tu_dominio.com  
MAIL_FROM_NAME=Chacharitas
```

### 2. Variables de Entorno para SMTP (Alternativa)

Si prefieres usar SMTP en lugar de la API:

```env
# Configuración de Email - SMTP
MAIL_SERVICE=smtp
SMTP_SERVER=smtp.mailgun.org
SMTP_PORT=587
SMTP_USER=tu_usuario_smtp_aqui
SMTP_PASSWORD=tu_contraseña_smtp_aqui
MAIL_FROM_EMAIL=noreply@tu_dominio.com
MAIL_FROM_NAME=Chacharitas
```

## 🚀 Uso

### Enviar Email Simple

```python
from app.utils.email import send_simple_email

await send_simple_email("usuario@example.com")
```

### Enviar Email de Verificación

```python
from app.utils.email import send_verification_email

await send_verification_email(
    email="usuario@example.com",
    verify_url="https://tu-app.com/verify?token=abc123",
    resend_url="https://tu-app.com/resend-verification"
)
```

### Usar el Servicio Directamente

```python
from app.utils.email import EmailService

# Con Mailgun API
await EmailService.send_email(
    to_email="usuario@example.com",
    subject="Asunto del mensaje",
    html_content="<h1>Contenido HTML</h1>",
    text_content="Contenido en texto plano"
)
```

## 🔄 Migración desde SMTP

Si actualmente estás usando SMTP y quieres cambiar a Mailgun API:

1. **Cambia la variable de entorno:**

   ```env
   MAIL_SERVICE=mailgun  # Cambiar de "smtp" a "mailgun"
   ```

2. **El código no necesita cambios** - la función `send_verification_email()` funcionará automáticamente con Mailgun API.

## ✅ Ventajas de Mailgun API vs SMTP

### Mailgun API:

- ✅ Más rápido y confiable
- ✅ Mejor entregabilidad
- ✅ Tracking de emails (abiertos, clicks, bounces)
- ✅ No bloquea el hilo de ejecución
- ✅ Manejo automático de errores
- ✅ Webhooks para eventos

### SMTP:

- ✅ Más universal
- ✅ Funciona con cualquier proveedor SMTP
- ❌ Más lento
- ❌ Puede bloquear la aplicación

## 🧪 Pruebas

### Probar la Configuración

Crea un endpoint temporal para probar:

```python
# En algún router
@router.post("/test-email")
async def test_email():
    try:
        await send_simple_email("tu-email@example.com")
        return {"message": "Email enviado correctamente"}
    except Exception as e:
        return {"error": str(e)}
```

### Verificar en Mailgun Dashboard

1. Ve a tu dashboard de Mailgun
2. Revisa la sección "Logs"
3. Deberías ver los emails enviados desde tu API

## 🔍 Troubleshooting

### Error: "Mailgun API Key y Domain son requeridos"

- Verifica que `MAILGUN_API_KEY` y `MAILGUN_DOMAIN` estén configurados en tu `.env`
- Asegúrate de que el archivo `.env` esté en la raíz del proyecto

### Error: "Error enviando email: Forbidden"

- Verifica que tu API Key sea correcta
- Confirma que el dominio esté autorizado en Mailgun
- Revisa que no hayas excedido los límites de tu plan

### Error: "Domain not found"

- Verifica que `MAILGUN_DOMAIN` sea tu dominio correcto de Mailgun
- Confirma que el dominio esté verificado en Mailgun

## 🔄 Sincronización con Laravel

Para mantener consistencia entre tu aplicación Laravel y la API FastAPI:

1. **Usa las mismas credenciales** en ambas aplicaciones
2. **Mantén el mismo remitente** (`MAIL_FROM_EMAIL`)
3. **Usa templates similares** para una experiencia consistente
4. **Configura webhooks** en Mailgun para ambas aplicaciones si es necesario

## 📝 Logs y Monitoreo

Para ver logs de emails en producción:

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# En tu servicio de email
logger.info(f"Enviando email a {to_email} con asunto: {subject}")
```

---

¡Con esta configuración tu API FastAPI enviará emails usando la misma infraestructura que tu aplicación Laravel! 🚀
