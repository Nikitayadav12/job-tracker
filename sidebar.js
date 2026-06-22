/* ============================================
   Job Tracker — Sidebar injector
   Renders the sidebar nav + user chip on every app page.
   ============================================ */
const ICONS = {
  dashboard: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/></svg>',
  apps: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 7h16M4 12h16M4 17h10" stroke-linecap="round"/></svg>',
  logout: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4" stroke-linecap="round" stroke-linejoin="round"/><path d="M16 17l5-5-5-5M21 12H9" stroke-linecap="round" stroke-linejoin="round"/></svg>',
};

function renderSidebar(activePage) {
  const mount = document.getElementById("sidebarMount");
  if (!mount) return;

  mount.innerHTML = `
    <aside class="sidebar">
      <div class="brand">
        <div class="brand-mark">J</div>
        <div class="brand-name">Job Tracker</div>
      </div>
      <nav class="nav-section">
        <a href="dashboard.html" class="nav-link ${activePage === "dashboard" ? "active" : ""}">${ICONS.dashboard}<span>Dashboard</span></a>
        <a href="applications.html" class="nav-link ${activePage === "applications" ? "active" : ""}">${ICONS.apps}<span>Applications</span></a>
      </nav>
      <div class="sidebar-footer">
        <div class="user-chip" id="userChip">
          <div class="user-avatar" id="userAvatar">…</div>
          <div>
            <div class="user-name" id="userName">Loading…</div>
            <div class="user-email" id="userEmail"></div>
          </div>
        </div>
        <a href="#" class="nav-link" id="logoutBtn">${ICONS.logout}<span>Log out</span></a>
      </div>
    </aside>
  `;

  document.getElementById("logoutBtn").addEventListener("click", (e) => {
    e.preventDefault();
    logout();
  });

  loadUserChip();
}

async function loadUserChip() {
  try {
    const user = await Api.profile();
    const name = user.username || user.email;
    const initials = (user.username ? user.username[0] : user.email[0]).toUpperCase();
    document.getElementById("userAvatar").textContent = initials;
    document.getElementById("userName").textContent = name;
    document.getElementById("userEmail").textContent = user.email;
  } catch (err) {
    document.getElementById("userName").textContent = "Account";
  }
}