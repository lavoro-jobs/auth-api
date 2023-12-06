from lavoro_library.email import send_email


async def send_confirmation_email(email, token):
    message_html = f"""
    <html>
        <body>
            <h1>Confirm your email</h1>
            <p>Please confirm your email by clicking on the link: <a href="http://localhost:3000/confirm-email/{token}">http://localhost:3000/confirm-email/{token}</a></p>
        </body>
    </html>
    """
    await send_email(email, "Lavoro - Confirm your email", message_html)
    return True
