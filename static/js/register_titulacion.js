document.addEventListener("DOMContentLoaded", function () {

    const tipoTitulacion = document.getElementById("id_tipo_titulacion");
    const epapInput = document.getElementById("id_presion_epap");

    // contenedor del campo EPAP (label + input + errores)
    const epapRow = epapInput.closest(".form-row-2");

    function toggleEpap() {
        if (tipoTitulacion.value === "BPAP") {
            epapRow.style.display = "block";
            epapInput.required = true;
        } else {
            epapRow.style.display = "none";
            epapInput.required = false;
            epapInput.value = ""; // limpiar valor
        }
    }

    // Ejecutar al cargar
    toggleEpap();

    // Ejecutar cuando cambie
    tipoTitulacion.addEventListener("change", toggleEpap);
});
