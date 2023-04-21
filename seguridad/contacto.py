from flask import session, request
from db.database import *
from typing import Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Contacto:
    def __init__(self, correo="", nombre="", numero="", asunto="", mensaje="") -> None:
        self.correo = correo
        self.nombre = nombre
        self.numero = numero
        self.asunto = asunto
        self.mensaje = mensaje
        self.tipo_usuario = session.get('tipo_usuario')
        self.id_usuario = session.get('id')

    def enviar_correos(self) -> bool:
        # Ejemplo para Gmail, cambiar si se usa otro proveedor
        smtp_server = "smtp.gmail.com"
        smtp_port = 587  # Puerto para TLS
        # Tu dirección de correo electrónico
        smtp_username = 'serviciossbarranquilla@gmail.com'
        smtp_password = 'kdsmhsnwqacecycn'  # Tu contraseña

        # Crear una conexión segura al servidor SMTP
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)

        # La dirección de correo electrónico del destinatario
        to_email = "serviciossbarranquilla@gmail.com"
        from_email = self.correo  # Tu dirección de correo electrónico
        subject = self.asunto  # Asunto del correo

        # Crear el mensaje MIME
        message = MIMEMultipart()
        message['From'] = from_email
        message['To'] = to_email
        message['Subject'] = subject

        # Cuerpo del mensaje
        body = """
        <!DOCTYPE html>
        <html>
        <head>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
        <meta charset="utf-8">
        <title>Correo de ejemplo</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f8f8f8;
                }}
                
                .container {{
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                    background-color: #ffffff;
                    border-radius: 5px;
                }}
                
                h1 {{
                    color: #333333;
                }}
                
                p {{
                    color: #777777;
                }}
                
                strong {{
                    color: #000000;
                }}
                
                .logo {{
                    width: 150px;
                    height: auto;
                    margin-bottom: 20px;
                }}
                
                .button {{
                    display: inline-block;
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: #ffffff;
                    text-decoration: none;
                    border-radius: 5px;
                }}
                
                .button:hover {{
                    background-color: #0056b3;
                }}
            </style>

        </head>
        <body>

        <div class="container">
        <div class="d-flex justify-content-center">
                <img class="rounded-circle" src="https://us.123rf.com/450wm/zukiuki/zukiuki1805/zukiuki180502147/101758354-dise%C3%B1o-de-ilustraci%C3%B3n-del-s%C3%ADmbolo-de-llave-inglesa-de-logotipo-empresarial-icono-de-casa-y.jpg?ver=6"  alt="Generic placeholder image"
                    width="140" height="140">
        </div>     
            <h1>Asunto: {asunto}</h1>
            <p> <strong>Mensaje:</strong>{mensaje}</p>
            <h3>Datos personales</h3>
            <p><strong>Enviado por :</strong>{nombre}</p>
            <p><strong>Correo enviado por:</strong> {correo}</p>
            <p><strong>celular:</strong> {numero}</p>
        </div>
        <footer class="container">
            <p class="float-right">{tipo}</p>
            <p>&copy; 2023 GESTIÓN DE SERVICIOS (ALBAÑIL, PLOMERO, CARPINTERO) ; <a href="https://www.minambiente.gov.co/politica-de-proteccion-de-datos-personales/">Privacy</a></p>
        </footer>
        </body>
        </html>

        """.format(asunto=self.asunto, mensaje=self.mensaje, nombre=self.nombre,
                   correo=self.correo, numero=self.numero, tipo=self.tipo_usuario)

        # Adjuntar el cuerpo del correo como parte HTML al mensaje MIME
        message.attach(MIMEText(body, 'html'))

        # Convertir el mensaje MIME a una cadena de caracteres
        message_str = message.as_string()

        # Enviar el correo electrónico
        server.sendmail(from_addr=from_email,
                        to_addrs=to_email, msg=message_str)

        # Cerrar la conexión con el servidor SMTP
        server.quit()

        return True

    def informacion_usuario_contacto(self) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
            SELECT udp.nombre_completo nombre,u.email correo,udp.numero_celular celular
                FROM usuarios u 
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                WHERE u.id=%s
        """
        cursor.execute(query, (self.id_usuario,))
        return cursor.fetchone()

    def validacion_contacto(self) -> bool:
        json = request.get_json()
        usuario = self.informacion_usuario_contacto()

        if 'nombre' not in json or 'correo' not in json or 'numero' not in json:
            return False

        if usuario['nombre'] != json['nombre'] or usuario['correo'] != json['correo'] or int(usuario['celular']) != int(json['numero']):
            return True

        return False


class ValidacionDatosContacto(Exception):
    ...
