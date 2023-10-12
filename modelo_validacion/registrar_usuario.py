from pydantic import BaseModel,validator,Field,EmailStr
import re
from seguridad.registrar import *
from validate_email_address import validate_email

class BaseModelCustom(BaseModel):
    class Config:
         error_msg_templates = {
            'value_error.email': 'El valor proporcionado no es una dirección de correo electrónico válida.',
            'value_error.any_str.max_length': 'Asegúrate de que este valor tenga como máximo {limit_value} caracteres.'
        }


class Usuario(BaseModelCustom):
    email: EmailStr
    contrasenia: str
    rol: int
    nombre: str
    tipo_documento: int
    numero_documento: int 
    descripcion: str

    contrasenia: str = Field(..., max_length = 8)  # Establece el máximo en 8 caracteres para el campo contrasenia
    descripcion: str = Field(..., max_length = 255)

    # @validator('email')
    # def validate_email(cls, email):
    #     email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
    #     if not re.match(email_pattern, email):
    #         raise CorreoNoValido('El correo electrónico no es válido')
    #     return email
    
    # @validator('contrasenia')
    # def contrasenia_caracteres(cls, contrasenia):

    #     if len(contrasenia) < 4:
    #         raise ValueError('La longitud mínima  es de 4 caracteres.')

    #     if len(contrasenia) > 50:
    #         raise ValueError('La longitud máxima es de 50 caracteres.')

    #     return contrasenia




