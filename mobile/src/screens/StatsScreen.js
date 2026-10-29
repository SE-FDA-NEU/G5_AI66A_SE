/**
 * /stats: where the money went. Spending month by month or year by year, with the month that cost
 * the most and the one that cost the least (US12, BR12), and one month by kind of spending (US10).
 *
 * Everything comes from GET /api/stats/months, /years and /breakdown. Tapping a month in the chart
 * breaks that month down. The year cannot move past this one (BR12), and a year with no entries
 * reads "No entries in this year" rather than an empty chart. On a wide screen the chart and the
 * breakdown sit side by side.
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
import BarChart from '../components/BarChart';
import ErrorMessage from '../components/ErrorMessage';
import KindBreakdown from '../components/KindBreakdown';
import MainLayout from '../components/MainLayout';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { describeError } from '../i18n/translate';
import { colors, radius, spacing } from '../theme';
import { defaultMonth } from '../utils/chart';
import { todayIso } from '../utils/entryForm';
import { formatDong, formatMonth } from '../utils/format';

const VIEWS = [
  { view: 'months', label: 'stats.byMonth' },
  { view: 'years', label: 'stats.byYear' },
];

export default function StatsScreen() {
  const { signOut } = useAuth();
  const { language, t } = useLanguage();
  const { width } = useWindowDimensions();
  const wide = width >= 900;
  const thisYear = Number(todayIso().slice(0, 4));
  const [view, setView] = useState('months');
  const [year, setYear] = useState(thisYear);
  // null while loading; then the answer of /api/stats/months or /years.
  const [trend, setTrend] = useState(null);
  const [month, setMonth] = useState(null);
  const [breakdown, setBreakdown] = useState(null);
  const [problem, setProblem] = useState(null);

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

  const loadBreakdown = useCallback(
    async (chosen) => {
      setMonth(chosen);
      setBreakdown(null);
      try {
        setBreakdown(await api.breakdown(chosen));
      } catch (err) {
        await handleApiError(err);
      }
    },
    [handleApiError],
  );

  const load = useCallback(async () => {
    setProblem(null);
    setTrend(null);
    try {
      if (view === 'years') {
        setTrend(await api.statsYears());
        return;
      }
      const months = await api.statsMonths(year);
      setTrend(months);
      await loadBreakdown(defaultMonth(year, months.busiest, todayIso()));
    } catch (err) {
      await handleApiError(err);
    }
  }, [view, year, loadBreakdown, handleApiError]);

  // Load each time /stats comes into view, so an entry saved since is already counted.
  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  const shown = describeError(problem, t, api.baseUrl);
  const empty = trend !== null && trend.periods.every((period) => period.count === 0);
  const nameOf = (period) => (period?.includes('-') ? formatMonth(period) : period);
  const spendingOf = (period) =>
    trend?.periods.find((candidate) => candidate.period === period)?.spending ?? 0;

  const chartCard = (
    <View style={[styles.card, wide && styles.chartCard]}>
      <View style={styles.segment} role="radiogroup">
        {VIEWS.map((option) => {
          const selected = option.view === view;
          return (
            <Pressable
              key={option.view}
              style={[styles.segmentOption, selected && styles.segmentSelected]}
              onPress={() => setView(option.view)}
              role="radio"
              aria-checked={selected}
            >
              <Text style={[styles.segmentText, selected && styles.segmentTextSelected]}>
                {t(option.label)}
              </Text>
            </Pressable>
          );
        })}
      </View>

      {view === 'months' ? (
        <View style={styles.yearRow}>
          <Pressable
            style={styles.arrow}
            onPress={() => setYear(year - 1)}
            accessibilityRole="button"
            accessibilityLabel={t('stats.previousYear')}
          >
            <Text style={styles.arrowText}>‹</Text>
          </Pressable>
          <Text style={styles.year}>{year}</Text>
          <Pressable
            style={[styles.arrow, year >= thisYear && styles.arrowOff]}
            // BR12: no year later than this one.
            onPress={() => setYear(year + 1)}
            disabled={year >= thisYear}
            accessibilityRole="button"
            accessibilityLabel={t('stats.nextYear')}
          >
            <Text style={styles.arrowText}>›</Text>
          </Pressable>
        </View>
      ) : null}

      <ErrorMessage problem={shown} />

      {trend === null && !shown ? (
        <ActivityIndicator style={styles.loading} color={colors.primary} />
      ) : null}

      {empty ? (
        <View style={styles.emptyBox}>
          <Text style={styles.emptyTitle}>{t('stats.noEntries')}</Text>
          <Text style={styles.emptyHint}>{t('stats.noEntries.hint')}</Text>
        </View>
      ) : null}

      {trend !== null && !empty ? (
        <View>
          <View style={styles.highlights}>
            <Highlight
              label={t('stats.most')}
              period={nameOf(trend.busiest)}
              amount={formatDong(spendingOf(trend.busiest), language)}
              tone={colors.spent}
            />
            <Highlight
              label={t('stats.least')}
              period={nameOf(trend.quietest)}
              amount={formatDong(spendingOf(trend.quietest), language)}
              tone={colors.received}
            />
          </View>
          <BarChart
            periods={trend.periods}
            selected={view === 'months' ? month : null}
            onSelect={view === 'months' ? loadBreakdown : null}
            busiest={trend.busiest}
          />
          {view === 'months' ? <Text style={styles.tapHint}>{t('stats.tapHint')}</Text> : null}
        </View>
      ) : null}
    </View>
  );

  const breakdownCard =
    view === 'months' && month && !empty ? (
      <View style={[styles.card, wide && styles.breakdownCard]}>
        <Text style={styles.cardTitle}>{t('stats.whereItWent', { month: formatMonth(month) })}</Text>
        {breakdown === null ? (
          <ActivityIndicator color={colors.primary} />
        ) : (
          <>
            <Text style={styles.total}>
              {t('stats.totalSpent', { amount: formatDong(breakdown.total, language) })}
            </Text>
            <KindBreakdown breakdown={breakdown} />
          </>
        )}
      </View>
    ) : null;

  return (
    <MainLayout current="Stats">
      <ScrollView contentContainerStyle={styles.page}>
        <View style={wide ? styles.columns : null}>
          {chartCard}
          {breakdownCard}
        </View>
      </ScrollView>
    </MainLayout>
  );
}

function Highlight({ label, period, amount, tone }) {
  return (
    <View style={[styles.highlight, { borderLeftColor: tone }]}>
      <Text style={styles.highlightLabel}>{label}</Text>
      <Text style={styles.highlightPeriod}>{period}</Text>
      <Text style={[styles.highlightAmount, { color: tone }]}>{amount}</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  page: { alignSelf: 'center', maxWidth: 1100, padding: spacing.md, width: '100%' },
  columns: { alignItems: 'flex-start', flexDirection: 'row', gap: spacing.md },
  card: {
    backgroundColor: colors.surface,
    borderRadius: radius.md,
    marginBottom: spacing.md,
    padding: spacing.md,
  },
  chartCard: { flex: 3, minWidth: 0 },
  breakdownCard: { flex: 2, minWidth: 0 },
  segment: {
    borderColor: colors.primary,
    borderRadius: radius.sm,
    borderWidth: 1,
    flexDirection: 'row',
    overflow: 'hidden',
  },
  segmentOption: { alignItems: 'center', flex: 1, paddingVertical: spacing.sm },
  segmentSelected: { backgroundColor: colors.primary },
  segmentText: { color: colors.primary, fontSize: 15, fontWeight: '600' },
  segmentTextSelected: { color: colors.textInverse },
  yearRow: {
    alignItems: 'center',
    flexDirection: 'row',
    justifyContent: 'center',
    marginTop: spacing.md,
  },
  arrow: { paddingHorizontal: spacing.md, paddingVertical: spacing.xs },
  arrowOff: { opacity: 0.25 },
  arrowText: { color: colors.primary, fontSize: 24, fontWeight: '700' },
  year: { color: colors.text, fontSize: 18, fontWeight: '700', minWidth: 64, textAlign: 'center' },
  loading: { marginVertical: spacing.lg },
  emptyBox: { alignItems: 'center', paddingVertical: spacing.lg },
  emptyTitle: { color: colors.text, fontSize: 17, fontWeight: '700' },
  emptyHint: { color: colors.textMuted, fontSize: 14, marginTop: spacing.xs, textAlign: 'center' },
  highlights: { flexDirection: 'row', gap: spacing.sm, marginVertical: spacing.md },
  highlight: {
    backgroundColor: colors.background,
    borderLeftWidth: 4,
    borderRadius: radius.sm,
    flex: 1,
    padding: spacing.sm,
  },
  highlightLabel: { color: colors.textMuted, fontSize: 12 },
  highlightPeriod: { color: colors.text, fontSize: 16, fontWeight: '700', marginTop: 2 },
  highlightAmount: { fontSize: 14, fontWeight: '700', marginTop: 2 },
  tapHint: { color: colors.textMuted, fontSize: 12, marginTop: spacing.xs },
  cardTitle: { color: colors.text, fontSize: 16, fontWeight: '700' },
  total: { color: colors.textMuted, fontSize: 13, marginBottom: spacing.md, marginTop: 2 },
});
