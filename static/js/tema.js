console.log("corriendo tema.js");

document.addEventListener('DOMContentLoaded', () => {
  const btnTema = document.getElementById('btn-toggle-theme');
  const iconoTema = document.getElementById('icono-tema');
  const body = document.body;

  function actualizarIcono(tema) {
    if (tema === 'dark') {
      iconoTema.classList.remove('bi-moon-stars-fill');
      iconoTema.classList.add('bi-sun-fill');

      const iconoMobile = document.getElementById('icono-tema-mobile');
      if (iconoMobile) {
        iconoMobile.classList.remove('bi-moon-stars-fill');
        iconoMobile.classList.add('bi-sun-fill');
      }
    } else {
      iconoTema.classList.remove('bi-sun-fill');
      iconoTema.classList.add('bi-moon-stars-fill');

      const iconoMobile = document.getElementById('icono-tema-mobile');
      if (iconoMobile) {
        iconoMobile.classList.remove('bi-sun-fill');
        iconoMobile.classList.add('bi-moon-stars-fill');
      }
    }
  }

  const temaGuardado = localStorage.getItem('tema') || 'light';
  body.setAttribute('data-bs-theme', temaGuardado);
  actualizarIcono(temaGuardado);

  function cambiarTema() {
    const temaActual = body.getAttribute('data-bs-theme');
    const nuevoTema = temaActual === 'light' ? 'dark' : 'light';

    console.log(`Cambiando tema de ${temaActual} a ${nuevoTema}`);

    body.setAttribute('data-bs-theme', nuevoTema);
    localStorage.setItem('tema', nuevoTema);
    actualizarIcono(nuevoTema);

    // Refrescar offcanvas para que tome estilos nuevos
    const offcanvas = document.getElementById('offcanvasSidebar');
    if (offcanvas && bootstrap) {
      const bsOffcanvas = bootstrap.Offcanvas.getInstance(offcanvas);
      if (bsOffcanvas && offcanvas.classList.contains('show')) {
        bsOffcanvas.hide();
        setTimeout(() => {
          bsOffcanvas.show();
        }, 200);
      }
    }
  }

  if (btnTema) btnTema.addEventListener('click', cambiarTema);

  document.addEventListener('click', (e) => {
    if (e.target.closest('#btn-toggle-theme-mobile')) {
      e.preventDefault();
      cambiarTema();
    }
  });
});
