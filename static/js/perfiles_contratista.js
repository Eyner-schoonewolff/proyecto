function agregar() {
    $.ajax({
        url: '/contratistas',
        method: 'GET',
        success: function (datos) {
            let html = '';
            let con = 1;
          
            $.each(datos, function (i, item) {
                console.log(item.email);
                html += `<div class="mx-5 py-3 ">
                <div class="slide-container swiper">
                    <div class="slide-content">
                        <div class="card-wrapper swiper-wrapper">
                        
                            <div class="card swiper-slide mb-5">
                                <div class="image-content">
                                    <span class="overlay"></span>
                                    <div class="card-image">
                                        <img src="../static/imagen/perfiles.png" id="img">
                                    </div>
                                </div>
                                <div class="card-body">
                                    <h2>Contratista ${con}</h2>
                                    <p class="card-text">
                                    ${item.nombre_completo}
                                    </p>
                                    <p class="card-text">
                                        <b>Telefono:</b> ${item.celular}<br>
                                        <b>Correo:</b> ${item.email}<br>
                                        <b>Ocupaciones:</b> ${item.ocupaciones}.
                                    </p>
                                </div>


                            </div>
                        </div>
                    </div>
                </div>
                </div>`;
                con++;
            })

   
            $("#container_div").append(html);
        }

    })



}

agregar()