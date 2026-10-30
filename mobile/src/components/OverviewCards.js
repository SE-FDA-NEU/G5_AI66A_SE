/**
 * The cards beside the list on a wide screen at /: where this month's money went (US10), the
 * last six months (US12) and the debts still open (US13). Each card opens its own screen.
 *
 * They are extras: the overview is complete without them, so a card that cannot load is left out
 * rather than shown as an error; the month card on / already says when the server cannot be
 * reached. They reload each time / comes into view, like the rest of the page.
 */

import { useFocusEffect } from '@react-navigation/native';
import { useCallback, useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import { api } from '../api/client';
import BarChart from './BarChart';
import KindBreakdown from './KindBreakdown';
import { useLanguage } from '../i18n/LanguageContext';
import { colors, radius, spacing } from '../theme';
import { lastMonths } from '../utils/chart';
import { overdueCount } from '../utils/debts';
import { todayIso } from '../utils/entryForm';
import { formatDong } from '../utils/format';

const SHOWN_KINDS = 4;
const SHOWN_MONTHS = 6;

export default function OverviewCards({ navigation }) {
  const { language, t } = useLanguage();
  const [breakdown, setBreakdown] = useState(null);
  const [months, setMonths] = useState(null);
  const [debts, setDebts] = useState(null);

  const load = useCallback(async () => {
    const today = todayIso();
    const year = Number(today.slice(0, 4));
    const month = Number(today.slice(5, 7));
    // Six months back can reach into last year, so ask for both years when it does.
    const years = month < SHOWN_MONTHS ? [year - 1, year] : [year];
    const [kinds, open, ...trends] = await Promise.allSettled([
      api.breakdown(),
      api.debts(),
      ...years.map((y) => api.statsMonths(y)),
    ]);
    setBreakdown(kinds.status === 'fulfilled' ? kinds.value : null);
    setDebts(open.status === 'fulfilled' ? open.value : null);
    setMonths(
      trends.every((answer) => answer.status === 'fulfilled')
        ? lastMonths(trends.flatMap((answer) => answer.value.periods), today, SHOWN_MONTHS)
        : null,
    );
  }, []);

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  return (
    <View>
      {breakdown ? (
        <Card
          title={t('overview.whereItWent')}
          more={t('overview.toStats')}
          onMore={() => navigation.navigate('Stats')}
        >
          <KindBreakdown breakdown={breakdown} limit={SHOWN_KINDS} />
        </Card>
      ) : null}

      {months ? (
        <Card
          title={t('overview.lastMonths')}
          more={t('overview.toStats')}
          onMore={() => navigation.navigate('Stats')}
        >
          <BarChart periods={months} height={90} />
        </Card>
      ) : null}

      {debts ? (
        <Card
          title={t('debts.title')}
          more={t('overview.toDebts')}
          onMore={() => navigation.navigate('Debts')}
        >
          <View style={styles.debts}>
            <View style={styles.debt}>
              <Text style={styles.debtLabel}>{t('debts.owe')}</Text>
              <Text style={[styles.debtValue, styles.owe]}>{formatDong(debts.owe, language)}</Text>
            </View>
            <View style={styles.debt}>
              <Text style={styles.debtLabel}>{t('debts.owed')}</Text>
              <Text style={[styles.debtValue, styles.owed]}>{formatDong(debts.owed, language)}</Text>
            </View>
          </View>
          {overdueCount(debts.items) > 0 ? (
            <Text style={styles.overdue}>
              {t('debts.overdueCount', { count: overdueCount(debts.items) })}
            </Text>
          ) : null}
        </Card>
      ) : null}
    </View>
  );
}

function Card({ title, more, onMore, children }) {
  return (
    <View style={styles.card}>
      <View style={styles.head}>
        <Text style={styles.title}>{title}</Text>
        <Pressable onPress={onMore} accessibilityRole="link">
          <Text style={styles.more}>{more} ›</Text>
        </Pressable>
      </View>
      {children}
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.surface,
    borderRadius: radius.md,
    marginBottom: spacing.md,
    padding: spacing.md,
  },
  head: {
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.sm,
  },
  title: { color: colors.text, fontSize: 15, fontWeight: '700' },
  more: { color: colors.primary, fontSize: 13, fontWeight: '600' },
  debts: { flexDirection: 'row', gap: spacing.md },
  debt: { flex: 1 },
  debtLabel: { color: colors.textMuted, fontSize: 13 },
  debtValue: { fontSize: 17, fontWeight: '700', marginTop: 2 },
  owe: { color: colors.spent },
  owed: { color: colors.received },
  overdue: { color: colors.danger, fontSize: 13, fontWeight: '700', marginTop: spacing.sm },
});
