/**
 * The numbers behind the charts on /stats (US10, US12): bar heights, short amounts, axis labels
 * and the month broken down first.
 */

import {
  barHeight,
  chartMax,
  defaultMonth,
  lastMonths,
  periodLabel,
  shortAmount,
} from '../src/utils/chart';

describe('barHeight', () => {
  test('scales a value against the tallest bar', () => {
    expect(barHeight(3840000, 3840000, 160)).toBe(160);
    expect(barHeight(1920000, 3840000, 160)).toBe(80);
  });

  test('keeps a small value visible, at 2 pixels at least', () => {
    expect(barHeight(1000, 3840000, 160)).toBe(2);
  });

  test('draws nothing for 0, or when every value is 0', () => {
    expect(barHeight(0, 3840000, 160)).toBe(0);
    expect(barHeight(0, 0, 160)).toBe(0);
  });
});

test('chartMax takes the largest of money spent and received', () => {
  const periods = [
    { period: '2026-09', spending: 3030000, income: 4000000 },
    { period: '2026-10', spending: 2931000, income: 0 },
  ];
  expect(chartMax(periods)).toBe(4000000);
  expect(chartMax([])).toBe(0);
});

describe('shortAmount', () => {
  test('writes millions, thousands and billions in English', () => {
    expect(shortAmount(2931000)).toBe('2.9M');
    expect(shortAmount(55000)).toBe('55K');
    expect(shortAmount(1200000000)).toBe('1.2B');
    expect(shortAmount(900)).toBe('900');
  });

  test('uses a decimal comma and Vietnamese words in Vietnamese (US11)', () => {
    expect(shortAmount(2931000, 'vi')).toBe('2,9 tr');
    expect(shortAmount(55000, 'vi')).toBe('55 N');
  });
});

describe('periodLabel', () => {
  test('names a month in the chosen language', () => {
    expect(periodLabel('2026-10')).toBe('Oct');
    expect(periodLabel('2026-01', 'vi')).toBe('T1');
  });

  test('leaves a year as it is', () => {
    expect(periodLabel('2025')).toBe('2025');
  });
});

describe('defaultMonth', () => {
  test('is this month when this year is shown', () => {
    expect(defaultMonth(2026, '2026-04', '2026-10-24')).toBe('2026-10');
  });

  test('is the month that cost the most in an earlier year, else December', () => {
    expect(defaultMonth(2025, '2025-12', '2026-10-24')).toBe('2025-12');
    expect(defaultMonth(2024, null, '2026-10-24')).toBe('2024-12');
  });
});

describe('lastMonths', () => {
  const year = (y) =>
    Array.from({ length: 12 }, (_, i) => ({ period: `${y}-${String(i + 1).padStart(2, '0')}` }));

  test('keeps the six months up to this one, oldest first', () => {
    const months = lastMonths(year(2026), '2026-10-24', 6).map((month) => month.period);
    expect(months).toEqual(['2026-05', '2026-06', '2026-07', '2026-08', '2026-09', '2026-10']);
  });

  test('reaches back into last year early in the year', () => {
    const months = lastMonths([...year(2026), ...year(2025)], '2026-02-03', 6);
    expect(months.map((month) => month.period)).toEqual([
      '2025-09',
      '2025-10',
      '2025-11',
      '2025-12',
      '2026-01',
      '2026-02',
    ]);
  });
});
