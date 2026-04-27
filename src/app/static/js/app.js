// Minimal client-side behavior: sidebar toggle on small screens.
(function () {
  const shell = document.querySelector('[data-app-shell]');
  const toggle = document.querySelector('[data-sidebar-toggle]');
  if (!shell || !toggle) return;
  toggle.addEventListener('click', () => shell.classList.toggle('is-open'));
  // Close when clicking a link (mobile)
  shell.querySelectorAll('.sidebar-link').forEach((a) => {
    a.addEventListener('click', () => shell.classList.remove('is-open'));
  });
})();
