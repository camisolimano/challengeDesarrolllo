document.addEventListener("DOMContentLoaded", function () {
    const dniButton = document.getElementById("searchDNIButton");
    const dniInput = document.getElementById("id_dni");
    const errorMessage = document.getElementById("errorMessage");

    dniButton.addEventListener("click", function () {
        const dni = dniInput.value.trim();
        const isValidDni = dni && /^[0-9]{7,8}$/.test(dni);
        const ph = window.posthog;
        if (ph && typeof ph.capture === "function") {
            ph.capture("sq_dni_search_clicked", {
                dni_length: dni,
                is_valid_format: isValidDni,
                client_id: "client_2",

            });
        }

        if (isValidDni) {
            errorMessage.style.display = "none";

            const url = `https://www.cuitonline.com/search.php?q=${dni}`;
            window.open(url, "_blank");
        } else {
            errorMessage.style.display = "block";
            errorMessage.textContent =
                "Por favor, ingresa un DNI válido (solo números, 7 u 8 dígitos).";

            if (ph && typeof ph.capture === "function") {
                ph.capture("sq_dni_invalid", {
                    dni_attempt: dni,
                });
            }
        }
    });
});
