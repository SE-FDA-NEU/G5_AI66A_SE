/**
 * How amounts and dates look on screen. Pure functions, so the tests can check them directly.
 */

import { DEFAULT_LANGUAGE, translate } from '../i18n/translate';

/**
 * 55000 -> "55,000 ₫". Each dictionary says how its language groups thousands (US11): a comma in
 * English, as docs/requirements.md writes amounts, and a dot in Vietnamese, "55.000 ₫".
 */
export function formatDong(amount, language = DEFAULT_LANGUAGE) {
  const value = Math.round(Math.abs(Number(amount)));
  if (!Number.isFinite(value)) {
    return '0 ₫';
  }
  const separator = translate(language, 'number.thousands');
  return `${String(value).replace(/\B(?=(\d{3})+(?!\d))/g, separator)} ₫`;
}

/** Money spent shows as "−55,000 ₫", money received as "+4,000,000 ₫". */
export function formatAmount(amount, kind, language = DEFAULT_LANGUAGE) {
  return `${kind === 'income' ? '+' : '−'}${formatDong(amount, language)}`;
}

/** "2026-09-28" -> "28/09/2026": day first in every language, as the requirements write dates. */
export function formatDate(isoDate) {
  const [year, month, day] = String(isoDate ?? '').split('-');
  return year && month && day ? `${day}/${month}/${year}` : '';
}
