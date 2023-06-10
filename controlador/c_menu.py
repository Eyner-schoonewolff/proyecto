from flask import Blueprint, render_template, redirect, url_for, session, request, jsonify
from seguridad.Model_solicitar_servicio import Solicitar
from seguridad.datos_usuario import DatosUsuario
from seguridad.perfiles import Perfiles
from seguridad.contacto import Contacto, ValidacionDatosContacto
from decorador.decoradores import  *


class Menu_controlador():
    ...