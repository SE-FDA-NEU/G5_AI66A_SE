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
  // A sentence for the welcome screen after signing out for a reason, such as a deleted account.
  const [notice, setNotice] = useState(null);

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

  // Both answer with a token: a new account is signed in at once, with no second sign-in (US01).
  const start = useCallback(async (result) => {
    await saveToken(result.access_token);
    setUser(result.user);
    setStatus('signed-in');
  }, []);

  const signIn = useCallback(
    async (email, password) => start(await api.login(email, password)),
    [start],
  );

  const signUp = useCallback(
    async (email, password) => start(await api.register(email, password)),
    [start],
  );

  // The account's email, read again once the server answers. When the app opened with no
  // connection, restoreSession could not read it, and the overview showed no address.
  const refreshUser = useCallback(async () => {
    try {
      setUser(await api.me());
    } catch {
      // Still unreachable, or signed out meanwhile: the overview already says which.
    }
  }, []);

  const signOut = useCallback(async () => {
    await clearToken();
    setUser(null);
    setStatus('signed-out');
  }, []);

  // US16: the profile screen saves, then every screen greets the new name at once.
  const updateProfile = useCallback(async (changes) => {
    const saved = await api.updateProfile(changes);
    setUser(saved);
    return saved;
  }, []);

  // US18, BR16: the server checks the email and password again; only then is the app signed out.
  const deleteAccount = useCallback(
    async (email, password) => {
      await api.deleteAccount(email, password);
      await signOut();
      setNotice('welcome.deleted');
    },
    [signOut],
  );

  const clearNotice = useCallback(() => setNotice(null), []);

  const value = useMemo(
    () => ({
      status,
      user,
      notice,
      signIn,
      signUp,
      signOut,
      refreshUser,
      updateProfile,
      deleteAccount,
      clearNotice,
    }),
    [
      status,
      user,
      notice,
      signIn,
      signUp,
      signOut,
      refreshUser,
      updateProfile,
      deleteAccount,
      clearNotice,
    ],
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
