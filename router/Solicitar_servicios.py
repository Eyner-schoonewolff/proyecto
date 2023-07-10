from flask import Blueprint
from decorador.decoradores import  *
from controlador.c_solicitar_servicios import Solicitar_controlador

solicitar_servi = Blueprint('solicitar_servi', __name__, static_url_path='/static',
                            template_folder="templates")


@solicitar_servi.route("/solicitar_serv", methods=["POST"])
def solicitar_():
    solicitar_controlador=Solicitar_controlador()
    return solicitar_controlador.servicio()


@solicitar_servi.route("/eliminar_solicitud/<id>", methods=['GET'])
@login_required_home
def eliminar_(id):
    solicitar_controlador=Solicitar_controlador()
    return solicitar_controlador.cancelar(id)

