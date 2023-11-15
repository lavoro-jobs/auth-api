import os

from fastapi_mail import FastMail, MessageSchema, MessageType, ConnectionConfig

connection_config = ConnectionConfig(
    MAIL_USERNAME="lavoro.projektr@gmail.com",
    MAIL_PASSWORD=os.environ.get("EMAIL_PASSWORD"),
    MAIL_FROM="lavoro.projektr@gmail.com",
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_FROM_NAME="Lavoro",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
)


async def send_confirmation_email(email, token):
    message_html = f"""
    <html>
        <body>
            <h1>Confirm your email</h1>
            <p>Please confirm your email by clicking on the link: <a href="http://localhost:3000/confirm-email/{token}">http://localhost:3000/confirm-email/{token}</a></p>
        </body>
    </html>
    """

    message = MessageSchema(
        subject="Lavoro - Confirm your email", recipients=[email], body=message_html, subtype=MessageType.html
    )

    fm = FastMail(connection_config)
    await fm.send_message(message)
    return True
