from seguridad.registrar import *
from decorador.decoradores import *

class Registrar_controlador():

    def c_agregar_usuario(self):
        usuario_nuevo = request.get_json()
        email = str(usuario_nuevo['email'])
        contrasenia = usuario_nuevo['contrasenia']
        rol = int(usuario_nuevo['rol'])
        nombre = usuario_nuevo['nombre']
        tipo_documento = int(usuario_nuevo['tipo_documento'])
        numero_documento = int(usuario_nuevo['numero_documento'])
        descripcion = str(usuario_nuevo['descripcion'])

        registro = Usuario(email=email, contrasenia=contrasenia, rol=rol,
                           nombre=nombre, tipo_documento=tipo_documento, numero_documento=numero_documento, descripcion=descripcion)
        try:
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

        except CorreoExistenteException as e:
            return {"registro": False, "mensaje": str(e)}
        except DocumentoExistenteException as e:
            return {"registro": False, "mensaje": str(e)}
        except ExistenteException as e:
            return {"registro": False, "mensaje": str(e)}
        except DatosInvalidoException as e:
            return {"registro": False, "mensaje": str(e)}
