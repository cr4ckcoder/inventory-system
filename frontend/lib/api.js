export const API_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

// -------------------- AUTH --------------------
export async function signupUser(data) {
  const res = await fetch(`${API_URL}/users/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Signup failed");
  }
  return res.json();
}

export async function loginUser(credentials) {
  const res = await fetch(`${API_URL}/users/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(credentials),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Login failed");
  }
  return res.json();
}

// -------------------- GENERIC FETCH WRAPPER --------------------
export async function fetchWithAuth(endpoint, options = {}) {
  const token = typeof window !== "undefined" ? localStorage.getItem("token") : null;

  const headers = {
    "Content-Type": "application/json",
    ...(token && { Authorization: `Bearer ${token}` }),
    ...options.headers,
  };

  const res = await fetch(`${API_URL}${endpoint}`, { ...options, headers });

  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Request failed");
  }

  return res.json();
}

// -------------------- DASHBOARD DATA --------------------
export const getDashboardStats = () => fetchWithAuth("/dashboard/stats");

// -------------------- PRODUCTS --------------------
export const getProducts = () => fetchWithAuth("/products");
export const getProductById = (id) => fetchWithAuth(`/products/${id}`);
export const createProduct = (data) =>
  fetchWithAuth("/products", { method: "POST", body: JSON.stringify(data) });
export const updateProduct = (id, data) =>
  fetchWithAuth(`/products/${id}`, { method: "PUT", body: JSON.stringify(data) });
export const deleteProduct = (id) =>
  fetchWithAuth(`/products/${id}`, { method: "DELETE" });

// -------------------- INVENTORY --------------------
export const getInventory = () => fetchWithAuth("/inventory");
export const getTransfers = () => fetchWithAuth("/transfers");
export const getUsers = () => fetchWithAuth("/users");


// -------------------- CATEGORIES --------------------
export const getCategories = () => fetchWithAuth("/categories");
export const createCategory = (data) =>
  fetchWithAuth("/categories", { method: "POST", body: JSON.stringify(data) });