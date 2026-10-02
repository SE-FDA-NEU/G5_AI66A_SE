/**
 * Whether someone is signed in, shared by the whole app, so that signing out in one place signs
 * out everywhere.
 */

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react';

import { api, clearToken, loadToken, saveToken } from '../api/client';
import { isExpired } from '../api/session';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  // 'loading' while the stored token is read, then 'signed-in' or 'signed-out'.
  const [status, setStatus] = useState('loading');
  const [user, setUser] = useState(null);

  useEffect(() => {
    let cancelled = false;

    async function restoreSession() {
      const token = await loadToken();
      if (!token || isExpired(token)) {
        // BR10: more than 7 days since sign-in, so the password is needed again.
        await clearToken();
        if (!cancelled) setStatus('signed-out');
        return;
      }
      // US02: within 7 days the app opens straight onto the overview, without a password.
      if (!cancelled) setStatus('signed-in');
      try {
        const profile = await api.me();
        if (!cancelled) setUser(profile);
      } catch (error) {
        if (error.status === 401) {
          await clearToken();
          if (!cancelled) {
            setUser(null);
            setStatus('signed-out');
          }
        }
        // With no network, stay signed in: the overview says there is no connection.
      }
    }

    restoreSession();
    return () => {
      cancelled = true;
    };
  }, []);

  const signIn = useCallback(async (email, password) => {
    const result = await api.login(email, password);
    await saveToken(result.access_token);
    setUser(result.user);
    setStatus('signed-in');
  }, []);

  const signOut = useCallback(async () => {
    await clearToken();
    setUser(null);
    setStatus('signed-out');
  }, []);

  const value = useMemo(
    () => ({ status, user, signIn, signOut }),
    [status, user, signIn, signOut],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used inside AuthProvider');
  }
  return context;
}
