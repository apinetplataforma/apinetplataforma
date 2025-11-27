console.log("corriendo notificaciones.js");

// Función para obtener cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Configura Axios para enviar cookies y token CSRF en POST
axios.defaults.withCredentials = true;
axios.defaults.headers.post['X-CSRFToken'] = csrftoken;

document.addEventListener('DOMContentLoaded', function () {
    const contenedor = document.getElementById('contenedor-notificaciones');
    const badge = document.getElementById('badge-unread');
    const offcanvas = document.getElementById('offcanvasNotifications');

    const apiBaseURL = '/api/notificaciones/';

    async function cargarNotificaciones() {
        try {
            const response = await axios.get(apiBaseURL, {
                headers: {
                    'Accept': 'application/json',
                }
            });

            const data = response.data;
            const noLeidas = data.filter(notif => !notif.leida);

            // Actualizar badge
            if (noLeidas.length > 0) {
                badge.style.display = 'inline-block';
                badge.textContent = noLeidas.length;
            } else {
                badge.style.display = 'none';
            }

            if (noLeidas.length === 0) {
                contenedor.innerHTML = `
                    <div class="text-center py-5">
                        <img src="/static/img/notificacion.png" width="150" class="opacity-75 mb-2" alt="No notificaciones">
                        <p class="text-muted">No tienes notificaciones pendientes</p>
                    </div>`;
                return;
            }

            let html = `<button class="btn btn-success btn-sm w-100 mb-3" id="btn-marcar-todo">
                <i class="bi bi-check2-all"></i> Marcar todas como leídas
            </button>`;

            html += '<ul class="list-group list-group-flush">';
            noLeidas.forEach(notif => {
                html += `
                <li class="list-group-item shadow-sm rounded d-flex justify-content-between align-items-start mb-2">
                    <div class="ms-2 me-auto">
                        <div class="fw-bold">${notif.titulo}</div>
                        <small>${notif.mensaje.length > 80 ? notif.mensaje.substring(0, 77) + '...' : notif.mensaje}</small><br>
                        <small class="text-muted">
                            <i class="bi bi-clock"></i> ${new Date(notif.created).toLocaleDateString('es-ES', { day: '2-digit', month: 'short', hour: '2-digit', minute: '2-digit' })}
                        </small>
                    </div>
                    <button class="btn btn-outline-primary btn-sm marcar-individual" data-id="${notif.id}">
                        <i class="bi bi-check2-square"></i>
                    </button>
                </li>`;
            });
            html += '</ul>';

            contenedor.innerHTML = html;

            document.getElementById('btn-marcar-todo').addEventListener('click', marcarTodasComoLeidas);

            document.querySelectorAll('.marcar-individual').forEach(btn => {
                btn.addEventListener('click', function () {
                    const id = this.dataset.id;
                    marcarComoLeida(id);
                });
            });

        } catch (error) {
            console.error('Error al cargar notificaciones:', error);
            contenedor.innerHTML = `<p class="text-danger">Error al cargar notificaciones</p>`;
            badge.style.display = 'none';
        }
    }

    async function marcarComoLeida(id) {
        try {
            await axios.post(`${apiBaseURL}${id}/marcar_leida/`, {}, {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                }
            });
            await cargarNotificaciones();
        } catch (error) {
            console.error('Error al marcar notificación como leída:', error);
        }
    }

    async function marcarTodasComoLeidas() {
        try {
            await axios.post(`${apiBaseURL}marcar_todas_leidas/`, {}, {
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json',
                }
            });
            await cargarNotificaciones();
        } catch (error) {
            console.error('Error al marcar todas como leídas:', error);
        }
    }

    offcanvas.addEventListener('show.bs.offcanvas', function () {
        cargarNotificaciones();
    });

    // Opcional cargar badge al inicio
    cargarNotificaciones();
});
