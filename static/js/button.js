document.querySelector('#formulario').addEventListener('keyup', () => {
    const usuario =document.querySelector('#usuario')
    const contrasenia =document.querySelector('#contrasenia')
    const btn = document.querySelector('#btn-registro')
    let desativar=false
    if (usuario.value == '' || contrasenia.value == '') {
        desativar = true
    }
    if (desativar == true) {
        btn.disabled = true
    } else {
        btn.disabled = false
    }
});




