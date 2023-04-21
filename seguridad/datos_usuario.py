from db.database import *
from flask import session
from typing import Dict
import datetime
import re

<<<<<<< HEAD
=======

>>>>>>> ajustes_finales
class DatosUsuario:
    def __init__(self, email_actual="", email_nuevo="") -> None:
        self.email_actual = email_actual
        self.email_nuevo = email_nuevo
        self.id_usuario = session.get('id')
<<<<<<< HEAD
        self.tipo_usuario = session.get('tipo_usuario')
=======
>>>>>>> ajustes_finales

    def validar_correo_electronico(self):
        # Expresión regular para validar correos electrónicos
        patron = r'^(?=.{1,256})(?=.{1,64}@.{1,255}$)(?=.{1,255}$)((?!@)[\w&\'*+._%-]+(?:(?!@)[\w&\'*+._%-]|){0,63}(?<!@)@)+(?:(?!@)[\w&\'*+._%-]+(?:(?!@)[\w&\'*+._%-]|){0,63}(?<!@)\.)+(?:(?!@)[a-zA-Z]{2,63}(?:(?!@)[a-zA-Z]{2,63}|))$'
        if re.match(patron, self.email_nuevo):
            return True
        else:
            return False

    def informacion_usuario(self, email) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
            SELECT udp.nombre_completo nombre, udp.numero_documento documento, udp.direccion, udp.numero_celular celular
                FROM usuarios u 
                INNER JOIN usuario_datos_personales udp ON u.id_usuario_datos_personales=udp.id
                WHERE u.email=%s
        """
        cursor.execute(query, (email,))
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
        cursor = db.connection.cursor(dictionary=True)
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
        cursor = db.connection.cursor(dictionary=True)
        query = "SELECT id,nombre ocupacion FROM ocupacion o"
        cursor.execute(query)
        return cursor.fetchall()

<<<<<<< HEAD
    def obtener(self) -> Dict:
        # Obtener el cursor y el correo electrónico actual
        cursor = db.connection.cursor(dictionary=True)
        # Consultar los datos del usuario con sus ocupaciones
        #Este query es para obtener los contratistas
        query = """
            SELECT udp.nombre_completo,udp.numero_celular, udp.numero_documento, udp.direccion, GROUP_CONCAT(o.nombre SEPARATOR ', ') AS ocupaciones,udp.descripcion,o.id id_ocupacion
=======
    def obtener(self, id) -> Dict:
        # Obtener el cursor y el correo electrónico actual
        cursor = db.connection.cursor(dictionary=True)
        # Consultar los datos del usuario con sus ocupaciones
        query = """
             SELECT udp.nombre_completo,udp.numero_celular, udp.numero_documento, udp.direccion, GROUP_CONCAT(o.nombre SEPARATOR ', ') AS ocupaciones,o.id id_ocupacion
>>>>>>> ajustes_finales
        FROM usuario_datos_personales udp
        INNER JOIN usuarios u ON u.id_usuario_datos_personales = udp.id
        INNER JOIN usuario_ocupaciones uo ON uo.id_usuario =u.`id`
        INNER JOIN ocupacion o ON uo.id_ocupacion = o.id
        WHERE u.id=%s and uo.eliminado=0
        GROUP BY udp.nombre_completo, udp.numero_celular, udp.numero_documento, udp.direccion
        """
<<<<<<< HEAD
        cursor.execute(query, (self.id_usuario,))
        datos = cursor.fetchone()

        # Si los datos no se encuentran, consultar solo los datos básicos del usuario, es decir para obtener los datos del usuario cliente
        if datos is None:
            query_ = """
            SELECT udp.nombre_completo,udp.numero_celular, udp.numero_documento, udp.direccion,udp.descripcion
=======
        cursor.execute(query, (id,))
        datos = cursor.fetchone()

        # Si los datos no se encuentran, consultar solo los datos básicos del usuario
        if datos is None:
            query_ = """
            SELECT udp.nombre_completo,udp.numero_celular, udp.numero_documento, udp.direccion
