from flask import Blueprint, request, session,redirect,url_for
from seguridad.Model_solicitar_servicio import solicitar
solicitar_servi = Blueprint('solicitar_servi', __name__, static_url_path='/static',
                      template_folder="templates")


@solicitar_servi.route("/solicitar_serv", methods=["POST"])
def solicitar_():
    solicitu_nueva = request.get_json()
    fecha = str(solicitu_nueva['fecha'])
    hora = str(solicitu_nueva['hora'])
    tipo_contratista = int(solicitu_nueva['servicio'])
    contratista = int(solicitu_nueva['contratista'])
    problema = str(solicitu_nueva['problema'])
    id_user = session.get('id')

    Solicitar = solicitar(fecha=fecha,hora=hora,tipo_contratista = tipo_contratista,contratista = contratista,problema = problema)

    valor=Solicitar.agregar(id_user)
   
    if valor == '1':
        return {"numero": 1}
    else:
        return {"numero": 0}
    


@solicitar_servi.route("/eliminar_solicitud",methods=['GET','DELETE'])
def eliminar_():
    print('se elimino')
    return redirect(url_for('menus.consultar'))
   