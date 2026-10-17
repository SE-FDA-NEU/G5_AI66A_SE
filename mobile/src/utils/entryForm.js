/**
 * Reading what a person types into the form on /transactions/new (US03). Pure functions, so the
 * tests can call them directly. The rules themselves (BR5, BR6, BR11) are the API's to check; these
 * only turn the text into what the API expects.
 */

const pad = (number) => String(number).padStart(2, '0');

/**
 * Today on this device, as YYYY-MM-DD. Read from the local clock, not from toISOString(), which
 * gives the date in UTC: before 07:00 in Vietnam that is still yesterday.
 */
export function todayIso(now = new Date()) {
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;
}

/** The day before `iso`, as YYYY-MM-DD. */
export function dayBefore(iso) {
  const [year, month, day] = iso.split('-').map(Number);
  return todayIso(new Date(year, month - 1, day - 1));
}

/**
 * The amount typed, as a whole number of dong; null when the field is empty.
 *
 * "55000", "55,000", "55.000" and "55 000" all mean 55000: people group thousands as their language
 * does. A minus sign is kept, so the API answers -20000 with BR5. Anything else, such as "55000.50"
 * or "abc", gives NaN: the form then shows the BR5 message without asking the API.
 */
export function parseAmount(text) {
  const typed = String(text ?? '').trim();
  if (typed === '') return null;
  if (/^-?\d+$/.test(typed) || /^-?\d{1,3}([.,\s]\d{3})+$/.test(typed)) {
    return Number(typed.replace(/[.,\s]/g, ''));
  }
  return Number.NaN;
}

/**
 * "13/11/2026" -> "2026-11-13", the way the API writes dates; null when it is not a real day.
 * Day first, as the app shows dates everywhere. A future day is a real day: BR11 is the API's.
 */
export function parseDateInput(text) {
  const match = String(text ?? '').trim().match(/^(\d{1,2})\/(\d{1,2})\/(\d{4})$/);
  if (!match) return null;
  const [day, month, year] = [Number(match[1]), Number(match[2]), Number(match[3])];
  const date = new Date(year, month - 1, day);
  const real =
    date.getFullYear() === year && date.getMonth() === month - 1 && date.getDate() === day;
  return real ? `${year}-${pad(month)}-${pad(day)}` : null;
}
