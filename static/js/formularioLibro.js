document.addEventListener('DOMContentLoaded', function() {

    const idLibroInput = document.querySelector('#idLibro');
    const tituloInput = document.querySelector('#Titulo');
    const autorInput = document.querySelector('#Autor');
    const editorialInput = document.querySelector('#Editorial');
    const anioPublicacionInput = document.querySelector('#Publicacion');
    const stockInput = document.querySelector('#Stock');
    const formulario = document.querySelector('#registrarlibro');

    idLibroInput.addEventListener('blur', validar);
    tituloInput.addEventListener('blur', validar);
    autorInput.addEventListener('blur', validar);
    editorialInput.addEventListener('blur', validar);
    anioPublicacionInput.addEventListener('blur', validar);
    stockInput.addEventListener('blur', validar);



    function validar(e) {

        const hoy = new Date();
        hoy.setHours(0,0,0,0); // ignorar horas, minutos y segundos

        if(e.target.value.trim() === "") {
            mostrarAlerta(`El campo ${e.target.id} es obligatorio`);
        }

        else if(e.target.id === 'idLibro' && !validarIdLibro(e.target.value)) {
            mostrarAlerta('El ID del libro no es válido. Debe tener el formato LBRXXX, donde XXX son tres dígitos.');
        }
        else if((e.target.id === 'Autor' && !validarNombre(e.target.value)) || (e.target.id === 'Apellido' && !validarNombre(e.target.value))) {
            mostrarAlerta(`El campo ${e.target.id} solo acepta letras y sin espacios`);
        }
        else if(e.target.id === 'Publicacion' && (e.target.value < 0 || e.target.value > hoy.getFullYear())) {
            mostrarAlerta(`El año de publicación no puede ser mayor a ${hoy.getFullYear()}, ni menor a 0`);
        }
        else if(e.target.id === 'Stock' && (Number(e.target.value) <= 0 || !Number.isInteger(Number(e.target.value)))) {
            mostrarAlerta('El stock debe ser un número entero positivo.');
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

    function validarNombre(valor) {
        // acepta letras y acentos
        const regex = /^[a-zA-ZÁÉÍÓÚáéíóúÑñ]+$/; 
        return regex.test(valor);
    }




    
});