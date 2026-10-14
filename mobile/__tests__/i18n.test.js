/**
 * Language options (US11): every language has exactly the texts English has, placeholders are
 * filled, and every error the API names by its code is shown in the chosen language, with a hint.
 */

import { strings } from '../src/i18n/strings';
import {
  DEFAULT_LANGUAGE,
  ERROR_KEYS,
  LANGUAGE_NAMES,
  LANGUAGES,
  describeError,
  isLanguage,
  translate,
} from '../src/i18n/translate';

// A missing text counts as having no placeholders; the key test above names it.
const placeholders = (text) => (String(text ?? '').match(/\{\w+\}/g) ?? []).sort();
const OTHER_LANGUAGES = LANGUAGES.filter((code) => code !== 'en');
// A language code with no dictionary, for the fallback tests.
const UNKNOWN = 'zz';
const SEEDED_CATEGORIES = ['Food', 'Transport', 'Shopping', 'Bills', 'Entertainment', 'Health',
  'Education', 'Other', 'Salary', 'Bonus', 'Other income'];

describe('the dictionaries', () => {
  test('offer English and Vietnamese first, with English the default', () => {
    expect(LANGUAGES.slice(0, 2)).toEqual(['en', 'vi']);
    expect(DEFAULT_LANGUAGE).toBe('en');
  });

  test.each(OTHER_LANGUAGES)('%s has exactly the keys English has', (code) => {
    expect(Object.keys(strings[code]).sort()).toEqual(Object.keys(strings.en).sort());
  });

  test.each(OTHER_LANGUAGES)('%s uses the same placeholders as English', (code) => {
    for (const key of Object.keys(strings.en)) {
      expect([key, placeholders(strings[code][key])]).toEqual([key, placeholders(strings.en[key])]);
    }
  });

  test.each(LANGUAGES)('%s names itself and leaves no text empty', (code) => {
    expect(LANGUAGE_NAMES[code]).toBeTruthy();
    for (const [key, text] of Object.entries(strings[code])) {
      expect([key, typeof text === 'string' && text.length > 0]).toEqual([key, true]);
    }
  });

  test('name all 11 categories the seed script writes, in English as seeded (BR6, BR8)', () => {
    for (const name of SEEDED_CATEGORIES) {
      expect(strings.en[`category.${name}`]).toBe(name);
    }
  });

  test('keep the exact English sentences of the acceptance criteria', () => {
    expect(strings.en['error.incorrectSignIn']).toBe('Incorrect email or password');
    expect(strings.en['overview.noConnection']).toBe('No connection. Tap Refresh to try again');
    expect(strings.en['error.emailTaken']).toBe('This email is already registered');
    expect(strings.en['error.passwordLength']).toBe('Password must be 6 to 128 characters');
  });

  test('keep the exact Vietnamese texts of the US11 criteria', () => {
    expect(strings.vi['login.submit']).toBe('Đăng nhập');
    expect(strings.vi['login.password']).toBe('Mật khẩu');
    expect(strings.vi['error.incorrectSignIn']).toBe('Email hoặc mật khẩu không đúng');
    expect(strings.vi['category.Food']).toBe('Ăn uống');
  });
});

describe('translate', () => {
  test('starts in English', () => {
    expect(translate(DEFAULT_LANGUAGE, 'login.submit')).toBe('Sign in');
  });

  test('gives the text of the chosen language', () => {
    expect(translate('vi', 'login.submit')).toBe('Đăng nhập');
    expect(translate('vi', 'login.password')).toBe('Mật khẩu');
  });

  test('fills placeholders', () => {
    expect(translate('en', 'overview.count', { shown: 20, total: 25 })).toBe(
      'The 20 most recent of 25 entries',
    );
    expect(translate('vi', 'overview.count', { shown: 20, total: 25 })).toBe(
      '20 giao dịch gần nhất trong tổng số 25',
    );
  });

  test('falls back to English, then to the key itself, rather than showing nothing', () => {
    expect(translate(UNKNOWN, 'login.submit')).toBe('Sign in');
    expect(translate('vi', 'no.such.key')).toBe('no.such.key');
  });

  test('accepts only the languages it has a dictionary for', () => {
    for (const code of LANGUAGES) {
      expect(isLanguage(code)).toBe(true);
    }
    expect(isLanguage(UNKNOWN)).toBe(false);
    expect(isLanguage(null)).toBe(false);
  });
});

describe('describeError', () => {
  const vi = (key, params) => translate('vi', key, params);
  const en = (key, params) => translate('en', key, params);
  const URL = 'http://localhost:8000/api';

  test('shows the BR3 sentence in the chosen language, picked by its code', () => {
    const error = { status: 401, code: 'incorrect_sign_in', message: 'Incorrect email or password' };
    expect(describeError(error, vi, URL).message).toBe('Email hoặc mật khẩu không đúng');
    expect(describeError(error, en, URL).message).toBe('Incorrect email or password');
  });

  test('follows the code, not the English sentence, so rewording the API changes nothing', () => {
    const error = { status: 422, code: 'date_in_future', message: 'Some newer wording' };
    expect(describeError(error, en, URL).message).toBe('The date cannot be in the future');
  });

  test.each(Object.entries(ERROR_KEYS))('%s has a message and a hint in every language', (code, key) => {
    for (const language of LANGUAGES) {
      const shown = describeError({ status: 400, code }, (k, p) => translate(language, k, p), URL);
      expect([code, language, shown.message]).toEqual([code, language, strings[language][key]]);
      expect([code, language, Boolean(shown.hint)]).toEqual([code, language, true]);
    }
  });

  test('names the server address and says what to do when there was no answer at all', () => {
    const shown = describeError({ status: 0, message: '' }, vi, URL);
    expect(shown.message).toBe('Không kết nối được máy chủ tại http://localhost:8000/api');
    expect(shown.hint).toContain('docs/SETUP.md');
  });

  test('shows a message of the screen itself, with its hint when it has one', () => {
    expect(describeError({ key: 'login.missing' }, en, URL)).toEqual({
      message: 'Enter your email and password',
      hint: null,
    });
  });

  test('shows a sentence with an unknown code as the API sent it, with general advice', () => {
    const shown = describeError({ status: 418, code: 'teapot', message: 'I am a teapot' }, en, URL);
    expect(shown.message).toBe('I am a teapot');
    expect(shown.hint).toBe(strings.en['error.refused.hint']);
  });

  test('never shows a bare status such as "Error 422"', () => {
    const shown = describeError({ status: 422, code: null, message: '' }, en, URL);
    expect(shown.message).toBe('The server refused this request');
  });

  test('shows nothing when there is no error', () => {
    expect(describeError(null, en, '')).toBeNull();
  });
});
