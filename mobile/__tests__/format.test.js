/**
 * How amounts and dates look on /: the month's totals (US04) and the list (US05).
 */

import {
  formatAmount,
  formatDate,
  formatDong,
  formatMonth,
  formatSigned,
} from '../src/utils/format';

describe('formatDong', () => {
  test('separates thousands with commas, as the requirements do', () => {
    expect(formatDong(55000)).toBe('55,000 ₫');
    expect(formatDong(4000000)).toBe('4,000,000 ₫');
    expect(formatDong(999)).toBe('999 ₫');
  });

  test('does not break on missing values', () => {
    expect(formatDong(undefined)).toBe('0 ₫');
    expect(formatDong('abc')).toBe('0 ₫');
  });
});

describe('formatDong in the chosen language (US11)', () => {
  test('groups thousands as the language writes them: dots in Vietnamese', () => {
    expect(formatDong(55000, 'vi')).toBe('55.000 ₫');
    expect(formatDong(4000000, 'vi')).toBe('4.000.000 ₫');
  });

  test('falls back to English commas for a language with no dictionary', () => {
    expect(formatDong(55000, 'zz')).toBe('55,000 ₫');
  });
});

describe('formatAmount', () => {
  test('money spent carries a minus sign', () => {
    expect(formatAmount(55000, 'expense')).toBe('−55,000 ₫');
  });

  test('money received carries a plus sign', () => {
    expect(formatAmount(4000000, 'income')).toBe('+4,000,000 ₫');
  });

  test('follows the chosen language', () => {
    expect(formatAmount(55000, 'expense', 'vi')).toBe('−55.000 ₫');
  });
});

describe('formatDate', () => {
  test('shows the day first, as dates are written in Vietnam', () => {
    expect(formatDate('2026-09-28')).toBe('28/09/2026');
  });

  test('gives an empty string when there is no date', () => {
    expect(formatDate(null)).toBe('');
    expect(formatDate('')).toBe('');
  });
});

describe('formatSigned', () => {
  test('shows what is left as it is', () => {
    expect(formatSigned(1069000)).toBe('1,069,000 ₫');
    expect(formatSigned(0)).toBe('0 ₫');
  });

  test('puts a minus sign before more spent than received', () => {
    expect(formatSigned(-120000)).toBe('−120,000 ₫');
    expect(formatSigned(-120000, 'vi')).toBe('−120.000 ₫');
  });
});

describe('formatMonth', () => {
  test('writes the month as the requirements do', () => {
    expect(formatMonth('2026-10')).toBe('10/2026');
  });

  test('gives an empty string when there is no month', () => {
    expect(formatMonth(undefined)).toBe('');
  });
});
