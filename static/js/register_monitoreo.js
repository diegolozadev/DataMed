document.addEventListener("DOMContentLoaded", function () {
    // 1. Referencias a los selectores e inputs (Django genera los IDs como id_nombre)
    const modoVentilatorio = document.getElementById("id_modo_ventilatorio");
    const epapInput = document.getElementById("id_presion_epap");
    const frecuenciaInput = document.getElementById("id_frecuencia_respiratoria");

    // 2. Referencias a las COLUMNAS (los contenedores que queremos ocultar)
    const colIpaps = document.getElementById("col_ipap");
    const colEpap = document.getElementById("col_epap");
    const colFrecuencia = document.getElementById("col_frecuencia");

    // 3. Referencias para el cálculo de porcentaje
    const basalInput = document.getElementById("id_hipopnea_basal");
    const residualInput = document.getElementById("id_hipopnea_residual");
    const porcentajeOutput = document.getElementById("id_porcentaje_correccion");

    function toggleCampos() {
        const valor = modoVentilatorio.value;

        // Lógica según el Modo Ventilatorio
        if (valor === "BPAP ST") {
            colEpap.style.display = "block";
            colFrecuencia.style.display = "block";
        } 
        else if (valor === "BPAP S" || valor === "BPAP") {
            colEpap.style.display = "block";
            colFrecuencia.style.display = "none";
            frecuenciaInput.value = ""; 
        } 
        else {
            // Caso CPAP: Oculta EPAP y Frecuencia (solo queda IPAP/Presión)
            colEpap.style.display = "none";
            colFrecuencia.style.display = "none";
            epapInput.value = "";
            frecuenciaInput.value = "";
        }
    }

    function calcularPorcentaje() {
            const b = parseFloat(basalInput.value) || 0;
            const r = parseFloat(residualInput.value) || 0;
            
            // Limpiar clases de color previas
            porcentajeOutput.classList.remove('text-success', 'text-danger', 'text-warning');

            if (b > 0) {
                const resultado = ((b - r) / b) * 100;
                porcentajeOutput.value = resultado.toFixed(1) + "%";

                // Lógica de colores según el resultado
                if (resultado < 0) {
                    // El paciente empeoró (Valor negativo)
                    porcentajeOutput.classList.add('text-danger');
                } else if (resultado >= 90) {
                    // Excelente corrección
                    porcentajeOutput.classList.add('text-success');
                } else if (resultado >= 50) {
                    // Corrección regular/buena
                    porcentajeOutput.classList.add('text-warning');
                } else {
                    // Poca corrección
                    porcentajeOutput.classList.add('text-danger');
                }
            } else {
                porcentajeOutput.value = "0%";
            }
        }

    // Eventos
    modoVentilatorio.addEventListener("change", toggleCampos);
    basalInput.addEventListener("input", calcularPorcentaje);
    residualInput.addEventListener("input", calcularPorcentaje);

    // Ejecución inicial
    toggleCampos();
    calcularPorcentaje();
});