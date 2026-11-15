/**
 * Category names and the search box on /categories (US17, BR17).
 */

import { strings } from '../src/i18n/strings';
import { translate } from '../src/i18n/translate';
import { categoryName, fold, matchesSearch } from '../src/utils/categories';

const vi = (key, params) => translate('vi', key, params);

describe('categoryName', () => {
  test('translates a shared category', () => {
    expect(categoryName({ name: 'Food', custom: false }, vi)).toBe(strings.vi['category.Food']);
  });

  test("shows an account's own category exactly as typed, in every language", () => {
    expect(categoryName({ name: 'Cà phê sáng', custom: true }, vi)).toBe('Cà phê sáng');
    expect(categoryName({ name: 'Food court', custom: true }, vi)).toBe('Food court');
  });

  test('shows nothing for no category', () => {
    expect(categoryName(null, vi)).toBe('');
  });
});

describe('the search', () => {
  test('ignores capitals, accents and the spaces around it', () => {
    expect(fold('  ĂN Uống ')).toBe('an uong');
    expect(fold('Đi lại')).toBe('di lai');
  });

  test.each([
    ['Ăn uống', 'an', true],
    ['Ăn uống', 'UỐNG', true],
    ['Đi lại', 'di', true],
    ['Cà phê', 'ca phe', true],
    ['Giáo dục', 'an', false],
    ['Mua sắm', '', true],
    ['Mua sắm', '   ', true],
  ])('%s against "%s" is %s', (name, query, expected) => {
    expect(matchesSearch(name, query)).toBe(expected);
  });
});
