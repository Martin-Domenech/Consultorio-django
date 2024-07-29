function confirmarEliminarPaciente(event, pacienteId) {
    event.preventDefault();
    if (confirm("¿Estás seguro de que deseas eliminar este paciente?")) {
        document.getElementById('eliminar-form-' + pacienteId).submit();
    } else {
        return false;
    }
}

function confirmarEliminarHC(event, hcid) {
    event.preventDefault();
    if (confirm("¿Estás seguro de que deseas eliminar esta evolución?")) {
        document.getElementById('eliminar-form-' + hcid).submit();
    } else {
        return false;
    }
}