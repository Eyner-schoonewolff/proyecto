from seguridad.registrar import *
from decorador.decoradores import *
from pydantic import ValidationError
from modelo_validacion.registrar_usuario import UsuarioModelo
from flask_jwt_extended import get_jwt_identity, jwt_required

#agregar tipos de datos
class UsuarioControlador:

    def mensaje_error(self, errores) -> str:
        if len(errores)<=1:
            mensaje_completo = f"{errores[0]['loc'][0]}: {errores[0]['msg']}"
            return mensaje_completo
        
        mensaje=[]
        for error in errores:
            msg = f"{error['loc'][0]}: {error['msg']}"
            mensaje.append(msg)
        mensaje_completo = "\n".join(mensaje)

        return mensaje_completo

    def agregar_usuario(self,usuario:UsuarioModelo): # crear objeto Usuario y pasarlo
            
            registro = Usuario(email=usuario.email,
                                contrasenia=usuario.contrasenia,
                                rol=usuario.rol,
                                nombre=usuario.nombre, 
                                tipo_documento=usuario.tipo_documento,
                                numero_documento=usuario.numero_documento, 
                                descripcion=usuario.descripcion
                                )
            
            if registro.existe_():
                return {"registro": False, "mensaje":"El correo y el número de documento ya se encuentran registrados"}
              
            elif registro.existe_documento():
                return {"registro": False, "mensaje":  "El número de documento ya existe, por favor verificar"}
            
            elif registro.existe_correo():
                return {"registro": False, "mensaje": "El correo que deseas ingresar ya existe "}
            
            elif registro.valor_invalido():
                return {"registro": False, "mensaje": "No se debio enviar este dato aqui, por favor verificar bien"}
             
            else:
                registro.agregar()
                return {"registro": True, "home": "/templates/index.html","mensaje":"registro exitoso"}
        

  
  
