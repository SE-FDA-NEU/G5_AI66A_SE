/**
 * The chosen language, shared by every screen and kept on the device between visits (US11).
 */

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';
import { Platform } from 'react-native';

import * as storage from '../api/storage';
import { DEFAULT_LANGUAGE, isLanguage, translate } from './translate';

const LANGUAGE_KEY = 'g5_language';

const LanguageContext = createContext(null);

export function LanguageProvider({ children }) {
  const [language, setLanguageState] = useState(DEFAULT_LANGUAGE);

  // Read the language chosen on an earlier visit. Until it arrives the app shows English.
  useEffect(() => {
    let cancelled = false;
    storage
      .getItem(LANGUAGE_KEY)
      .then((saved) => {
        if (!cancelled && isLanguage(saved)) setLanguageState(saved);
      })
      .catch(() => {});
    return () => {
      cancelled = true;
    };
  }, []);

  // In a browser, tell the page which language it is in, for screen readers and spell checks.
  useEffect(() => {
    if (Platform.OS === 'web' && typeof document !== 'undefined') {
      document.documentElement.lang = language;
    }
  }, [language]);

  const setLanguage = useCallback((next) => {
    if (!isLanguage(next)) return;
    setLanguageState(next);
    storage.setItem(LANGUAGE_KEY, next).catch(() => {});
  }, []);

  const t = useCallback((key, params) => translate(language, key, params), [language]);

  const value = useMemo(() => ({ language, setLanguage, t }), [language, setLanguage, t]);

  return <LanguageContext.Provider value={value}>{children}</LanguageContext.Provider>;
}

export function useLanguage() {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used inside LanguageProvider');
  }
  return context;
}
