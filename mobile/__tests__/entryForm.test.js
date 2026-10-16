/**
 * What the form on /transactions/new sends to the API (US03).
 */

import { dayBefore, parseAmount, parseDateInput, todayIso } from '../src/utils/entryForm';

describe('parseAmount', () => {
  test('reads whole dong, with or without thousands separators', () => {
    expect(parseAmount('55000')).toBe(55000);
    expect(parseAmount('55,000')).toBe(55000);
    expect(parseAmount('55.000')).toBe(55000);
    expect(parseAmount('4 000 000')).toBe(4000000);
  });

  test('leaves an empty field empty, so the API answers it with BR5', () => {
    expect(parseAmount('')).toBeNull();
    expect(parseAmount('   ')).toBeNull();
  });

  test('keeps 0 and a minus sign, so the API answers them with BR5', () => {
    expect(parseAmount('0')).toBe(0);
    expect(parseAmount('-20000')).toBe(-20000);
  });

  test('refuses a fraction of a dong and anything that is not a number', () => {
    expect(parseAmount('55000.50')).toBeNaN();
    expect(parseAmount('55,0')).toBeNaN();
    expect(parseAmount('abc')).toBeNaN();
  });
});

describe('parseDateInput', () => {
  test('reads the day first, as the app shows dates', () => {
    expect(parseDateInput('13/11/2026')).toBe('2026-11-13');
    expect(parseDateInput('1/2/2026')).toBe('2026-02-01');
  });

  test('refuses a day that does not exist, or another way of writing it', () => {
    expect(parseDateInput('31/02/2026')).toBeNull();
    expect(parseDateInput('2026-11-13')).toBeNull();
    expect(parseDateInput('')).toBeNull();
  });

  test('accepts a future day: BR11 is for the API to answer', () => {
    expect(parseDateInput('01/01/2099')).toBe('2099-01-01');
  });
});

describe('todayIso and dayBefore', () => {
  test('read the local date, not the UTC one', () => {
    // 06:30 on 12/11/2026 in the device's own time zone.
    expect(todayIso(new Date(2026, 10, 12, 6, 30))).toBe('2026-11-12');
  });

  test('cross the start of a month and of a year', () => {
    expect(dayBefore('2026-11-01')).toBe('2026-10-31');
    expect(dayBefore('2027-01-01')).toBe('2026-12-31');
  });
});
