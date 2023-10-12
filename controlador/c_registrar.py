from seguridad.registrar import *
from decorador.decoradores import *
from pydantic import ValidationError
from modelo_validacion.registrar_usuario import Usuario
from flask_jwt_extended import get_jwt_identity, jwt_required

class Registrar_controlador():

    def mensaje_error(self, errores) -> dict:
        if len(errores)<=1:
            mensaje_completo = f"{errores[0]['loc'][0]}: {errores[0]['msg']}"
            return mensaje_completo
        
        mensaje=[]
        for error in errores:
            msg = f"{error['loc'][0]}: {error['msg']}"
            mensaje.append(msg)
        mensaje_completo = "\n".join(mensaje)

        return mensaje_completo

    def c_agregar_usuario(self):
        usuario_nuevo = request.get_json()
     
        try:
            datos_validos = Usuario(**usuario_nuevo)
            
            email = datos_validos.email
            contrasenia = datos_validos.contrasenia
            rol = datos_validos.rol
            nombre = datos_validos.nombre
            tipo_documento = datos_validos.tipo_documento
            numero_documento = datos_validos.numero_documento
            descripcion = datos_validos.descripcion

            registro = Usuario(email=email, contrasenia=contrasenia, rol=rol,
                            nombre=nombre, tipo_documento=tipo_documento, numero_documento=numero_documento, descripcion=descripcion)
            if registro.existe_():
                raise CorreoExistenteException(
                    "El correo y el número de documento ya se encuentran registrados")
            elif registro.existe_documento():
                raise DocumentoExistenteException(
                    "El número de documento ya existe, por favor verificar")
            elif registro.existe_correo():
                raise ExistenteException(
                    "El correo que deseas ingresar ya existe ")
            elif registro.valor_invalido():
                raise DatosInvalidoException(
                    "No se debio enviar este dato aqui, por favor verificar bien"
                )
            else:
                registro.agregar()
                return {"registro": True, "home": "/templates/index.html","mensaje":"registro exitoso"}
        

        except ValidationError as e:
            errores = e.errors()
            obtener_mensaje_errores = self.mensaje_error(errores)

            return jsonify({"registro": False, "mensaje": obtener_mensaje_errores}), 400
        except CorreoExistenteException as e:
            return {"registro": False, "mensaje": str(e)}
        except DocumentoExistenteException as e:
            return {"registro": False, "mensaje": str(e)}
        except ExistenteException as e:
            return {"registro": False, "mensaje": str(e)}
        except DatosInvalidoException as e:
            return {"registro": False, "mensaje": str(e)}
