import axios from "axios";

const API_URL = (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000/api/v1").replace(/\/$/, "");

export const api = axios.create({
  baseURL: API_URL,
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

export const unwrap = (response) => response?.data?.data ?? response?.data ?? null;

export const unwrapList = (response) => {
  const data = unwrap(response);
  if (Array.isArray(data)) return data;
  if (Array.isArray(data?.items)) return data.items;
  if (Array.isArray(data?.results)) return data.results;
  if (Array.isArray(data?.data)) return data.data;
  return [];
};

export const apiError = (error) => {
  const detail = error?.response?.data?.detail;
  if (Array.isArray(detail)) return detail.map((x) => x?.msg || String(x)).join(", ");
  if (typeof detail === "string") return detail;
  return error?.response?.data?.message || error?.message || "Something went wrong.";
};

api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Do NOT log the user out for every 401. A protected business endpoint
    // may return 401/403 because of permissions or a backend rule.
    // Only the session check is authoritative for deciding that the
    // browser no longer has a valid login session.
    const requestUrl = error?.config?.url || "";
    const isSessionCheck = requestUrl === "/users/me";
    if (error?.response?.status === 401 && isSessionCheck && !window.location.pathname.startsWith("/login")) {
      window.dispatchEvent(new CustomEvent("stocksense:unauthorized"));
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: (payload) => api.post("/auth/login", payload),
  signup: (payload) => api.post("/auth/signup", payload),
  logout: () => api.post("/auth/logout"),
  me: () => api.get("/users/me"),
  updateMe: (payload) => api.patch("/users/me", payload),
  forgotPassword: (payload) => api.post("/auth/forgot-password", payload),
  resetPassword: (payload) => api.post("/auth/reset-password", payload),
};

export const dashboardApi = { summary: (params = {}) => api.get("/dashboard/summary", { params }) };

export const productApi = {
  list: (params = {}) => api.get("/products", { params }),
  get: (id) => api.get(`/products/${id}`),
  create: (payload) => api.post("/products", payload),
  update: (id, payload) => api.patch(`/products/${id}`, payload),
  remove: (id) => api.delete(`/products/${id}`),
  categories: (params = {}) => api.get("/categories", { params }),
  createCategory: (payload) => api.post("/categories", payload),
};

export const inventoryApi = { list: (params = {}) => api.get("/inventory", { params }) };

export const warehouseApi = {
  list: (params = {}) => api.get("/warehouses", { params }),
  get: (id) => api.get(`/warehouses/${id}`),
  create: (payload) => api.post("/warehouses", payload),
  update: (id, payload) => api.patch(`/warehouses/${id}`, payload),
  remove: (id) => api.delete(`/warehouses/${id}`),
};

export const locationApi = {
  list: (params = {}) => api.get("/locations", { params }),
  get: (id) => api.get(`/locations/${id}`),
  create: (payload) => api.post("/locations", payload),
  update: (id, payload) => api.patch(`/locations/${id}`, payload),
  remove: (id) => api.delete(`/locations/${id}`),
};

const operationResource = (resource) => ({
  list: (params = {}) => api.get(`/${resource}`, { params }),
  get: (id) => api.get(`/${resource}/${id}`),
  create: (payload) => api.post(`/${resource}`, payload),
  update: (id, payload) => api.patch(`/${resource}/${id}`, payload),
  validate: (id) => api.post(`/${resource}/${id}/validate`),
  cancel: (id) => api.post(`/${resource}/${id}/cancel`),
  remove: (id) => api.delete(`/${resource}/${id}`),
});

export const receiptApi = operationResource("receipts");
export const deliveryApi = operationResource("deliveries");
export const transferApi = operationResource("transfers");
export const adjustmentApi = operationResource("adjustments");
export const ledgerApi = { list: (params = {}) => api.get("/ledger", { params }) };

export default api;