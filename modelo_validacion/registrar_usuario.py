from pydantic import BaseModel,validator,Field,EmailStr
from seguridad.registrar import *


class BaseModelCustom(BaseModel):
    class Config:
         error_msg_templates = {
            'value_error.email': 'El valor proporcionado no es una dirección de correo electrónico válida.',
            'value_error.any_str.max_length': 'Asegúrate de que este valor tenga como máximo {limit_value} caracteres.',
            'value_error.any_str.min_length': 'Asegúrate de que este valor tenga como mínimo {limit_value} caracteres.',
        }


class UsuarioModelo(BaseModelCustom):
    email: EmailStr
    contrasenia: str
    rol: int
    nombre: str
    tipo_documento: int
    numero_documento: int 
    descripcion: str

    contrasenia: str = Field(...,min_length = 6, max_length = 16)  # Establece el máximo en 8 caracteres para el campo contrasenia
    descripcion: str = Field(..., max_length = 255)


    @validator('rol',pre=True)
    def rol_validate(cls, rol):
            try:
                valor_rol_entero = int (rol)
            except ValueError:
                raise ValueError('El campo rol no puede ser una cadena (str). Debe ser un valor entero.')

            if isinstance(valor_rol_entero, str):
                raise ValueError('El campo rol no puede ser una cadena (str). Debe ser un valor entero.')
                
            elif valor_rol_entero not in (0, 2, 3):
                raise ValueError('El campo rol debe ser 0, 2 o 3.')  # Mensaje personalizado

                 
            return rol
        
                 






