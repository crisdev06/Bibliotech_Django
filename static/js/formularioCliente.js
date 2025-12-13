document.addEventListener('DOMContentLoaded', function() {

    const rutInput = document.querySelector('#Rut');
    const nombreInput = document.querySelector('#Nombre');
    const apellidoInput = document.querySelector('#Apellido');
    const emailInput = document.querySelector('#Email');
    const telefonoInput = document.querySelector('#Telefono');
    const contraseniaInput = document.querySelector('#Password');
    const formulario = document.querySelector('#formularioCliente');

    rutInput.addEventListener('blur', validar);
    nombreInput.addEventListener('blur', validar);
    apellidoInput.addEventListener('blur', validar);
    emailInput.addEventListener('blur', validar);
    telefonoInput.addEventListener('blur', validar);
    contraseniaInput.addEventListener('blur', validar);

    function validar(e) {

        if(e.target.value.trim() === "") {
            console.log("primera validacion");
            mostrarAlerta(`El campo ${e.target.id} es obligatorio`);
        }
        else if(e.target.id === 'Rut' && !validarRut(e.target.value)) {
            mostrarAlerta('El rut no es válido');
        }
        else if((e.target.id === 'Nombre' && !validarNombre(e.target.value)) || (e.target.id === 'Apellido' && !validarNombre(e.target.value))) {
            mostrarAlerta(`El campo ${e.target.id} solo acepta letras y sin espacios`);

        }
        else if(e.target.id === 'Telefono' && !validarTelefono(e.target.value)) {
            mostrarAlerta('El teléfono no es válido. Debe comenzar con 9 y tener 9 dígitos.');
        }
        else if(e.target.id === 'Email' && !validarEmail(e.target.value)) {
            mostrarAlerta('El correo no es válido');
        }
        else if(e.target.id === 'Password' && e.target.value.length < 4) {
            mostrarAlerta('La contraseña debe tener al menos 4 caracteres');
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
    
    function validarNombre(valor) {
        // acepta letras y acentos
        const regex = /^[a-zA-ZÁÉÍÓÚáéíóúÑñ]+$/; 
        return regex.test(valor);
    }

    function validarEmail(email) {
        const regex = /^\S+@\S+\.\S+$/;
        return regex.test(email);
    }
    function limpiarAlerta() {
        const alertaExistente = formulario.querySelector('.alert');
        if (alertaExistente) {
            alertaExistente.remove();
        }
    }

    function validarTelefono(valor) {
        // Solo números y que empiece con 9, longitud de 9 dígitos
        return /^9\d{8}$/.test(valor);
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
