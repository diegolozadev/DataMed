document.addEventListener("DOMContentLoaded", function () {

    const modo_ventilatorio = document.getElementById("id_modo_ventilatorio");
    const epapInput = document.getElementById("id_presion_epap");

    // contenedor del campo EPAP (label + input + errores)
    const epapRow = epapInput.closest(".form-row-2");

    function toggleEpap() {
        if (modo_ventilatorio.value === "BPAP" || modo_ventilatorio.value === "BPAP ST") {
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
    modo_ventilatorio.addEventListener("change", toggleEpap);
});
