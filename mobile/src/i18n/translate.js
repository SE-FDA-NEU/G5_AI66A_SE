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

// The API always answers in English, with the exact sentences of the acceptance criteria. The app
// shows each sentence it knows in the chosen language; any other sentence is shown as it came.
const API_SENTENCES = {
  'Incorrect email or password': 'error.incorrectSignIn',
  'Please sign in again': 'error.signInAgain',
};

/**
 * The text to show for an error from src/api/client.js, in the chosen language.
 * Status 0 means no answer at all: no network, or no server running.
 */
export function describeError(error, t, baseUrl) {
  if (!error) return null;
  if (error.status === 0) return t('error.cannotReach', { url: baseUrl });
  const key = API_SENTENCES[error.message];
  return key ? t(key) : error.message;
}
