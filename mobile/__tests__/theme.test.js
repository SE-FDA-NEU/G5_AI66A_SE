/**
 * Light and dark (US19): the same colours exist in both palettes, and the choice resolves as the
 * menu says. And the layout of /welcome follows the screen's shape (US15).
 */

import { palettes, resolveScheme, THEME_CHOICES } from '../src/theme';
import { welcomeLayout } from '../src/screens/WelcomeScreen';

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

test.each([
  [1280, 800, 'side'], // a laptop
  [844, 390, 'side'], // a phone held sideways
  [390, 844, 'stack'], // a phone held upright
  [700, 500, 'stack'], // wider than tall, but under 720 pixels
  [720, 720, 'stack'], // square
])('a %i x %i screen puts the choices %s', (width, height, layout) => {
  expect(welcomeLayout(width, height)).toBe(layout);
});
