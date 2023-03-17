


const li        = document.querySelectorAll('.li')
const bloque    = document.querySelectorAll('.bloque')

// CLICK en li
    // TODOS .li quitar la clase activo
    // TODOS .bloque quitar la clase activo
    // .li con la posicion se añadimos la clase activo
    // .bloque con la posicion se añadimos la clase activo
$(".c1").css('display', 'none')
$(".c0").css('display', 'none')
// Recorriendo todos los LI
li.forEach( ( cadaLi , i )=>{

   
    // Asignando un CLICK a CADALI
    li[i].addEventListener('click',()=>{
       
        // Recorrer TODOS los .li
        li.forEach( ( cadaLi , i )=>{
            // Quitando la clase activo de cada li
            li[i].classList.remove('activo')
            // Quitando la clase activo de cada bloque
            bloque[i].classList.remove('activo')
        })
        

        // En el li que hemos click le añadimos la clase activo
        li[i].classList.add('activo')
        // En el bloque con la misma posición le añadimos la clase activo
        bloque[i].classList.add('activo')

        if(i == 0){
            $(".c0").css('display', 'block')
            $(".c1").css('display', 'none')
        }else{
            $(".c1").css('display', 'block')
            $(".c0").css('display', 'none')
        }

    })
    
})

function open_clientes() {

        // Recorrer TODOS los .li
        li.forEach( ( cadaLi , i )=>{
            // Quitando la clase activo de cada li
            li[0].classList.remove('activo')
            // Quitando la clase activo de cada bloque
            bloque[0].classList.remove('activo')
        })
        // En el li que hemos click le añadimos la clase activo
        li[0].classList.add('activo')
        // En el bloque con la misma posición le añadimos la clase activo
        bloque[0].classList.add('activo')
        $(".c0").css('display', 'block')
}


$('#fecha_cor').datetimepicker({
	format: 'YYYY-MM-DD',
})

$('#fecha_con').datetimepicker({
	format: 'YYYY-MM-DD',
})


open_clientes()
