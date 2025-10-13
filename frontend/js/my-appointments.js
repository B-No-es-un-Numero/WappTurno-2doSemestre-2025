document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("appointments-container");
    const appointments = JSON.parse(localStorage.getItem("appointments")) || [];
    container.innerHTML = "";

    appointments.forEach((appointment, index) => {
        const card = document.createElement("div");
        card.className = "col-12 col-md-8 mb-4";
        card.innerHTML = `
        <div class="card shadow-sm border-start border-primary border-4 h-100">
            <div class="card-body">
            <h5 class="card-title text-primary fw-bold">Turno Reservado</h5>
            <hr>
            <div class="row">
                <div class="col-md-6 mb-3">
                <strong><i class="bi bi-person-badge"></i> Especialista:</strong> ${appointment.doctor}
                </div>
                <div class="col-md-6 mb-3">
                <strong><i class="bi bi-activity"></i> Especialidad:</strong> ${appointment.specialty}
                </div>
                <div class="col-md-6 mb-3">
                <strong><i class="bi bi-calendar-event"></i> Fecha:</strong> ${appointment.date}
                </div>
                <div class="col-md-6 mb-3">
                <strong><i class="bi bi-clock"></i> Hora:</strong> ${appointment.time}
                </div>
                <div class="col-12">
                <strong><i class="bi bi-geo-alt"></i> Lugar:</strong> Hospital Central, Calle Falsa 123
                </div>
            </div>
            <div class="d-grid gap-2 d-md-flex justify-content-md-end mt-3">
                <button class="btn btn-outline-danger btn-sm cancel-btn" data-index="${index}">
                <i class="bi bi-x-circle me-1"></i> Cancelar Turno
                </button>
            </div>
            </div>
        </div>
        `;
        container.appendChild(card);
    });


    const finishedCard = document.createElement("div");
    finishedCard.className = "col-12 col-md-8 mb-4";
    finishedCard.innerHTML = `
    <div class="card shadow-sm border-start border-secondary border-4 h-100">
        <div class="card-body">
            <h5 class="card-title text-secondary fw-bold">Turno Finalizado</h5>
            <hr>
            <div class="row">
                <div class="col-md-6 mb-3">
                    <strong><i class="bi bi-person-badge"></i> Especialista:</strong> Dra. Ana Pérez
                </div>
                <div class="col-md-6 mb-3">
                    <strong><i class="bi bi-activity"></i> Especialidad:</strong> Odontología
                </div>
                <div class="col-md-6 mb-3">
                    <strong><i class="bi bi-calendar-event"></i> Fecha:</strong> 05 de Julio de 2025
                </div>
                <div class="col-md-6 mb-3">
                    <strong><i class="bi bi-clock"></i> Hora:</strong> 14:00 hs
                </div>
                <div class="col-12">
                    <strong><i class="bi bi-geo-alt"></i> Lugar:</strong> Clínica del Sol, Av. Siempre
                        Viva 742
                </div>
            </div>
            <div class="d-grid gap-2 d-md-flex justify-content-md-end mt-3">
                <a href="#" class="btn btn-outline-secondary btn-sm disabled"><i
                 class="bi bi-check-circle me-1"></i> Turno Finalizado</a>
            </div>
        </div>
    </div>
  `;
    container.appendChild(finishedCard);


    container.addEventListener("click", (e) => {
        if (e.target.closest(".cancel-btn")) {
            const button = e.target.closest(".cancel-btn");
            const index = button.dataset.index;

            if (confirm("¿Seguro que deseas cancelar este turno?")) {
                appointments.splice(index, 1);
                localStorage.setItem("appointments", JSON.stringify(appointments));
                showAlert("El turno ha sido cancelado correctamente.", "warning");
                setTimeout(() => location.reload(), 1500);
            }
        }
    });

    function showAlert(message, type) {
        const existing = document.getElementById("formAlert");
        if (existing) existing.remove();

        const alertDiv = document.createElement("div");
        alertDiv.className = `alert alert-${type} mt-3 text-center`;
        alertDiv.id = "formAlert";
        alertDiv.innerHTML = `<i class="bi bi-info-circle"></i> ${message}`;
        container.prepend(alertDiv);
    }
});