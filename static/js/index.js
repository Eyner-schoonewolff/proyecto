document.querySelector("#BotonLogin").addEventListener('click', async () => {
    const email = document.querySelector("#inputEmail").value;
    const contrasenia = document.querySelector("#inputcontrasenia").value;

    const datos = {
        email,
        contrasenia
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
            await Swal.fire({
                title: "¡Éxito!",
                text: "El usuario se ha logueado correctamente",
                icon: "success",
                confirmButtonText: "Aceptar",
                customClass: {
                    container: 'my-swal-container'
                }
            });

            window.location.href = data.home;
            localStorage.setItem("jwt-token", data.token);
            console.log(token);
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
