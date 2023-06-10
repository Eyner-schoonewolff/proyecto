from flask import Blueprint, request, session, render_template,jsonify
from seguridad.datos_usuario import DatosUsuario,DatoUnicoEmail,CorreoInvalido
from seguridad.Model_solicitar_servicio import *
from decorador.decoradores import  *
import json


class Datos_personales_controlador():
    ...