from flask import Blueprint, request, session, redirect, url_for
import os
import uuid
from werkzeug.utils import secure_filename
from seguridad.Model_solicitar_servicio import Solicitar
from decorador.decoradores import  *


class Solicitar_controlador():
    ...