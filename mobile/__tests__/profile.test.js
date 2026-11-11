/**
 * How the app names a person and what the profile form sends (US16, BR15).
 */

import { displayName, initials, profileChanges } from '../src/utils/profile';

const MAI = { email: 'mai@example.com', full_name: null, nickname: null, phone: null, avatar: null };

describe('displayName', () => {
  test('the nickname first', () => {
    expect(displayName({ ...MAI, full_name: 'Nguyen Thi Mai', nickname: 'Mai' })).toBe('Mai');
  });

  test('then the full name', () => {
    expect(displayName({ ...MAI, full_name: 'Nguyen Thi Mai' })).toBe('Nguyen Thi Mai');
  });

  test('then the email, as before Sprint 5', () => {
    expect(displayName(MAI)).toBe('mai@example.com');
  });

  test('a name of spaces only counts as none', () => {
    expect(displayName({ ...MAI, nickname: '   ' })).toBe('mai@example.com');
  });

  test('nobody signed in reads as nothing', () => {
    expect(displayName(null)).toBe('');
  });
});

describe('initials', () => {
  test('first and last word of the name', () => {
    expect(initials({ ...MAI, full_name: 'nguyen thi mai' })).toBe('NM');
  });

  test('one word gives one letter', () => {
    expect(initials({ ...MAI, nickname: 'Mai' })).toBe('M');
  });

  test('no name: the first letter of the email', () => {
    expect(initials(MAI)).toBe('M');
  });
});

describe('profileChanges', () => {
  test('only what changed is sent', () => {
    const form = { full_name: 'Nguyen Thi Mai', nickname: '', phone: '', avatar: null };
    expect(profileChanges(MAI, form)).toEqual({ full_name: 'Nguyen Thi Mai' });
  });

  test('an emptied field is sent empty, so the server clears it', () => {
    const saved = { ...MAI, nickname: 'Mai' };
    const form = { full_name: '', nickname: '  ', phone: '', avatar: null };
    expect(profileChanges(saved, form)).toEqual({ nickname: '' });
  });

  test('removing the picture sends null', () => {
    const saved = { ...MAI, avatar: 'data:image/jpeg;base64,AAAA' };
    const form = { full_name: '', nickname: '', phone: '', avatar: null };
    expect(profileChanges(saved, form)).toEqual({ avatar: null });
  });

  test('nothing changed, nothing sent', () => {
    expect(profileChanges(MAI, { full_name: '', nickname: '', phone: '', avatar: null })).toEqual({});
  });
});
