document.addEventListener('DOMContentLoaded', () => {
  const checkboxes = document.querySelectorAll('input[name="familia"]');
  const detalles = document.querySelectorAll('.familia-detalle');

  function mostrarDetalle() {
    let familiaId = null;
    checkboxes.forEach(cb => {
      if (cb.checked) familiaId = cb.value;
    });
    detalles.forEach(det => {
      if (det.getAttribute('data-familia-id') === familiaId) {
        det.style.display = '';
      } else {
        det.style.display = 'none';
      }
    });
  }

  checkboxes.forEach(cb => {
    cb.addEventListener('change', () => {
      // Solo permite un checkbox activo a la vez
      checkboxes.forEach(c => c.checked = false);
      cb.checked = true;
      mostrarDetalle();
    });
  });

  mostrarDetalle(); // Inicializa al cargar
});