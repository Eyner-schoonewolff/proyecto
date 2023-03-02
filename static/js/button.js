document.querySelector('#formulario').addEventListener('keyup', () => {
    const btn = document.querySelector('#btn-registro')
    const form = document.querySelector('#formulario')
    let desativar=false
    if (form.rol.value == '' || form.usuario.value == '' || form.contraseña.value == '') {
        desativar = true
    }
    if (desativar == true) {
        btn.disabled = true
    } else {
        btn.disabled = false
    }
});




