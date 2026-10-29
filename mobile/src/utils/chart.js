/**
 * The numbers behind the charts on /stats (US10, US12). Pure functions, so the tests can call them
 * directly; the components only draw what these return.
 */

import { DEFAULT_LANGUAGE, translate } from '../i18n/translate';

/**
 * How tall a bar is, in pixels, when the tallest bar is `height`: never negative, and a value
 * above 0 always gets at least 2 pixels, so a small month is still visible next to a big one.
 */
export function barHeight(value, max, height) {
  if (!(max > 0) || !(value > 0)) return 0;
  return Math.max(2, Math.round((value / max) * height));
}

/** The largest value of a chart, so every bar is scaled against the same number. */
export function chartMax(periods) {
  return Math.max(0, ...periods.flatMap((period) => [period.spending, period.income]));
}

/**
 * An amount short enough to sit on top of a bar: 2,931,000 is "2.9M" in English and "2,9 tr" in
 * Vietnamese, 55,000 is "55K" or "55 N". The full amount is always written next to the chart too.
 */
export function shortAmount(amount, language = DEFAULT_LANGUAGE) {
  const value = Math.abs(Number(amount)) || 0;
  const steps = [
    [1e9, 'number.billion'],
    [1e6, 'number.million'],
    [1e3, 'number.thousand'],
  ];
  for (const [size, key] of steps) {
    if (value >= size) {
      const scaled = Math.round((value / size) * 10) / 10;
      const digits = String(scaled).replace('.', translate(language, 'number.decimal'));
      return `${digits}${translate(language, key)}`;
    }
  }
  return String(value);
}

/**
 * What the axis says under a bar: "Oct" or "T10" for the period "2026-10", and "2026" for a year.
 */
export function periodLabel(period, language = DEFAULT_LANGUAGE) {
  const [year, month] = String(period ?? '').split('-');
  if (!month) return year ?? '';
  const names = translate(language, 'chart.months').split(',');
  return names[Number(month) - 1] ?? month;
}

/**
 * The month to break down when a year is shown: this month in this year, else the month that cost
 * the most, else December. `today` is "YYYY-MM-DD", from utils/entryForm.js.
 */
export function defaultMonth(year, busiest, today) {
  const thisMonth = today.slice(0, 7);
  if (thisMonth.startsWith(`${year}-`)) return thisMonth;
  return busiest ?? `${year}-12`;
}
