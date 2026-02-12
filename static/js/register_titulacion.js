document.addEventListener("DOMContentLoaded", function () {
    const tipoTitulacion = document.getElementById("id_tipo_titulacion");
    const epapInput = document.getElementById("id_presion_epap");
    const frecuenciaInput = document.getElementById("id_frecuencia_respiratoria");

    // Seleccionamos los contenedores de cada uno
    const epapRow = epapInput.closest(".form-row-2");
    const frecuenciaRow = frecuenciaInput.closest(".form-row-2");

    function toggleCampos() {
        const valor = tipoTitulacion.value;

        if (valor === "BPAP ST") {
            // Se muestran AMBOS y son obligatorios
            epapRow.style.display = "block";
            frecuenciaRow.style.display = "block";
            epapInput.required = true;
            frecuenciaInput.required = true;
        } 
        else if (valor === "BPAP") {
            // Solo EPAP es visible y obligatorio
            epapRow.style.display = "block";
            frecuenciaRow.style.display = "none";
            epapInput.required = true;
            frecuenciaInput.required = false;
            frecuenciaInput.value = ""; 
        } 
        else {
            // Se ocultan ambos (para CPAP u otros)
            epapRow.style.display = "none";
            frecuenciaRow.style.display = "none";
            epapInput.required = false;
            frecuenciaInput.required = false;
            epapInput.value = "";
            frecuenciaInput.value = "";
        }
    }

    // Ejecutar al cargar y al cambiar
    toggleCampos();
    tipoTitulacion.addEventListener("change", toggleCampos);
});