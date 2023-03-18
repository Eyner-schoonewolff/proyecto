from db.database import *
import datetime

class solicitar:
     def __init__(self, fecha: str, hora: str, tipo_contratista: int, contratista: str, problema: str) -> None:
        self.fecha = fecha
        self.hora = hora
        self.tipo_contratista = tipo_contratista
        self.contratista = contratista
        self.problema = problema
    
     def agregar(self,id_user) -> None:
        segundo = datetime.datetime.now()
        fechatime = self.fecha + ' ' + self.hora+':'+repr(segundo.second) ;
        cursor = db.connection.cursor()
        informacion = (self.contratista,fechatime,self.problema,id_user)
        query_informacion = """
                    INSERT INTO solicitud (id_usuario_ocupaciones,horario,descripcion,id_usuario_cliente)
                    VALUES (%s,%s,%s,%s)
                """
        cursor.execute(query_informacion, (informacion))
        db.connection.commit()
        return '1'