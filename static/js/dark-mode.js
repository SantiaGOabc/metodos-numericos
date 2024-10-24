const darkModeToggle = document.getElementById('dark-mode-toggle');
const icon = darkModeToggle.querySelector('i');

// Verificar si el modo oscuro está habilitado en localStorage
const darkModeEnabled = localStorage.getItem('dark-mode') === 'enabled';

// Aplicar el modo oscuro si está habilitado
if (darkModeEnabled) {
    document.body.classList.add('dark-mode');
    darkModeToggle.classList.add('dark');
    icon.classList.remove('fa-moon');
    icon.classList.add('fa-sun');
    darkModeToggle.textContent = 'Cambiar tema';
    darkModeToggle.prepend(icon); // Asegurarse de que el ícono se mantenga al principio
}

// Función para alternar el modo oscuro
darkModeToggle.addEventListener('click', () => {
    document.body.classList.toggle('dark-mode');
    darkModeToggle.classList.toggle('dark');

    if (document.body.classList.contains('dark-mode')) {
        icon.classList.remove('fa-moon');
        icon.classList.add('fa-sun');
        darkModeToggle.textContent = 'claro';
        localStorage.setItem('dark-mode', 'enabled'); // Guardar estado en localStorage
    } else {
        icon.classList.remove('fa-sun');
        icon.classList.add('fa-moon');
        darkModeToggle.textContent = 'oscuro';
        localStorage.setItem('dark-mode', 'disabled'); // Guardar estado en localStorage
    }
    darkModeToggle.prepend(icon); // Mantener el ícono en su posición
});
