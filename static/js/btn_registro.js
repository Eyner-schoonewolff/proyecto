document.querySelector('#formulario').addEventListener('keyup', () => {
    const nombre = document.querySelector('#nombre')
    const email = document.querySelector('#email')
    const contrasenia = document.querySelector('#contrasenia')
    const documento = document.querySelector('#numeroDocumento')
    const direccion = document.querySelector('#direccion')
    const numeroCelular = document.querySelector('#numeroCelular')
    const btn = document.querySelector('#btn-registro')
    let desativar = false
    if (nombre.value == '' || contrasenia.value == '' || email.value == '' || documento.value == '' ||
        direccion.value == '' ||
        numeroCelular.value == '') 
    {
        desativar = true
    }
    if (desativar == true) {
        btn.disabled = true
    } else {
        btn.disabled = false
    }
});




