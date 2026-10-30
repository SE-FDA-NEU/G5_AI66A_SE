/**
 * Looking up a text in the chosen language (US11). Pure functions, so the tests call them directly.
 */

import { strings } from './strings';

// Every language with a dictionary in strings.js, in the order the switch shows them.
export const LANGUAGES = Object.keys(strings);

// English by default: the acceptance criteria and docs/SETUP.md describe the English screens, so a
// first run looks exactly as they say, whatever language the device uses.
export const DEFAULT_LANGUAGE = 'en';

// What each language calls itself, read out by screen readers on the switch.
export const LANGUAGE_NAMES = Object.fromEntries(
  LANGUAGES.map((code) => [code, strings[code]['language.name']]),
);

export function isLanguage(value) {
  return LANGUAGES.includes(value);
}

/**
 * The text for `key` in `language`, with `{name}` placeholders filled from `params`.
 * A key missing in the chosen language falls back to English, and a key missing everywhere shows
 * itself, so a gap is visible on screen instead of blank.
 */
export function translate(language, key, params = {}) {
  const text = strings[language]?.[key] ?? strings[DEFAULT_LANGUAGE][key] ?? key;
  return text.replace(/\{(\w+)\}/g, (placeholder, name) =>
    name in params ? String(params[name]) : placeholder,
  );
}

/** True when the English dictionary has `key`, so every other language has it too. */
export function hasText(key) {
  return Object.prototype.hasOwnProperty.call(strings[DEFAULT_LANGUAGE], key);
}

// The API names every error with a `code` that never changes when its English sentence is
// reworded (docs/design.md, section 3). The app picks the message to show by that code, in the
// chosen language; matching the English sentence instead broke as soon as one word changed.
export const ERROR_KEYS = {
  incorrect_sign_in: 'error.incorrectSignIn',
  sign_in_again: 'error.signInAgain',
  email_taken: 'error.emailTaken',
  password_length: 'error.passwordLength',
  invalid_email: 'error.invalidEmail',
  amount_not_positive: 'error.amountNotPositive',
  amount_too_large: 'error.amountTooLarge',
  date_in_future: 'error.dateInFuture',
  unknown_category: 'error.unknownCategory',
  invalid_month: 'error.invalidMonth',
  invalid_year: 'error.invalidYear',
  year_in_future: 'error.yearInFuture',
  invalid_request: 'error.invalidRequest',
  entry_not_found: 'error.entryNotFound',
  debt_not_found: 'error.debtNotFound',
  already_settled: 'error.alreadySettled',
  person_length: 'error.personLength',
  due_before_start: 'error.dueBeforeStart',
  not_found: 'error.notFound',
  server_error: 'error.server',
};

/** The message under `key`, and its hint under `key.hint` when the dictionary has one. */
function withHint(key, t, params) {
  const hintKey = `${key}.hint`;
  return { message: t(key, params), hint: hasText(hintKey) ? t(hintKey, params) : null };
}

/**
 * What to show for a problem, in the chosen language: `{ message, hint }`, or null for none.
 *
 * A problem is either `{ key }`, a message of the screen itself such as "Enter your email and
 * password", or an error from src/api/client.js. Status 0 means no answer at all: no network, or
 * no server running. A code the app does not know yet shows the API's sentence as it came, with
 * general advice, rather than nothing.
 */
export function describeError(problem, t, baseUrl) {
  if (!problem) return null;
  if (problem.key) return withHint(problem.key, t);
  if (problem.status === 0) return withHint('error.cannotReach', t, { url: baseUrl });
  const key = ERROR_KEYS[problem.code];
  if (key) return withHint(key, t);
  return { message: problem.message || t('error.refused'), hint: t('error.refused.hint') };
}
