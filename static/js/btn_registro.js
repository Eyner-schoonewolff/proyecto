document.querySelector('#formulario').addEventListener('keyup', () => {
    const nombre = document.querySelector('#nombre')
    const email = document.querySelector('#email')
    const contrasenia = document.querySelector('#contrasenia')
    const documento = document.querySelector('#numeroDocumento')

    const btn = document.querySelector('#btn-registro')
    let desativar = false
    if (nombre.value == '' || contrasenia.value == '' || email.value == '' || documento.value == '') {
        desativar = true
    }
    if (desativar == true) {
        btn.disabled = true
    } else {
        btn.disabled = false
    }
});




