function tablaCotizar() {
	$.ajax({
		url: "Viajes/tablaCotizar/" + idsolicitud,
		type: "POST",
		cache: false,
		async: false,
		success: function (data) {
			const datos = JSON.parse(data);

			// Crear un objeto para contar las fechas_aplique
			const fechaCount = {};

			// arreglo con el nuevo objeto
			let arreglo = [];

			// para guardar las descripciones repetidas 
			let descripRepetidas ;
			// para guardar las fechas repetidas
			let fechasMasRepetidas;
			

			// Contar la frecuencia de cada fecha_aplique
			datos.forEach((item) => {
				const fecha = item.fecha_aplique;
				fechaCount[fecha] = (fechaCount[fecha] || 0) + 1;
			});

			// Encontrar las fechas_aplique que se repiten más de una vez
			fechasMasRepetidas = Object.keys(fechaCount).filter(
				(fecha) => fechaCount[fecha] > 1
			);

			fechasMasRepetidas.forEach((element) => {

				let nuevoObjeto = {};


				// calcula la cantidad de columna tiene el objeto por medio de las fechas iguales
				infoForFecha = datos.filter((fecha) => fecha.fecha_aplique == element);

				const decrip = {};
				infoForFecha.forEach((item) => {
					const nombreDescripcion = item.descripcion;
					decrip[nombreDescripcion] = (decrip[nombreDescripcion] || 0) + 1;
				});

				// calculamos cual es la descripción que mas se repite
				descripRepetidas = Object.keys(decrip).filter(
					(de) => decrip[de] > 1
				);

				
				descripRepetidas.forEach((element) => {
					// Filtrar objetos con descripción "Hospedaje"
					const descripObjects = infoForFecha.filter(
						(obj) => obj.descripcion === element
					);

					// los datos fecha_aplique, descripcion, destino, se repiten entonces se guarda primero en el objeto
					nuevoObjeto['id'] = descripObjects[0].id
					nuevoObjeto['fecha_aplique'] = descripObjects[0].fecha_aplique
					nuevoObjeto['descripcion'] = descripObjects[0].descripcion
					nuevoObjeto['destino'] = descripObjects[0].destino


					// creamos otro objeto con las nuevas propiedades
					descripObjects.forEach((obj) => {
						nuevoObjeto[obj.nombre] = obj.valor_campo;
					});
					arreglo.push(nuevoObjeto)
				});
				
			});
			
			let arregloTabla = [];
			fechasMasRepetidas.forEach(element => {
				
				
				const datosFiltrados = arreglo.filter((i) => i.fecha_aplique == element)

				descripRepetidas.forEach(e => {
				 	const datosFiltradosconsulta = datos.filter((i) => i.fecha_aplique == element && i.descripcion != e);

					 arregloTabla.push(datosFiltrados[0])

					 // creamos otro objeto con las nuevas propiedades
					datosFiltradosconsulta.forEach((obj) => {
						let arrgeloDatosSobrantes = {};
						 arrgeloDatosSobrantes["id"] = obj.id;
						 arrgeloDatosSobrantes["fecha_aplique"] = obj.fecha_aplique;
						 arrgeloDatosSobrantes["descripcion"] = obj.descripcion;
						 arrgeloDatosSobrantes["destino"] = obj.destino;
						 arrgeloDatosSobrantes[obj.nombre] = obj.valor_campo;

						 arregloTabla.push(arrgeloDatosSobrantes);
					});
				});
			});
			// console.log("arreglo tabla ",arregloTabla);
			pintarTabla(arregloTabla);
		},
	});
}