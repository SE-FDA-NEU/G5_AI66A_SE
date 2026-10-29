/**
 * /debts: money borrowed and lent (US13). What you owe and what is owed to you, from the open
 * debts only, then every debt, the open ones first and the soonest due first; settled ones are
 * under their own tab. A debt past its due date reads "Overdue" (BR14).
 *
 * Everything comes from GET /api/debts. Marking a debt settled, or removing one, asks the API and
 * reloads, so the totals always match what is stored. On a wide screen the totals sit beside the
 * list instead of above it.
 */

import { useFocusEffect } from '@react-navigation/native';
import { useCallback, useState } from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  useWindowDimensions,
  View,
} from 'react-native';

import { api } from '../api/client';
import DebtRow from '../components/DebtRow';
import ErrorMessage from '../components/ErrorMessage';
import MainLayout from '../components/MainLayout';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { describeError } from '../i18n/translate';
import { colors, radius, spacing } from '../theme';
import { overdueCount } from '../utils/debts';
import { formatDong } from '../utils/format';

const FILTERS = [
  { filter: 'open', label: 'debts.open' },
  { filter: 'settled', label: 'debts.settled' },
];

export default function DebtsScreen({ navigation }) {
  const { signOut } = useAuth();
  const { language, t } = useLanguage();
  const { width } = useWindowDimensions();
  const wide = width >= 900;
  // null while loading; then the answer of GET /api/debts.
  const [debts, setDebts] = useState(null);
  const [filter, setFilter] = useState('open');
  const [problem, setProblem] = useState(null);
  const [busy, setBusy] = useState(false);

  const handleApiError = useCallback(
    async (err) => {
      // BR10: the sign-in has expired, so back to /login.
      if (err.status === 401) {
        await signOut();
        return;
      }
      setProblem(err);
    },
    [signOut],
  );

  const load = useCallback(async () => {
    try {
      setDebts(await api.debts());
      setProblem(null);
    } catch (err) {
      await handleApiError(err);
    }
  }, [handleApiError]);

  // Load each time /debts comes into view, so a debt written down on /debts/new is listed.
  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  async function act(call) {
    setBusy(true);
    try {
      await call();
      await load();
    } catch (err) {
      await handleApiError(err);
    } finally {
      setBusy(false);
    }
  }

  const shown = describeError(problem, t, api.baseUrl);
  const items = (debts?.items ?? []).filter((debt) =>
    filter === 'open' ? !debt.settled_on : Boolean(debt.settled_on),
  );
  const overdue = overdueCount(debts?.items ?? []);

  const totals = (
    <View style={wide ? styles.side : null}>
      <View style={styles.totals}>
        <View style={[styles.total, styles.oweBox]}>
          <Text style={styles.totalLabel}>{t('debts.owe')}</Text>
          <Text style={[styles.totalValue, styles.oweText]}>
            {formatDong(debts?.owe ?? 0, language)}
          </Text>
        </View>
        <View style={[styles.total, styles.owedBox]}>
          <Text style={styles.totalLabel}>{t('debts.owed')}</Text>
          <Text style={[styles.totalValue, styles.owedText]}>
            {formatDong(debts?.owed ?? 0, language)}
          </Text>
        </View>
      </View>
      {overdue > 0 ? (
        <Text style={styles.overdueLine}>{t('debts.overdueCount', { count: overdue })}</Text>
      ) : null}
      <Pressable
        style={styles.primaryButton}
        onPress={() => navigation.navigate('NewDebt')}
        accessibilityRole="button"
      >
        <Text style={styles.primaryText}>+ {t('debts.add')}</Text>
      </Pressable>
      <Text style={styles.note}>{t('debts.notSpending')}</Text>
    </View>
  );

  const list = (
    <View style={wide ? styles.main : null}>
      <View style={styles.segment} role="tablist">
        {FILTERS.map((option) => {
          const selected = option.filter === filter;
          return (
            <Pressable
              key={option.filter}
              style={[styles.segmentOption, selected && styles.segmentSelected]}
              onPress={() => setFilter(option.filter)}
              role="tab"
              aria-selected={selected}
            >
              <Text style={[styles.segmentText, selected && styles.segmentTextSelected]}>
                {t(option.label)}
              </Text>
            </Pressable>
          );
        })}
      </View>
      <ErrorMessage problem={shown} />
      {debts === null && !shown ? <ActivityIndicator color={colors.primary} /> : null}
      {debts !== null && items.length === 0 ? (
        <Text style={styles.empty}>
          {t(filter === 'open' ? 'debts.noneOpen' : 'debts.noneSettled')}
        </Text>
      ) : null}
      {items.map((debt) => (
        <DebtRow
          key={debt.id}
          debt={debt}
          busy={busy}
          onSettle={() => act(() => api.settleDebt(debt.id))}
          onRemove={() => act(() => api.removeDebt(debt.id))}
        />
      ))}
    </View>
  );

  return (
    <MainLayout current="Debts">
      <ScrollView contentContainerStyle={styles.page}>
        <View style={wide ? styles.columns : null}>
          {totals}
          {list}
        </View>
      </ScrollView>
    </MainLayout>
  );
}

const styles = StyleSheet.create({
  page: { alignSelf: 'center', maxWidth: 1100, padding: spacing.md, width: '100%' },
  columns: { alignItems: 'flex-start', flexDirection: 'row', gap: spacing.lg },
  side: { width: 360 },
  main: { flex: 1, minWidth: 0 },
  totals: { flexDirection: 'row', gap: spacing.sm },
  total: { borderRadius: radius.md, flex: 1, padding: spacing.md },
  oweBox: { backgroundColor: colors.dangerLight },
  owedBox: { backgroundColor: colors.primaryLight },
  totalLabel: { color: colors.text, fontSize: 13, fontWeight: '600' },
  totalValue: { fontSize: 20, fontWeight: '800', marginTop: spacing.xs },
  oweText: { color: colors.spent },
  owedText: { color: colors.received },
  overdueLine: { color: colors.danger, fontSize: 14, fontWeight: '700', marginTop: spacing.sm },
  primaryButton: {
    alignItems: 'center',
    backgroundColor: colors.primary,
    borderRadius: radius.sm,
    marginTop: spacing.md,
    padding: spacing.md,
  },
  primaryText: { color: colors.textInverse, fontSize: 16, fontWeight: '700' },
  note: { color: colors.textMuted, fontSize: 13, marginBottom: spacing.md, marginTop: spacing.sm },
  segment: {
    borderColor: colors.primary,
    borderRadius: radius.sm,
    borderWidth: 1,
    flexDirection: 'row',
    marginBottom: spacing.md,
    overflow: 'hidden',
  },
  segmentOption: { alignItems: 'center', flex: 1, paddingVertical: spacing.sm },
  segmentSelected: { backgroundColor: colors.primary },
  segmentText: { color: colors.primary, fontSize: 15, fontWeight: '600' },
  segmentTextSelected: { color: colors.textInverse },
  empty: { color: colors.textMuted, marginTop: spacing.md, textAlign: 'center' },
});
