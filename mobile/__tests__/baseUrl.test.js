/**
 * Where the app looks for the backend. A wrong address is the most common first-run failure,
 * so every case is pinned down here.
 */

import { deriveBaseUrl } from '../src/api/baseUrl';

describe('deriveBaseUrl', () => {
  test('uses EXPO_PUBLIC_API_URL when it is set by hand', () => {
    expect(
      deriveBaseUrl({ envUrl: 'http://10.0.0.5:8000/api', metroHostUri: '192.168.1.15:8081' }),
    ).toBe('http://10.0.0.5:8000/api');
  });

  test('drops a trailing slash, so paths never start with //', () => {
    expect(deriveBaseUrl({ envUrl: 'http://10.0.0.5:8000/api/' })).toBe(
      'http://10.0.0.5:8000/api',
    );
  });

  test('treats an empty or blank EXPO_PUBLIC_API_URL as not set', () => {
    expect(deriveBaseUrl({ envUrl: '   ', metroHostUri: '192.168.1.15:8081' })).toBe(
      'http://192.168.1.15:8000/api',
    );
  });

  test('in a browser, uses the machine the page came from', () => {
    expect(deriveBaseUrl({ pageHostname: 'localhost' })).toBe('http://localhost:8000/api');
  });

  test('on a phone, uses the computer that served the app', () => {
    expect(deriveBaseUrl({ metroHostUri: '192.168.1.15:8081' })).toBe(
      'http://192.168.1.15:8000/api',
    );
  });

  test('works on a phone hotspot address', () => {
    expect(deriveBaseUrl({ metroHostUri: '172.20.10.2:8081' })).toBe(
      'http://172.20.10.2:8000/api',
    );
  });

  test('keeps an IPv6 host whole', () => {
    expect(deriveBaseUrl({ metroHostUri: '[fe80::1]:8081' })).toBe('http://[fe80::1]:8000/api');
  });

  test('falls back to localhost when nothing else is known', () => {
    expect(deriveBaseUrl()).toBe('http://localhost:8000/api');
  });
});
