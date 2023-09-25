var token = "";

const email = document.querySelector("#inputEmail");
const contrasenia = document.querySelector("#inputcontrasenia");
const btn_login = document.querySelector("#BotonLogin");

email.addEventListener("keydown", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        btn_login.click();
    }
});

contrasenia.addEventListener("keydown", function (event) {
    if (event.keyCode === 13) {
        event.preventDefault();
        btn_login.click();
    }
});


btn_login.addEventListener('click', async () => {

    const datos = {
        email:email.value,
        contrasenia:contrasenia.value
    };

    try {
        const respuesta = await fetch('http://localhost:3000/auth', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(datos)
        });

        const data = await respuesta.json();

        if (data.login) {
            
            window.location.href = data.home;
            localStorage.setItem("jwt-token", data.token);
            localStorage.setItem("exp", data.exp);
            localStorage.setItem("exp_seg", data.exp_token_seg);
            console.log(data.exp_token_seg);
            return data;

        } else {
            await Swal.fire({
                title: "Hubo un error",
                text: data.excepcion,
                icon: "error",
                confirmButtonText: "Aceptar",
                customClass: {
                    container: 'my-swal-container'
                }
            });

            window.location.href = data.home;
        }
    } catch (error) {
        console.error(error);
    }
});
