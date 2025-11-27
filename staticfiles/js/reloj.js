
console.log("corriendo reloj");


function actualizarReloj() {
    const ahora = new Date();

    // Opciones para formatear fecha y hora
    const opciones = {
      weekday: 'long', year: 'numeric', month: 'long',
      day: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit',
      hour12: false, // formato 24h
      timeZoneName: 'short'
    };

    const fechaHoraFormateada = ahora.toLocaleString('es-ES', opciones);
    document.getElementById('reloj').textContent = fechaHoraFormateada;
  }

  actualizarReloj(); // Mostrar inmediatamente al cargar
  setInterval(actualizarReloj, 1000); // Actualizar cada segundo