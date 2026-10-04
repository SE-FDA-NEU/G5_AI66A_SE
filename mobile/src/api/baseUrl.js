/**
 * Where the backend is. The first of these that applies wins:
 *
 * 1. EXPO_PUBLIC_API_URL from mobile/.env, when someone has set it by hand;
 * 2. in a browser, the machine the page came from, on port 8000;
 * 3. on a phone in Expo Go, the computer that served the app (the Metro address), on port 8000.
 *
 * Cases 2 and 3 need no configuration, which is why a fresh clone runs without a mobile/.env.
 */

import Constants from 'expo-constants';
import { Platform } from 'react-native';

export const BACKEND_PORT = 8000;

/**
 * A pure function, kept apart from Expo so the tests can call it directly.
 *
 * @param {object} where
 * @param {string} [where.envUrl]        the value of EXPO_PUBLIC_API_URL, if any
 * @param {string} [where.pageHostname]  in a browser, the host of the page, such as "localhost"
 * @param {string} [where.metroHostUri]  on a phone, the Metro address, such as "192.168.1.15:8081"
 */
export function deriveBaseUrl({ envUrl, pageHostname, metroHostUri } = {}) {
  if (envUrl && envUrl.trim()) {
    return envUrl.trim().replace(/\/+$/, '');
  }
  if (pageHostname) {
    return `http://${pageHostname}:${BACKEND_PORT}/api`;
  }
  if (metroHostUri) {
    // Drop Metro's port and keep the host. An IPv6 host is bracketed and has colons of its own.
    const host = metroHostUri.startsWith('[')
      ? metroHostUri.slice(0, metroHostUri.lastIndexOf(':'))
      : metroHostUri.split(':')[0];
    if (host) {
      return `http://${host}:${BACKEND_PORT}/api`;
    }
  }
  return `http://localhost:${BACKEND_PORT}/api`;
}

export function getBaseUrl() {
  const inBrowser = Platform.OS === 'web' && typeof window !== 'undefined';
  return deriveBaseUrl({
    envUrl: process.env.EXPO_PUBLIC_API_URL,
    pageHostname: inBrowser ? window.location.hostname : undefined,
    metroHostUri: Constants.expoConfig?.hostUri ?? Constants.expoGoConfig?.debuggerHost,
  });
}