>>>>>>> ajustes_finales
            FROM usuario_datos_personales udp
            INNER JOIN usuarios u ON u.id_usuario_datos_personales = udp.id
            WHERE u.id = %s
            """
<<<<<<< HEAD
            cursor.execute(query_, (self.id_usuario,))
=======
            cursor.execute(query_, (id,))
>>>>>>> ajustes_finales
            datos = cursor.fetchone()
            datos['ocupaciones'] = None

        return datos

<<<<<<< HEAD
    def validar_campos_vacios(self)->bool:
        dato=self.obtener()
        if any(valor == '' or valor == 0 or valor is None for valor in [dato['direccion'], dato['ocupaciones'], dato['descripcion'], dato['numero_celular']]) and self.tipo_usuario == 'Contratista':
            return True
        
        if any(valor =='' or valor==0 for valor in [dato['direccion'] ,dato['numero_celular']]) and self.tipo_usuario=='Cliente':
            return True

        else:
            return False
        
    def actualizar(self, nombre, celular, direccion,descripcion,id_usuario):
        cursor = db.connection.cursor()
        datos_actualizar = (nombre, celular, direccion,descripcion, id_usuario)
        query = 'UPDATE usuario_datos_personales SET nombre_completo = %s, numero_celular = %s, direccion=%s,descripcion=%s WHERE id = %s'
        cursor.execute(query, datos_actualizar)
        db.connection.commit()
        cursor.close()
        return None
=======
    def actualizar(self, nombre, celular, direccion, id_usuario):
        cursor = db.connection.cursor()
        datos_actualizar = (nombre, celular, direccion, id_usuario)
        query = 'UPDATE usuario_datos_personales SET nombre_completo = %s, numero_celular = %s, direccion=%s WHERE id = %s'
        cursor.execute(query, datos_actualizar)
        db.connection.commit()
        cursor.close()
        return f"registro(s) actualizado(s)"
>>>>>>> ajustes_finales

    def id_usuarios(self, id) -> Dict:
        cursor = db.connection.cursor(dictionary=True)
        query = """
            SELECT id_usuario_contratista,id_usuario_cliente
            FROM solicitud
            WHERE id=%s
        """
        cursor.execute(query, (id,))
        return cursor.fetchone()

    def calificar(self, observaciones, estrellas, id_solicitud, tipo_usuario) -> bool:
        cursor = db.connection.cursor(dictionary=True)

        query_validacion = """
        SELECT count(u.id) cantidad
            FROM calificacion c
            INNER JOIN usuarios u ON c.`id_usuario`=u.`id`
            INNER JOIN tipo_usuario tu ON u.id_tipo_usuario = tu.id
            WHERE c.`id_solicitud`=%s and tu.id=%s
        
        """
        valores = (id_solicitud, tipo_usuario)

        cursor.execute(query_validacion, valores)

        calificacion = cursor.fetchone()['cantidad']

        if calificacion == 0:
            fecha_actual = datetime.datetime.now()

            cadena_fecha = fecha_actual.strftime("%Y-%m-%d %H:%M:%S")

            informacion = (observaciones, estrellas,
                           id_solicitud, self.id_usuario, cadena_fecha)

            query_informacion = """
                    INSERT INTO calificacion (observaciones,numero_estrellas,id_solicitud,id_usuario,registro)
                    VALUES (%s,%s,%s,%s,%s)
                """

            cursor.execute(query_informacion, informacion)
            db.connection.commit()
            return True

        elif calificacion == 1:
            return False

    def ocupaciones_contratista(self, id):
        cursor = db.connection.cursor(dictionary=True)
        query = """select us.id_ocupacion as id
                    from usuarios u 
                    join usuario_ocupaciones us on u.id = us.id_usuario
                    where u.id = %s and us.eliminado = 0"""
        cursor.execute(query, (id,))
        return cursor.fetchall()

    def ocupaciones_eliminadas(self, id):
        cursor = db.connection.cursor(dictionary=True)
        query = """select us.id_ocupacion as id
                    from usuarios u 
                    join usuario_ocupaciones us on u.id = us.id_usuario
                    where u.id = %s and us.eliminado = 1"""
        cursor.execute(query, (id,))
        return cursor.fetchall()

    def agregar_ocupaciones(self, data):
        cursor = db.connection.cursor(dictionary=True)
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
        cursor = db.connection.cursor(dictionary=True)
        query_informacion = """
                    UPDATE usuario_ocupaciones set eliminado = 0 
                    where id_usuario = """ + str(id) + " and id_ocupacion in ("+data+");"

        cursor.execute(query_informacion)
        db.connection.commit()
        return True

<<<<<<< HEAD
=======
    def informacion_contratistas(self):
        cursor = db.connection.cursor(dictionary=True)
        query = """select u.id,u.email as email,us.nombre_completo,us.numero_celular as celular,GROUP_CONCAT(o.nombre SEPARATOR ', ') AS ocupaciones
                    from usuarios u
                    join usuario_datos_personales us on u.id_usuario_datos_personales = us.id
                    join usuario_ocupaciones uc on uc.id_usuario = u.id
                    join ocupacion o on uc.id_ocupacion = o.id
                    where u.id_tipo_usuario = 2 and uc.eliminado = 0
                    group by u.id
                    order by us.nombre_completo,o.nombre;"""
        cursor.execute(query)
        return cursor.fetchall()

    def Eventos_contratistas(self, id):
        cursor = db.connection.cursor(dictionary=True)
        query = """select s.id,s.descripcion,concat(s.horario,'T',s.hora) as fecha ,if(s.id_estado = 1,'#3346FF',if(s.id_estado= 2,'#0cde00',if(s.id_estado = 3,'#FFF033','#E20202'))) as color
                    from solicitud s
                    where s.id_usuario_contratista = %s ;"""
        cursor.execute(query,(id,))
        return cursor.fetchall()

>>>>>>> ajustes_finales

class DatoUnicoEmail(Exception):
    ...


class CorreoInvalido(Exception):
    ...
