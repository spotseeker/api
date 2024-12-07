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
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OTP Verification</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 50px auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    padding: 10px 0;
                    border-bottom: 1px solid #dddddd;
                }}
                .header h1 {{
                    margin: 0;
                    color: #FB9062;
                }}
                .content {{
                    padding: 20px;
                }}
                .content p {{
                    font-size: 16px;
                    color: #333333;
                }}
                .otp-code {{
                    display: inline-block;
                    padding: 10px 20px;
                    font-size: 24px;
                    font-weight: bold;
                    color: #ffffff;
                    background-color: #6A0D83; /* Default color, change as needed */
                    border-radius: 4px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    padding: 10px 0;
                    border-top: 1px solid #dddddd;
                    font-size: 12px;
                    color: #777777;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>SpotSeeker</h1>
                </div>
                <div class="content">
                    <p>Hola {user.first_name},</p>
                    <p>
                        Para completar tu registro en SpotSeeker,
                        por favor ingresa el siguiente código:
                    </p>
                    <div class="otp-code">{otp}</div>
                    <p>Si no solicitaste este código, por favor ignora este correo.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 SpotSeeker. Todos los derechos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        self.__send_email(user.email, subject, message)

    def send_password_reset_otp(self, user: User, otp: str) -> None:
        subject = "Recupera tu contraseña en SpotSeeker"
        message = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OTP Verification</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                }}
                .container {{
                    max-width: 600px;
                    margin: 50px auto;
                    background-color: #ffffff;
                    padding: 20px;
                    border-radius: 8px;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                .header {{
                    text-align: center;
                    padding: 10px 0;
                    border-bottom: 1px solid #dddddd;
                }}
                .header h1 {{
                    margin: 0;
                    color: #FB9062;
                }}
                .content {{
                    padding: 20px;
                }}
                .content p {{
                    font-size: 16px;
                    color: #333333;
                }}
                .otp-code {{
                    display: inline-block;
                    padding: 10px 20px;
                    font-size: 24px;
                    font-weight: bold;
                    color: #ffffff;
                    background-color: #6A0D83; /* Default color, change as needed */
                    border-radius: 4px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    padding: 10px 0;
                    border-top: 1px solid #dddddd;
                    font-size: 12px;
                    color: #777777;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>SpotSeeker</h1>
                </div>
                <div class="content">
                    <p>Hola {user.first_name},</p>
                    <p>
                        Para recuperar tu contraseña en SpotSeeker,
                        por favor ingresa el siguiente código:
                    </p>
                    <div class="otp-code">{otp}</div>
                    <p>Si no solicitaste este código, por favor ignora este correo.</p>
                </div>
                <div class="footer">
                    <p>&copy; 2024 SpotSeeker. Todos los derechos reservados.</p>
                </div>
            </div>
        </body>
        </html>
        """
        self.__send_email(user.email, subject, message)
