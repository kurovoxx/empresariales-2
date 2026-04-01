import smtplib
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

def send_email_with_pdf(to_emails, subject, body, attachment_path):
    """
    Envía un correo con un archivo PDF adjunto.
    to_emails: lista de strings ['email1@test.com', 'email2@test.com']
    """
    if not to_emails:
        print("No hay destinatarios para este grupo.")
        return False

    # Configuración desde el .env
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    email_user = os.getenv("EMAIL_USER")
    email_pass = os.getenv("EMAIL_PASS")

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = email_user
    msg['To'] = ", ".join(to_emails)
    msg.set_content(body)

    # Adjuntar el PDF
    with open(attachment_path, 'rb') as f:
        file_data = f.read()
        file_name = os.path.basename(attachment_path)
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=file_name)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()  # Conexión segura
            server.login(email_user, email_pass)
            server.send_message(msg)
        print(f"✓ Correo enviado exitosamente a {len(to_emails)} personas.")
        return True
    except Exception as e:
        print(f"⚠ Error al enviar correo: {e}")
        raise e
