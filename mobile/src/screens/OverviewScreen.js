/**
 * The overview at /: the signed-in account's 20 most recent entries, newest first (US05), in
 * the chosen language (US11).
 *
 * This is the walking skeleton: every row comes from GET /api/transactions, which reads the
 * transactions table. Nothing on this screen comes from an array in the code.
 */

import { useCallback, useEffect, useState } from 'react';
import {
  ActivityIndicator,
  FlatList,
  Platform,
  Pressable,
  RefreshControl,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { api } from '../api/client';
import EntryRow from '../components/EntryRow';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { describeError } from '../i18n/translate';
import { colors, radius, spacing } from '../theme';

export const RECENT_COUNT = 20;

export default function OverviewScreen() {
  const { user, signOut } = useAuth();
  const { t } = useLanguage();
  const [entries, setEntries] = useState([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  // Either { key } for "No connection. Tap Refresh to try again", or the error the API client
  // threw; translated when shown, like the errors on /login.
  const [message, setMessage] = useState(null);

  const load = useCallback(async () => {
    try {
      const page = await api.listRecent(RECENT_COUNT);
      setEntries(page.items);
      setTotal(page.total);
      setMessage(null);
    } catch (error) {
      if (error.status === 401) {
        // BR10: the sign-in has expired, so back to /login.
        await signOut();
        return;
      }
      // US05: keep whatever is already on screen and say why nothing changed.
      setMessage(error.status === 0 ? { key: 'overview.noConnection' } : error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [signOut]);

  useEffect(() => {
    load();
  }, [load]);

  function refresh() {
    setRefreshing(true);
    load();
  }

  const messageText = message?.key ? t(message.key) : describeError(message, t, api.baseUrl);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  return (
    <FlatList
      style={styles.screen}
      contentContainerStyle={styles.list}
      data={entries}
      keyExtractor={(entry) => String(entry.id)}
      renderItem={({ item }) => <EntryRow entry={item} />}
      initialNumToRender={RECENT_COUNT}
      // On a phone, pulling the list down refreshes it as well. A browser has no such gesture,
      // which is why the Refresh button exists.
      refreshControl={
        Platform.OS === 'web' ? undefined : (
          <RefreshControl refreshing={refreshing} onRefresh={refresh} />
        )
      }
      ListHeaderComponent={
        <View>
          <View style={styles.accountRow}>
            <Text style={styles.account}>{user?.email ?? ''}</Text>
            <Pressable onPress={signOut} accessibilityRole="button">
              <Text style={styles.link}>{t('overview.signOut')}</Text>
            </Pressable>
          </View>

          <View style={styles.titleRow}>
            <Text style={styles.count}>
              {total > 0 ? t('overview.count', { shown: entries.length, total }) : ' '}
            </Text>
            <Pressable
              style={[styles.refreshButton, refreshing && styles.refreshButtonBusy]}
              onPress={refresh}
              disabled={refreshing}
              accessibilityRole="button"
            >
              <Text style={styles.refreshText}>
                {refreshing ? t('overview.refreshing') : t('overview.refresh')}
              </Text>
            </Pressable>
          </View>

          {messageText ? (
            <Text style={styles.message} accessibilityRole="alert">
              {messageText}
            </Text>
          ) : null}
        </View>
      }
      ListEmptyComponent={
        message ? null : <Text style={styles.empty}>{t('overview.empty')}</Text>
      }
    />
  );
}

const styles = StyleSheet.create({
  screen: { backgroundColor: colors.background, flex: 1 },
  list: { alignSelf: 'center', maxWidth: 640, padding: spacing.md, width: '100%' },
  center: {
    alignItems: 'center',
    backgroundColor: colors.background,
    flex: 1,
    justifyContent: 'center',
  },
  accountRow: {
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.sm,
  },
  account: { color: colors.textMuted, fontSize: 14 },
  link: { color: colors.primary, fontSize: 14, fontWeight: '600' },
  titleRow: {
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.md,
  },
  count: { color: colors.text, flex: 1, fontSize: 16, fontWeight: '700' },
  refreshButton: {
    backgroundColor: colors.primary,
    borderRadius: radius.sm,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
  },
  refreshButtonBusy: { opacity: 0.6 },
  refreshText: { color: colors.textInverse, fontSize: 14, fontWeight: '600' },
  message: {
    backgroundColor: colors.dangerLight,
    borderRadius: radius.sm,
    color: colors.danger,
    marginBottom: spacing.md,
    padding: spacing.md,
  },
  empty: { color: colors.textMuted, marginTop: spacing.lg, textAlign: 'center' },
});
