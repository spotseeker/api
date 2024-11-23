import resend
from django.conf import settings

from spotseeker.user.models import User


class EmailHelper:
    def __init__(self) -> None:
        resend.api_key = settings.RESEND_APIKEY
        self.client = resend

    def __send_email(self, recipient: str, subject: str, message: str) -> None:
        params: self.client.Emails.SendParams = {
            "from": f"Andres de SpotSeeker <{settings.EMAIL_HOST_USER}>",
            "to": [recipient],
            "subject": subject,
            "html": message,
        }
        self.client.Emails.send(params)

    def send_onboarding_otp(self, user: User, otp: str) -> None:
        subject = "Valida tu correo en SpotSeeker"
        message = f"""
        <p>Hola {user.first_name},</p>
        <p>
            Para completar tu registro en SpotSeeker,
            por favor ingresa el siguiente código: <b>{otp}</b>
        </p>
        """
        self.__send_email(user.email, subject, message)

    def send_password_reset_otp(self, user: User, otp: str) -> None:
        subject = "Recupera tu contraseña en SpotSeeker"
        message = f"""
        <p>Hola {user.first_name},</p>
        <p>
            Para recuperar tu contraseña en SpotSeeker,
            por favor ingresa el siguiente código: <b>{otp}</b>
        </p>
        """
        self.__send_email(user.email, subject, message)
