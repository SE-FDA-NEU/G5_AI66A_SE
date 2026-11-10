/**
 * Colours and spacing shared by every screen, in a light and a dark palette (US19). Change a
 * colour here, never inside a screen.
 *
 * A screen never imports a colour directly. It builds its styles from the palette in use:
 *
 *   const makeStyles = (colors) => StyleSheet.create({ ... colors.primary ... });
 *   function MyScreen() { const styles = useStyles(makeStyles); ... }
 *
 * and asks useTheme() for a colour it passes as a prop, such as a spinner's. Switching between
 * light and dark then redraws every screen at once, with nothing to reload.
 */

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { useColorScheme } from 'react-native';

import * as storage from './api/storage';

const light = {
  primary: '#0E6B57',
  primaryLight: '#E3F0EC',
  received: '#0E6B57',
  // Money received in a chart, lighter than spent, so spending reads first.
  receivedSoft: '#8CC3B3',
  spent: '#A2452C',
  danger: '#A2452C',
  dangerLight: '#F7E4DF',
  // Due today or tomorrow: not late yet, but soon (BR14).
  warning: '#8A5A00',
  warningLight: '#FBEFD5',

  background: '#F4F6F5',
  surface: '#FFFFFF',
  border: '#DCE3E0',

  text: '#17211E',
  textMuted: '#5F6F68',
  // Text on a filled button: on primary, on danger.
  textInverse: '#FFFFFF',

  // The top bar of every screen, and the language switch in it.
  header: '#0E6B57',
  headerText: '#FFFFFF',
  // Behind the menu and the dialogs.
  scrim: 'rgba(10, 20, 17, 0.45)',
};

// Every pair used for text keeps a contrast of at least 4.5:1, as in the light palette.
const dark = {
  primary: '#5CC6A5',
  primaryLight: '#17372E',
  received: '#5CC6A5',
  receivedSoft: '#2F6E5D',
  spent: '#F08A6E',
  danger: '#F08A6E',
  dangerLight: '#3B211A',
  warning: '#E8B95A',
  warningLight: '#3A2E12',

  background: '#0F1513',
  surface: '#18211E',
  border: '#2B3833',

  text: '#E6EEEA',
  textMuted: '#9DAEA7',
  textInverse: '#0B1D17',

  header: '#123D33',
  headerText: '#E6EEEA',
  scrim: 'rgba(0, 0, 0, 0.6)',
};

export const palettes = { light, dark };

// The light palette, for code that runs outside a screen, such as the tests.
export const colors = light;

export const spacing = {
  xs: 4,
  sm: 8,
  md: 16,
  lg: 24,
  xl: 32,
};

export const radius = {
  sm: 6,
  md: 12,
};

// "system" follows the phone or the browser; "light" and "dark" are fixed by the person.
export const THEME_CHOICES = ['system', 'light', 'dark'];
const THEME_KEY = 'g5_theme';

/** The palette name in use for a choice, given what the device prefers. Pure, for the tests. */
export function resolveScheme(choice, deviceScheme) {
  if (choice === 'light' || choice === 'dark') return choice;
  return deviceScheme === 'dark' ? 'dark' : 'light';
}

const ThemeContext = createContext({
  choice: 'system',
  scheme: 'light',
  colors: light,
  setChoice: () => {},
});

export function ThemeProvider({ children }) {
  const deviceScheme = useColorScheme();
  const [choice, setChoiceState] = useState('system');

  // The choice made on an earlier visit, kept on the device like the language (US11).
  useEffect(() => {
    let cancelled = false;
    storage
      .getItem(THEME_KEY)
      .then((saved) => {
        if (!cancelled && THEME_CHOICES.includes(saved)) setChoiceState(saved);
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, []);

  const setChoice = useCallback((next) => {
    if (!THEME_CHOICES.includes(next)) return;
    setChoiceState(next);
    storage.setItem(THEME_KEY, next).catch(() => {});
  }, []);

  const scheme = resolveScheme(choice, deviceScheme);
  const value = useMemo(
    () => ({ choice, scheme, colors: palettes[scheme], setChoice }),
    [choice, scheme, setChoice],
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  return useContext(ThemeContext);
}

/** The styles a factory builds from the palette in use, built again only when it changes. */
export function useStyles(factory) {
  const { colors: palette } = useTheme();
  return useMemo(() => factory(palette), [factory, palette]);
}
