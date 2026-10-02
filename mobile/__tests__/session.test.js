/**
 * BR10 on the device: within 7 days of sign-in the stored token is still good; after that the
 * app asks for the password again.
 */

import { isExpired, tokenExpiry } from '../src/api/session';

function tokenExpiringAt(date) {
  const encode = (value) =>
    Buffer.from(JSON.stringify(value)).toString('base64url');
  return `${encode({ alg: 'HS256', typ: 'JWT' })}.${encode({
    sub: '1',
    exp: Math.floor(date.getTime() / 1000),
  })}.signature`;
}

const signedIn = new Date('2026-09-12T21:00:00Z');
const sevenDaysLater = new Date('2026-09-19T21:00:00Z');

describe('tokenExpiry', () => {
  test('reads the expiry the server put in the token', () => {
    expect(tokenExpiry(tokenExpiringAt(sevenDaysLater))).toEqual(sevenDaysLater);
  });

  test('gives null for something that is not a token', () => {
    expect(tokenExpiry('not-a-token')).toBeNull();
  });
});

describe('isExpired', () => {
  const token = tokenExpiringAt(sevenDaysLater);

  test('a token is good the moment it is issued', () => {
    expect(isExpired(token, signedIn)).toBe(false);
  });

  test('a token is still good one hour before its 7 days are up', () => {
    expect(isExpired(token, new Date('2026-09-19T20:00:00Z'))).toBe(false);
  });

  test('a token has expired one hour after its 7 days are up', () => {
    expect(isExpired(token, new Date('2026-09-19T22:00:00Z'))).toBe(true);
  });

  test('a token that cannot be read counts as expired', () => {
    expect(isExpired('not-a-token', signedIn)).toBe(true);
  });
});
