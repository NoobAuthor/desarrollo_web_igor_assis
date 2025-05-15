const regionesComunas = {
  Metropolitana: ["Santiago", "Providencia", "Ñuñoa"],
  Valparaíso: ["Valparaíso", "Viña del Mar"],
};

document.addEventListener("DOMContentLoaded", () => {
  // Prellenar fechas
  const ahora = new Date();
  const inicio = ahora.toISOString().slice(0, 16);
  document.getElementById("inicio").value = inicio;
  const termino = new Date(ahora.getTime() + 3 * 60 * 60 * 1000)
    .toISOString()
    .slice(0, 16);
  document.getElementById("termino").value = termino;

  // Poblar regiones
  const regionSelect = document.getElementById("region");
  Object.keys(regionesComunas).forEach((r) => {
    const option = document.createElement("option");
    option.value = r;
    option.textContent = r;
    regionSelect.appendChild(option);
  });

  // Actualizar comunas
  regionSelect.addEventListener("change", () => {
    const comunaSelect = document.getElementById("comuna");
    comunaSelect.innerHTML = '<option value="">Seleccione</option>';
    if (regionSelect.value) {
      regionesComunas[regionSelect.value].forEach((c) => {
        const option = document.createElement("option");
        option.value = c;
        option.textContent = c;
        comunaSelect.appendChild(option);
      });
    }
  });

  // Contactar por
  document.querySelectorAll(".contactar-por").forEach((select) => {
    select.addEventListener("change", () => {
      const input = select.nextElementSibling;
      input.style.display = select.value ? "inline" : "none";
    });
  });

  let contactoCount = 1;
  document.getElementById("agregar-contacto").addEventListener("click", () => {
    if (contactoCount < 5) {
      const div = document.createElement("div");
      div.innerHTML = `
                <label>Contactar por: 
                    <select class="contactar-por">
                        <option value="">Seleccione</option>
                        <option value="whatsapp">WhatsApp</option>
                        <option value="telegram">Telegram</option>
                        <option value="x">X</option>
                        <option value="instagram">Instagram</option>
                        <option value="tiktok">TikTok</option>
                        <option value="otra">Otra</option>
                    </select>
                    <input type="text" class="contacto-id" style="display:none;" minlength="4" maxlength="50">
                </label>`;
      document.getElementById("contactos").appendChild(div);
      div
        .querySelector(".contactar-por")
        .addEventListener("change", function () {
          this.nextElementSibling.style.display = this.value
            ? "inline"
            : "none";
        });
      contactoCount++;
    }
  });

  // Tema otro
  document.getElementById("tema").addEventListener("change", function () {
    document.getElementById("tema-otro").style.display =
      this.value === "otro" ? "inline" : "none";
  });

  // Agregar fotos
  let fotoCount = 1;
  document.getElementById("agregar-foto").addEventListener("click", () => {
    if (fotoCount < 5) {
      const div = document.createElement("div");
      div.innerHTML =
        '<label>Foto: <input type="file" class="foto-input"></label>';
      document.getElementById("fotos").appendChild(div);
      fotoCount++;
    }
  });

  // Validaciones
  document.getElementById("formulario").addEventListener("submit", (e) => {
    e.preventDefault();
    let errores = [];

    if (!regionSelect.value) errores.push("Debe seleccionar una región.");
    if (!document.getElementById("comuna").value)
      errores.push("Debe seleccionar una comuna.");
    if (!document.getElementById("nombre").value)
      errores.push("El nombre es obligatorio.");
    const email = document.getElementById("email").value;
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))
      errores.push("Email inválido.");
    const celular = document.getElementById("celular").value;
    if (celular && !/^\+\d{1,3}\.\d{8}$/.test(celular))
      errores.push("Celular debe ser +NNN.NNNNNNNN.");
    document.querySelectorAll(".contactar-por").forEach((select, i) => {
      if (select.value) {
        const id = document.querySelectorAll(".contacto-id")[i].value;
        if (id.length < 4 || id.length > 50)
          errores.push("ID de contacto debe tener entre 4 y 50 caracteres.");
      }
    });
    const inicio = document.getElementById("inicio").value;
    const termino = document.getElementById("termino").value;
    if (!inicio) errores.push("Fecha de inicio es obligatoria.");
    if (termino && termino <= inicio)
      errores.push("Fecha de término debe ser mayor que la de inicio.");
    const tema = document.getElementById("tema").value;
    if (!tema) errores.push("Debe seleccionar un tema.");
    if (tema === "otro") {
      const otro = document.getElementById("tema-otro").value;
      if (otro.length < 3 || otro.length > 15)
        errores.push('Tema "otro" debe tener entre 3 y 15 caracteres.');
    }
    const fotos = document.querySelectorAll(".foto-input");
    if (!Array.from(fotos).some((f) => f.files.length > 0))
      errores.push("Debe subir al menos una foto.");

    if (errores.length > 0) {
      alert(errores.join("\n"));
    } else if (confirm("¿Está seguro que desea agregar esta actividad?")) {
      alert(
        "Hemos recibido su información, muchas gracias y suerte en su actividad",
      );
      window.location.href = "index.html";
    }
  });
});
