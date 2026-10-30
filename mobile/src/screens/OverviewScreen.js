/**
 * The overview at /: this month's income, spending and what is left (US04), then the 20 most
 * recent entries, newest first (US05), in the chosen language (US11).
 *
 * Everything comes from the database through GET /api/summary and GET /api/transactions; nothing
 * on this screen comes from an array in the code. The screen has four states (docs/ui.md,
 * section 2): loading the first time, an error with nothing to show, an empty month, and data.
 *
 * On a wide screen the page has two columns: the month, the button and the cards of
 * components/OverviewCards.js on the left, the list on the right, so the width is used instead of
 * left empty. On a phone it stays one column, the list under the month.
 */

import { useFocusEffect } from '@react-navigation/native';
import { useCallback, useState } from 'react';
import {
  ActivityIndicator,
  FlatList,
  Platform,
  Pressable,
  RefreshControl,
  StyleSheet,
  ScrollView,
  Text,
  useWindowDimensions,
  View,
} from 'react-native';

import { api } from '../api/client';
import EntryRow from '../components/EntryRow';
import ErrorMessage from '../components/ErrorMessage';
import MainLayout from '../components/MainLayout';
import MonthSummary from '../components/MonthSummary';
import OverviewCards from '../components/OverviewCards';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { describeError } from '../i18n/translate';
import { colors, radius, spacing } from '../theme';

export const RECENT_COUNT = 20;
// From this width the overview has two columns.
const TWO_COLUMNS = 900;

export default function OverviewScreen({ navigation }) {
  const { user, signOut, refreshUser } = useAuth();
  const { t } = useLanguage();
  const { width } = useWindowDimensions();
  // null until the first answer arrives; the loading and error states depend on it.
  const [summary, setSummary] = useState(null);
  const [entries, setEntries] = useState([]);
  const [total, setTotal] = useState(0);
  const [refreshing, setRefreshing] = useState(false);
  // Either { key } for "No connection. Tap Refresh to try again", or the error the API client
  // threw; translated when shown, like the errors on /login.
  const [message, setMessage] = useState(null);

  const load = useCallback(async () => {
    try {
      const [month, page] = await Promise.all([api.summary(), api.listRecent(RECENT_COUNT)]);
      setSummary(month);
      setEntries(page.items);
      setTotal(page.total);
      setMessage(null);
      if (!user) refreshUser();
    } catch (error) {
      if (error.status === 401) {
        // BR10: the sign-in has expired, so back to /login.
        await signOut();
        return;
      }
      // US05: keep whatever is already on screen and say why nothing changed.
      setMessage(error.status === 0 ? { key: 'overview.noConnection' } : error);
    } finally {
      setRefreshing(false);
    }
  }, [signOut, user, refreshUser]);

  // Load each time / comes into view, so an entry saved on /transactions/new is already counted.
  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  function refresh() {
    setRefreshing(true);
    load();
  }

  // Loading: the first answer has not arrived yet.
  if (summary === null && message === null) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
        <Text style={styles.centerText}>{t('overview.loading')}</Text>
      </View>
    );
  }

  // Error: the first load failed, so there is nothing to keep on screen. With no answer at all
  // the message names the server address and says what to start (docs/SETUP.md, section 4).
  if (summary === null) {
    const firstProblem = describeError(message.key ? { status: 0 } : message, t, api.baseUrl);
    return (
      <View style={styles.center}>
        <View style={styles.narrow}>
          <ErrorMessage problem={firstProblem} />
          <Pressable style={styles.primaryButton} onPress={refresh} accessibilityRole="button">
            <Text style={styles.primaryText}>{t('overview.tryAgain')}</Text>
          </Pressable>
        </View>
      </View>
    );
  }

  // Empty or data: the month summary decides which, from its count.
  const openEntry = (entry) => navigation.navigate('EditEntry', { id: entry.id });

  const top = (
    <View>
      <View style={styles.accountRow}>
        <Text style={styles.account}>{user?.email ?? ''}</Text>
        <Pressable onPress={signOut} accessibilityRole="button">
          <Text style={styles.link}>{t('overview.signOut')}</Text>
        </Pressable>
      </View>

      <ErrorMessage problem={describeError(message, t, api.baseUrl)} />

      <MonthSummary summary={summary} />

      <Pressable
        style={styles.primaryButton}
        onPress={() => navigation.navigate('NewEntry')}
        accessibilityRole="button"
      >
        <Text style={styles.primaryText}>+ {t('overview.add')}</Text>
      </Pressable>
    </View>
  );

  const titleRow = (
    <View style={styles.titleRow}>
      <Text style={styles.count}>
        {total > 0 ? t('overview.count', { shown: entries.length, total }) : t('overview.recent')}
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
  );

  const empty = <Text style={styles.empty}>{t('overview.empty')}</Text>;

  if (width >= TWO_COLUMNS) {
    return (
      <MainLayout current="Overview">
        <ScrollView style={styles.screen} contentContainerStyle={styles.wide}>
          <View style={styles.side}>
            {top}
            <OverviewCards navigation={navigation} />
          </View>
          <View style={styles.main}>
            {titleRow}
            {entries.length === 0
              ? empty
              : entries.map((entry) => (
                  <EntryRow key={entry.id} entry={entry} onPress={() => openEntry(entry)} />
                ))}
          </View>
        </ScrollView>
      </MainLayout>
    );
  }

  return (
    <MainLayout current="Overview">
      <FlatList
        style={styles.screen}
        contentContainerStyle={styles.list}
        data={entries}
        keyExtractor={(entry) => String(entry.id)}
        renderItem={({ item }) => <EntryRow entry={item} onPress={() => openEntry(item)} />}
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
            {top}
            {titleRow}
          </View>
        }
        ListEmptyComponent={empty}
      />
    </MainLayout>
  );
}

const styles = StyleSheet.create({
  screen: { backgroundColor: colors.background, flex: 1 },
  list: { alignSelf: 'center', maxWidth: 640, padding: spacing.md, width: '100%' },
  wide: {
    alignItems: 'flex-start',
    alignSelf: 'center',
    flexDirection: 'row',
    gap: spacing.lg,
    maxWidth: 1200,
    padding: spacing.md,
    width: '100%',
  },
  side: { width: 400 },
  main: { flex: 1, minWidth: 0 },
  center: {
    alignItems: 'center',
    backgroundColor: colors.background,
    flex: 1,
    justifyContent: 'center',
    padding: spacing.lg,
  },
  centerText: { color: colors.textMuted, fontSize: 15, marginTop: spacing.md },
  narrow: { maxWidth: 480, width: '100%' },
  accountRow: {
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.sm,
  },
  account: { color: colors.textMuted, fontSize: 14 },
  link: { color: colors.primary, fontSize: 14, fontWeight: '600' },
  primaryButton: {
    alignItems: 'center',
    backgroundColor: colors.primary,
    borderRadius: radius.sm,
    marginBottom: spacing.md,
    padding: spacing.md,
  },
  primaryText: { color: colors.textInverse, fontSize: 16, fontWeight: '700' },
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
  empty: { color: colors.textMuted, marginTop: spacing.lg, textAlign: 'center' },
});
