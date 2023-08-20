from flask import session, request, render_template
from db.database import *
from typing import Dict
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from psycopg2 import extras

class Contacto:
    def __init__(self, correo="", nombre="", numero="", asunto="", mensaje="",tipo_usuario="",id_usuario:int=0) -> None:
        self.correo = correo
        self.nombre = nombre
        self.numero = numero
        self.asunto = asunto
        self.mensaje = mensaje
        self.servidor='smtp.gmail.com'
        self.contrasena='kdsmhsnwqacecycn'
        self.username='serviciossbarranquilla@gmail.com'
        self.puerto=587
        self.tipo_usuario = tipo_usuario
        self.id_usuario = id_usuario

    def enviar_correos(self) -> bool:
        # Ejemplo para Gmail, cambiar si se usa otro proveedor
        smtp_server = self.servidor
        smtp_port = self.puerto # Puerto para TLS
        smtp_username = self.username
        smtp_password = self.contrasena # Tu contraseña

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

        informacion = {
            'asunto': self.mensaje,
            'nombre': self.nombre,
            'correo': self.correo,
            'numero': self.numero,
            'tipo': self.tipo_usuario,
        }
        # Cuerpo del mensaje
        body = render_template("enviar_correos.html",informacion=informacion)
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
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
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

        if usuario['nombre'] != json['nombre'].lower() or usuario['correo'] != json['correo'] or int(usuario['celular']) != int(json['numero']):
            return True

        return False


class ValidacionDatosContacto(Exception):
    ...
