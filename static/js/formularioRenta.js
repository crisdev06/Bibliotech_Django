document.addEventListener('DOMContentLoaded', function() {

    const rutInput = document.querySelector('#Rut');
    const idLibroInput = document.querySelector('#idLibro');
    const fechaRentaInput = document.querySelector('#fechaRenta');
    const fechaDevolucionInput = document.querySelector('#fechaDevolucion');
    const formulario = document.querySelector('#rentaForm');

    rutInput.addEventListener('blur', validar);
    idLibroInput.addEventListener('blur', validar);
    fechaRentaInput.addEventListener('blur', validar);
    fechaDevolucionInput.addEventListener('blur', validar);

    function validar(e) {

        const hoy = new Date();
        hoy.setHours(0,0,0,0); // ignorar horas, minutos y segundos

        const fechaPrestamo = new Date(fechaRentaInput.value);
        const fechaDevolucion = new Date(fechaDevolucionInput.value);


        if(e.target.value.trim() === "") {
            mostrarAlerta(`El campo ${e.target.id} es obligatorio`);
        }
        else if(e.target.id === 'Rut' && !validarRut(e.target.value)) {
            mostrarAlerta('El rut no es válido');
        }
        else if(e.target.id === 'idLibro' && !validarIdLibro(e.target.value)) {
            mostrarAlerta('El ID del libro no es válido. Debe tener el formato LBRXXX, donde XXX son tres dígitos.');
        }
        else if(e.target.id === 'fechaRenta' && fechaPrestamo < hoy) {
            mostrarAlerta('La fecha de renta no puede ser anterior a hoy.');
        }
        else if(e.target.id === 'fechaDevolucion' && fechaDevolucion <= fechaPrestamo) {
            mostrarAlerta('La fecha de devolución debe ser posterior a la fecha de renta.');
        }
        else{
            limpiarAlerta();
        }
    }

    function mostrarAlerta(mensaje){

        limpiarAlerta();
        // verificar si ya hay una alerta
        const alertaExistente = formulario.querySelector('.alert');
        if (alertaExistente) {
            alertaExistente.remove();
        }

        const error = document.createElement('P');
        error.textContent = mensaje;
        
        error.classList.add('alert', 'alert-danger', 'mt-2');
         
        formulario.appendChild(error);

    }
    function limpiarAlerta() {
        const alertaExistente = formulario.querySelector('.alert');
        if (alertaExistente) {
            alertaExistente.remove();
        }
    }

    function validarIdLibro(id) {
 
        return /^LBR\d{3}$/.test(id.toUpperCase());
    }


    function validarRut(rutCompleto) {
        // Limpiar puntos y guión
        let rut = rutCompleto.replace(/\./g, '').replace('-', '');
        
        // Separar cuerpo y dígito verificador
        let cuerpo = rut.slice(0, -1);
        let dv = rut.slice(-1).toUpperCase();

        // Revisar que cuerpo sea numérico
        if (!/^\d+$/.test(cuerpo)) return false;

        // Calcular dígito verificador
        let suma = 0;
        let multiplo = 2;

        for (let i = cuerpo.length - 1; i >= 0; i--) {
            suma += parseInt(cuerpo.charAt(i)) * multiplo;
            multiplo = multiplo < 7 ? multiplo + 1 : 2;
        }

        let dvEsperado = 11 - (suma % 11);
        if (dvEsperado === 11) dvEsperado = '0';
        else if (dvEsperado === 10) dvEsperado = 'K';
        else dvEsperado = dvEsperado.toString();

        return dv === dvEsperado;
    }

});