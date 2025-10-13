document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const doctorSelect = document.getElementById("doctor");
  const dateInput = document.getElementById("appointmentDate");
  const timeSelect = document.getElementById("appointmentTime");
  const submitButton = form.querySelector('button[type="submit"]');

  form.addEventListener("submit", (event) => {
    event.preventDefault();

    removeAlerts();
    [doctorSelect, dateInput, timeSelect].forEach(input => input.classList.remove("is-invalid"));

    let isValid = true;

    if (!doctorSelect.value) {
      doctorSelect.classList.add("is-invalid");
      isValid = false;
    }

    if (!dateInput.value) {
      dateInput.classList.add("is-invalid");
      isValid = false;
    }

    if (!timeSelect.value) {
      timeSelect.classList.add("is-invalid");
      isValid = false;
    }

    if (!isValid) {
      showAlert("Por favor completá todos los campos correctamente.", "danger");
      return;
    }

    disableSubmit(true);

    setTimeout(() => {
      disableSubmit(false);

      const doctor = doctorSelect.options[doctorSelect.selectedIndex].text;
      const date = dateInput.value;
      const time = timeSelect.value;

      const newAppointment = {
        specialty: "Clínica General",
        doctor,
        date,
        time
      };

      const appointments = JSON.parse(localStorage.getItem("appointments")) || [];
      appointments.push(newAppointment);
      localStorage.setItem("appointments", JSON.stringify(appointments));

      showAlert(`Turno reservado con éxito para ${doctor} el ${date} a las ${time}.`, "success");

      setTimeout(() => {
        window.location.href = "./my-appointments.html";
      }, 2000);
    }, 8000);
  });

  function showAlert(message, type) {
    const alertDiv = document.createElement("div");
    alertDiv.className = `alert alert-${type} mt-3`;
    alertDiv.id = "formAlert";
    alertDiv.textContent = message;
    form.appendChild(alertDiv);
  }

  function removeAlerts() {
    const existing = document.getElementById("formAlert");
    if (existing) existing.remove();
  }

  function disableSubmit(state) {
    submitButton.disabled = state;
    if (state) {
      submitButton.innerHTML = `
        <span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>
        Guardando...
      `;
      submitButton.classList.add("disabled", "opacity-75");
    } else {
      submitButton.innerHTML = `<i class="bi bi-calendar-check-fill me-2"></i> Confirmar Turno`;
      submitButton.classList.remove("disabled", "opacity-75");
    }
  }
});