/**
 * Reading the sign-in token on the device (BR10).
 *
 * The token carries the moment it expires, 7 days after sign-in. Reading that here lets the app
 * open straight onto the overview within those 7 days, even with no network, and ask for the
 * password once they are over. The server checks the same expiry on every request.
 */

function decodeBase64Url(segment) {
  const base64 = segment.replace(/-/g, '+').replace(/_/g, '/');
  const padded = base64.padEnd(Math.ceil(base64.length / 4) * 4, '=');
  return globalThis.atob(padded);
}

/** When the token expires, as a Date, or null if it cannot be read. */
export function tokenExpiry(token) {
  try {
    const claims = JSON.parse(decodeBase64Url(token.split('.')[1]));
    return typeof claims.exp === 'number' ? new Date(claims.exp * 1000) : null;
  } catch {
    return null;
  }
}

/** True once the token has expired, or when it cannot be read at all. */
export function isExpired(token, now = new Date()) {
  const expiry = tokenExpiry(token);
  return expiry === null || expiry <= now;
}
