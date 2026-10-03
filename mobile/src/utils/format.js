/**
 * How amounts and dates look on screen. Pure functions, so the tests can check them directly.
 */

/** 55000 -> "55,000 ₫", written the way docs/requirements.md writes amounts. */
export function formatDong(amount) {
  const value = Math.round(Math.abs(Number(amount)));
  if (!Number.isFinite(value)) {
    return '0 ₫';
  }
  return `${String(value).replace(/\B(?=(\d{3})+(?!\d))/g, ',')} ₫`;
}

/** Money spent shows as "−55,000 ₫", money received as "+4,000,000 ₫". */
export function formatAmount(amount, kind) {
  return `${kind === 'income' ? '+' : '−'}${formatDong(amount)}`;
}

/** "2026-09-28" -> "28/09/2026". */
export function formatDate(isoDate) {
  const [year, month, day] = String(isoDate ?? '').split('-');
  return year && month && day ? `${day}/${month}/${year}` : '';
}
