const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:7463";

export const api = {
  baseUrl: API_BASE_URL,

  async request(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    const config = {
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(url, config);
    return response;
  },

  async get(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: "GET" });
  },

  async post(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  async put(endpoint, data, options = {}) {
    return this.request(endpoint, {
      ...options,
      method: "PUT",
      body: JSON.stringify(data),
    });
  },

  async delete(endpoint, options = {}) {
    return this.request(endpoint, { ...options, method: "DELETE" });
  },
};

export default api;
