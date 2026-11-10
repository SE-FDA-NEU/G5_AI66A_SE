/**
 * Light and dark (US19): the same colours exist in both palettes, and the choice resolves as the
 * menu says.
 */

import { palettes, resolveScheme, THEME_CHOICES } from '../src/theme';

test('both palettes name the same colours', () => {
  expect(Object.keys(palettes.dark).sort()).toEqual(Object.keys(palettes.light).sort());
});

test.each([
  ['system', 'dark', 'dark'],
  ['system', 'light', 'light'],
  ['system', null, 'light'],
  ['light', 'dark', 'light'],
  ['dark', 'light', 'dark'],
])('choice %s on a %s device gives %s', (choice, device, expected) => {
  expect(resolveScheme(choice, device)).toBe(expected);
});

test('the menu offers device, light and dark', () => {
  expect(THEME_CHOICES).toEqual(['system', 'light', 'dark']);
});
