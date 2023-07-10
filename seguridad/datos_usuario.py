from db.database import *
from flask import session
from typing import Dict
import datetime
import re
from psycopg2 import extras


class DatosUsuario:
    def __init__(self, email_actual="", email_nuevo="", verificacion_email="",
                 observaciones="", estrellas="", id_solicitud="", tipo_usuario_calificar="") -> None:
        self.email_actual = email_actual
        self.email_nuevo = email_nuevo
        self.verificacion_email = verificacion_email
        self.observaciones = observaciones
        self.estrellas = estrellas
        self.id_solicitud = id_solicitud
        self.tipo_usuario_calificar = tipo_usuario_calificar
        self.id_usuario = session.get('id')
        self.tipo_usuario = session.get('tipo_usuario')

    def validar_correo_electronico(self):
        # Expresión regular para validar correos electrónicos
        patron = r'^(?=.{1,256})(?=.{1,64}@.{1,255}$)(?=.{1,255}$)((?!@)[\w&\'*+._%-]+(?:(?!@)[\w&\'*+._%-]|){0,63}(?<!@)@)+(?:(?!@)[\w&\'*+._%-]+(?:(?!@)[\w&\'*+._%-]|){0,63}(?<!@)\.)+(?:(?!@)[a-zA-Z]{2,63}(?:(?!@)[a-zA-Z]{2,63}|))$'
        if re.match(patron, self.email_nuevo):
            return True
        else:
            return False

    def informacion_usuario(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
            SELECT udp.nombre_completo nombre, udp.numero_documento documento, udp.direccion, udp.numero_celular celular
                FROM usuarios u 
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                WHERE u.email=%s
        """
        cursor.execute(query, (self.verificacion_email,))
        return cursor.fetchone()

    def actualizar_email(self) -> bool:
        cursor = db.connection.cursor()
        actualizacion_email = (self.email_nuevo, self.email_actual)
        query = 'UPDATE usuarios SET email = %s WHERE email = %s'
        cursor.execute(query, actualizacion_email)
        db.connection.commit()
        cursor.close()
        return True

    def datos_unico_correo(self) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = "SELECT id FROM usuarios WHERE email=%s"
        cursor.execute(query, (self.email_nuevo,))
        return cursor.fetchone()

    def existe_correo(self) -> bool:
        dato_unico = self.datos_unico_correo()
        if dato_unico is None:
            return False

        if dato_unico:
            return True

        else:
            return True

    def ocupaciones(self):
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = "SELECT id,nombre ocupacion FROM ocupacion o"
        cursor.execute(query)
        return cursor.fetchall()

    def obtener(self) -> Dict:
        # Obtener el cursor y el correo electrónico actual
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        # Consultar los datos del usuario con sus ocupaciones
        # Este query es para obtener los contratistas
        query = """ 
        SELECT udp.nombre_completo, MAX(udp.numero_celular) as numero_celular, MAX(udp.numero_documento) as numero_documento,
            MAX(udp.direccion) as direccion, STRING_AGG(o.nombre, ', ') as ocupaciones, MAX(udp.descripcion) as descripcion,
            MAX(o.id) as id_ocupacion
                FROM usuario_datos_personales udp
                INNER JOIN usuarios u ON u.id_usuario_datos_personales = udp.id
                INNER JOIN usuario_ocupaciones uo ON uo.id_usuario = u.id
                INNER JOIN ocupacion o ON uo.id_ocupacion = o.id
                WHERE u.id = %s AND uo.eliminado = 0
                GROUP BY udp.nombre_completo
    """
        cursor.execute(query, (self.id_usuario,))
        datos = cursor.fetchone()

        # Si los datos no se encuentran, consultar solo los datos básicos del usuario, es decir para obtener los datos del usuario cliente
        if datos is None:
            query_ = """
            SELECT udp.nombre_completo,udp.numero_celular, udp.numero_documento, udp.direccion,udp.descripcion
            FROM usuario_datos_personales udp
            INNER JOIN usuarios u ON u.id_usuario_datos_personales = udp.id
            WHERE u.id = %s
            """
            cursor.execute(query_, (self.id_usuario,))
            datos = cursor.fetchone()
            datos['ocupaciones'] = None

        return datos

    def validar_campos_vacios(self) -> bool:
        dato = self.obtener()
        if any(valor == '' or valor == 0 or valor is None for valor in [dato['direccion'], dato['ocupaciones'], dato['descripcion'], dato['numero_celular']]) and self.tipo_usuario == 'Contratista':
            return True

        if any(valor == '' or valor == 0 for valor in [dato['direccion'], dato['numero_celular']]) and self.tipo_usuario == 'Cliente':
            return True

        else:
            return False

    def actualizar(self, nombre, celular, direccion, descripcion, id_usuario):
        cursor = db.connection.cursor()
        datos_actualizar = (nombre, celular, direccion,
                            descripcion, id_usuario)
        query = 'UPDATE usuario_datos_personales SET nombre_completo = %s, numero_celular = %s, direccion=%s,descripcion=%s WHERE id = %s'
        cursor.execute(query, datos_actualizar)
        db.connection.commit()
        cursor.close()
        return None

    def id_usuarios(self, id) -> Dict:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """
            SELECT id_usuario_contratista,id_usuario_cliente
            FROM solicitud
            WHERE id=%s
        """
        cursor.execute(query, (id,))
        return cursor.fetchone()

    def calificar(self) -> bool:
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)

        query_validacion = """
        SELECT count(u.id) cantidad
            FROM calificacion c
            INNER JOIN usuarios u ON c.id_usuario=u.id
            INNER JOIN tipo_usuario tu ON u.id_tipo_usuario = tu.id
            WHERE c.id_solicitud=%s and tu.id=%s
        
        """
        valores = (self.id_solicitud, self.tipo_usuario_calificar)

        cursor.execute(query_validacion, valores)

        calificacion = cursor.fetchone()['cantidad']

        if calificacion == 0:
            fecha_actual = datetime.datetime.now()

            cadena_fecha = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")
            print(self.id_usuario)

            informacion = (self.observaciones, self.estrellas,
                           self.id_solicitud, self.id_usuario, cadena_fecha)

            query_informacion = """
                    INSERT INTO calificacion (observaciones,id_numero_estrellas,id_solicitud,id_usuario,registro)
                    VALUES (%s,%s,%s,%s,%s)
                """

            cursor.execute(query_informacion, informacion)
            db.connection.commit()
            return True

        elif calificacion == 1:
            return False

    def ocupaciones_contratista(self, id):
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """select us.id_ocupacion as id
                    from usuarios u 
                    join usuario_ocupaciones us on u.id = us.id_usuario
                    where u.id = %s and us.eliminado = 0"""
        cursor.execute(query, (id,))
        return cursor.fetchall()

    def ocupaciones_eliminadas(self, id):
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """select us.id_ocupacion as id
                    from usuarios u 
                    join usuario_ocupaciones us on u.id = us.id_usuario
                    where u.id = %s and us.eliminado = 1"""
        cursor.execute(query, (id,))
        return cursor.fetchall()

    def agregar_ocupaciones(self, data):
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query_informacion = """
                    INSERT INTO usuario_ocupaciones (id_usuario,id_ocupacion)
                    VALUES """ + data + ";"
        cursor.execute(query_informacion)
        db.connection.commit()
        return True

    def eliminar_ocupaciones(self, id, data):
        cursor = db.connection.cursor()
        query_informacion = """
                    UPDATE usuario_ocupaciones set eliminado = 1 
                    where id_usuario = """ + str(id) + " and id_ocupacion in ("+data+");"

        cursor.execute(query_informacion)
        db.connection.commit()
        return True

    def actualizar_ocupaciones(self, id, data):
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query_informacion = """
                    UPDATE usuario_ocupaciones set eliminado = 0 
                    where id_usuario = """ + str(id) + " and id_ocupacion in ("+data+");"

        cursor.execute(query_informacion)
        db.connection.commit()
        return True

    def informacion_contratistas(self):
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """  SELECT u.id, u.email as email, MAX(us.nombre_completo) as nombre_completo, MAX(us.numero_celular) as celular, STRING_AGG(o.nombre, ', ') AS ocupaciones
                        FROM usuarios u
                        JOIN usuario_datos_personales us ON u.id_usuario_datos_personales = us.id
                        JOIN usuario_ocupaciones uc ON uc.id_usuario = u.id
                        JOIN ocupacion o ON uc.id_ocupacion = o.id
                        WHERE u.id_tipo_usuario = 2 AND uc.eliminado = 0
                        GROUP BY u.id, u.email
                        ORDER BY MAX(us.nombre_completo), MAX(o.nombre);"""
        cursor.execute(query)
        return cursor.fetchall()

    def eventos_contratistas(self, id):
        cursor = db.connection.cursor(cursor_factory=extras.RealDictCursor)
        query = """ SELECT s.id, s.descripcion, s.horario || 'T' || s.hora as fecha,
           CASE
               WHEN s.id_estado = 1 THEN '#3346FF'
               WHEN s.id_estado = 2 THEN '#0cde00'
               WHEN s.id_estado = 3 THEN '#FFF033'
               ELSE '#E20202'
           END as color
            FROM solicitud s
            WHERE s.id_usuario_contratista = %s;"""
        cursor.execute(query, (id,))
        return cursor.fetchall()


class DatoUnicoEmail(Exception):
    ...


class CorreoInvalido(Exception):
    ...
