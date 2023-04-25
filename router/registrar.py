from flask import Blueprint, request, session, render_template, redirect, url_for
from seguridad.registrar import *

registrar = Blueprint('registrar', __name__, static_url_path='/static',
                      template_folder="templates")


@registrar.route("/registrar")
def registro():
    logueado = session.get('login')
    if not logueado:
        return render_template("registrar.html")
    else:
        return redirect(url_for('login.index'))


@registrar.route("/auth_registro", methods=["POST"])
def auth():
    usuario_nuevo = request.get_json()

    email = str(usuario_nuevo['email'])
    contrasenia = usuario_nuevo['contrasenia']
    rol = int(usuario_nuevo['rol'])
    nombre = usuario_nuevo['nombre']
    tipo_documento = int(usuario_nuevo['tipo_documento'])
    numero_documento = int(usuario_nuevo['numero_documento'])
    descripcion = str(usuario_nuevo['descripcion'])
    
    registro = Usuario(email=email, contrasenia=contrasenia, rol=rol,
                       nombre=nombre, tipo_documento=tipo_documento, numero_documento=numero_documento,descripcion=descripcion)
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
            return {"registro": True, "home": "/"}

    except CorreoExistenteException as e:
        return {"registro": False, "mensaje": str(e)}
    except DocumentoExistenteException as e:
        return {"registro": False, "mensaje": str(e)}
    except ExistenteException as e:
        return {"registro": False, "mensaje": str(e)}
    except DatosInvalidoException as e:
        return {"registro": False, "mensaje": str(e)}

