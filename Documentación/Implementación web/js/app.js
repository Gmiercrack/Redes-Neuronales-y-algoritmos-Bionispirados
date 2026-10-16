// ============================================================
// Lógica de Interfaz, Navegación, KaTeX y Temas de BioOptima
// ============================================================

document.addEventListener('DOMContentLoaded', () => {
  // 1. Inicialización de KaTeX para fórmulas matemáticas
  initKaTeX();

  // 2. Control de Tema Oscuro / Claro
  initThemeToggle();

  // 3. Menú móvil
  initMobileMenu();

  // 4. Scrollspy y Navegación Superior
  initScrollspy();

  // 5. Controlador de Pestañas (Tabs)
  initTabs();

  // 6. Inicializar Mapa Interactivo TSP
  if (typeof initMapaTSP === 'function') {
    initMapaTSP();
  }
});

/**
 * Renderiza de forma instantánea todas las fórmulas LaTeX usando KaTeX
 */
function initKaTeX() {
  if (typeof renderMathInElement === 'function') {
    renderMathInElement(document.body, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '$', right: '$', display: false },
        { left: '\\[', right: '\\]', display: true },
        { left: '\\(', right: '\\)', display: false }
      ],
      throwOnError: false
    });
  }
}

/**
 * Conmutador de Modo Oscuro / Modo Claro con persistencia en localStorage
 */
function initThemeToggle() {
  const themeBtn = document.getElementById('theme-toggle-btn');
  const themeIcon = document.getElementById('theme-toggle-icon');
  
  // Leer preferencia guardada o sistema
  const savedTheme = localStorage.getItem('biooptima-theme') || 
    (window.matchMedia('(prefers-color-scheme: light)').matches ? 'light' : 'dark');

  applyTheme(savedTheme);

  if (themeBtn) {
    themeBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme') || 'dark';
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      applyTheme(newTheme);
      localStorage.setItem('biooptima-theme', newTheme);
      window.dispatchEvent(new Event('themeChanged'));
    });
  }

  function applyTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    if (themeIcon) {
      themeIcon.innerHTML = theme === 'dark' 
        ? '<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"/><path d="M12 1v2m0 18v2M4.22 4.22l1.42 1.42m12.72 12.72l1.42 1.42M1 12h2m18 0h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/></svg>'
        : '<svg width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    }
  }
}

/**
 * Menú responsive para móviles
 */
function initMobileMenu() {
  const toggleBtn = document.querySelector('.menu-toggle');
  const navMenu = document.querySelector('.nav-menu');

  if (toggleBtn && navMenu) {
    toggleBtn.addEventListener('click', () => {
      navMenu.classList.toggle('open');
    });

    // Cerrar al hacer clic en un enlace
    navMenu.querySelectorAll('.nav-link').forEach(link => {
      link.addEventListener('click', () => {
        navMenu.classList.remove('open');
      });
    });
  }
}

/**
 * Ilumina la sección activa en la barra superior al hacer scroll
 */
function initScrollspy() {
  const sections = document.querySelectorAll('.content-section, .hero-section');
  const navLinks = document.querySelectorAll('.nav-link');

  window.addEventListener('scroll', () => {
    let currentId = '';
    const scrollPos = window.scrollY + 120;

    sections.forEach(sec => {
      const top = sec.offsetTop;
      const height = sec.offsetHeight;
      if (scrollPos >= top && scrollPos < top + height) {
        currentId = sec.getAttribute('id');
      }
    });

    navLinks.forEach(link => {
      link.classList.remove('active');
      const href = link.getAttribute('href');
      if (href === `#${currentId}`) {
        link.classList.add('active');
      }
    });
  }, { passive: true });
}

/**
 * Controlador de pestañas dinámicas
 */
function initTabs() {
  document.querySelectorAll('.tab-controls').forEach(ctrl => {
    const targetGroupId = ctrl.getAttribute('data-tab-group');
    const buttons = ctrl.querySelectorAll('.tab-btn');
    const contentGroup = document.querySelectorAll(`[data-tab-content-group="${targetGroupId}"]`);

    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        const targetTab = btn.getAttribute('data-tab');

        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');

        contentGroup.forEach(c => {
          if (c.getAttribute('data-tab-id') === targetTab) {
            c.classList.add('active');
          } else {
            c.classList.remove('active');
          }
        });
      });
    });
  });
}
