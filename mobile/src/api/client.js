/**
 * Every call to the backend goes through this file. Screens never call fetch themselves, so a
 * change of address or of the sign-in scheme is made here and nowhere else.
 */

import { getBaseUrl } from './baseUrl';
import * as storage from './storage';

const BASE_URL = getBaseUrl();
const TOKEN_KEY = 'g5_access_token';

/**
 * An error the screens can act on. `status` is the HTTP status, or 0 when there was no answer;
 * `code` names the error, such as "date_in_future", and picks the message the screen shows.
 */
export class ApiError extends Error {
  constructor(status, message, code = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
  }
}

export function saveToken(token) {
  return storage.setItem(TOKEN_KEY, token);
}

export function loadToken() {
  return storage.getItem(TOKEN_KEY);
}

export function clearToken() {
  return storage.removeItem(TOKEN_KEY);
}

async function request(path, { method = 'GET', body, signedIn = true } = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (signedIn) {
    const token = await loadToken();
    if (token) headers.Authorization = `Bearer ${token}`;
  }

  let response;
  try {
    response = await fetch(`${BASE_URL}${path}`, {
      method,
      headers,
      body: body ? JSON.stringify(body) : undefined,
    });
  } catch {
    // fetch rejects, rather than answering, when there is no network or no server running.
    // The address is in the message so that a wrong one is easy to spot.
    throw new ApiError(0, `Cannot reach the server at ${BASE_URL}`, 'no_connection');
  }

  const payload = await response.json().catch(() => null);
  if (!response.ok) {
    // The API answers every error as {"detail": "<one sentence>", "code": "<what went wrong>"}.
    // An answer without that shape, such as a proxy's error page, counts as a server error.
    const code = payload?.code ?? (response.status >= 500 ? 'server_error' : null);
    throw new ApiError(response.status, payload?.detail ?? '', code);
  }
  return payload;
}

export const api = {
  baseUrl: BASE_URL,

  register: (email, password) =>
    request('/users', { method: 'POST', body: { email, password }, signedIn: false }),

  login: (email, password) =>
    request('/auth/login', { method: 'POST', body: { email, password }, signedIn: false }),

  me: () => request('/auth/me'),

  listRecent: (limit = 20) => request(`/transactions?limit=${limit}`),

  summary: () => request('/summary'),

  categories: () => request('/categories'),

  createEntry: (entry) => request('/transactions', { method: 'POST', body: entry }),

  getEntry: (id) => request(`/transactions/${id}`),

  correctEntry: (id, entry) => request(`/transactions/${id}`, { method: 'PATCH', body: entry }),

  removeEntry: (id) => request(`/transactions/${id}`, { method: 'DELETE' }),
};
