/* ============================================
   Job Tracker — API Client
   Edit API_BASE to point at your deployed backend.
   ============================================ */
const API_BASE = "https://job-tracker-ekk2.onrender.com/api";

const Storage = {
  getAccess: () => localStorage.getItem("jt_access"),
  getRefresh: () => localStorage.getItem("jt_refresh"),
  setTokens: (access, refresh) => {
    localStorage.setItem("jt_access", access);
    if (refresh) localStorage.setItem("jt_refresh", refresh);
  },
  clear: () => {
    localStorage.removeItem("jt_access");
    localStorage.removeItem("jt_refresh");
  },
};

async function apiRequest(path, { method = "GET", body, auth = true, retry = true } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (auth) {
    const token = Storage.getAccess();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  let res;
  try {
    res = await fetch(`${API_BASE}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch (networkErr) {
    throw new ApiError("Can't reach the server. Check your connection and try again.", 0);
  }

  // Token expired — try refresh once
  if (res.status === 401 && auth && retry && Storage.getRefresh()) {
    const refreshed = await tryRefreshToken();
    if (refreshed) {
      return apiRequest(path, { method, body, auth, retry: false });
    }
    Storage.clear();
    window.location.href = "login.html";
    throw new ApiError("Session expired. Please log in again.", 401);
  }

  if (!res.ok) {
    let message = `Request failed (${res.status})`;
    try {
      const data = await res.json();
      message = extractErrorMessage(data) || message;
    } catch (_) {}
    throw new ApiError(message, res.status);
  }

  if (res.status === 204) return null;
  try {
    return await res.json();
  } catch (_) {
    return null;
  }
}

function extractErrorMessage(data) {
  if (typeof data === "string") return data;
  if (data.detail) return data.detail;
  if (data.non_field_errors) return data.non_field_errors.join(" ");
  const firstKey = Object.keys(data)[0];
  if (firstKey) {
    const val = data[firstKey];
    const text = Array.isArray(val) ? val.join(" ") : String(val);
    return `${firstKey}: ${text}`;
  }
  return null;
}

class ApiError extends Error {
  constructor(message, status) {
    super(message);
    this.status = status;
  }
}

async function tryRefreshToken() {
  try {
    const res = await fetch(`${API_BASE}/auth/token/refresh/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh: Storage.getRefresh() }),
    });
    if (!res.ok) return false;
    const data = await res.json();
    Storage.setTokens(data.access, data.refresh);
    return true;
  } catch (_) {
    return false;
  }
}

function requireAuth() {
  if (!Storage.getAccess()) {
    window.location.href = "login.html";
  }
}

function logout() {
  Storage.clear();
  window.location.href = "login.html";
}

const Api = {
  register: (payload) => apiRequest("/auth/register/", { method: "POST", body: payload, auth: false }),
  login: (payload) => apiRequest("/auth/login/", { method: "POST", body: payload, auth: false }),
  profile: () => apiRequest("/auth/profile/"),

  listApplications: (params = "") => apiRequest(`/applications/${params}`),
  getApplication: (id) => apiRequest(`/applications/${id}/`),
  createApplication: (payload) => apiRequest("/applications/", { method: "POST", body: payload }),
  updateApplication: (id, payload) => apiRequest(`/applications/${id}/`, { method: "PATCH", body: payload }),
  deleteApplication: (id) => apiRequest(`/applications/${id}/`, { method: "DELETE" }),

  listNotes: (appId) => apiRequest(`/applications/${appId}/notes/`),
  addNote: (appId, payload) => apiRequest(`/applications/${appId}/notes/`, { method: "POST", body: payload }),
  deleteNote: (appId, noteId) => apiRequest(`/applications/${appId}/notes/${noteId}/`, { method: "DELETE" }),

  dashboardSummary: () => apiRequest("/dashboard/summary/"),
};

function showToast(message, type = "success") {
  let toast = document.querySelector(".toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.className = "toast";
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.className = `toast show ${type === "error" ? "error" : ""}`;
  clearTimeout(toast._timer);
  toast._timer = setTimeout(() => toast.classList.remove("show"), 3200);
}

function showError(el, message) {
  if (!el) return;
  el.textContent = message;
  el.classList.add("show");
}
function hideError(el) {
  if (!el) return;
  el.classList.remove("show");
  el.textContent = "";
}
