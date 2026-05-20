const botonMenuMovil = document.getElementById("boton-menu-movil");
const menuPrincipal = document.getElementById("menu-principal");

if (botonMenuMovil && menuPrincipal) {
  botonMenuMovil.addEventListener("click", () => {
    menuPrincipal.classList.toggle("abierto");
  });
}

const selectorPaquete = document.getElementById("selector-paquete");
const textoResumenPaquete = document.getElementById("texto-resumen-paquete");

if (selectorPaquete && textoResumenPaquete) {
  selectorPaquete.addEventListener("change", () => {
    const opcion = selectorPaquete.value;
    if (opcion === "sinergia") {
      textoResumenPaquete.textContent = "Se aplicó recomendación de paquete de actualización de componentes (descuento simulado del 8%).";
    } else if (opcion === "mantenimiento") {
      textoResumenPaquete.textContent = "Se aplicó recomendación de paquete con mantenimiento preventivo (descuento simulado del 5%).";
    } else {
      textoResumenPaquete.textContent = "No hay paquete aplicado actualmente.";
    }
  });
}

const formularioBuscadorServicios = document.getElementById("form-buscador-servicios");
const estadoAnalizando = document.getElementById("estado-analizando");

if (formularioBuscadorServicios && estadoAnalizando) {
  formularioBuscadorServicios.addEventListener("submit", () => {
    estadoAnalizando.hidden = false;
  });
}
