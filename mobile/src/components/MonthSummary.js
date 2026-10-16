/**
 * This month's position at the top of /: money received, money spent and what is left (US04).
 *
 * A month with no entries says "No transactions yet this month" rather than three zeros
 * (criterion 3). What is left turns red, with a minus sign, once more was spent than received, so
 * the state reads in words and sign as well as in colour.
 */

import { StyleSheet, Text, View } from 'react-native';

import { useLanguage } from '../i18n/LanguageContext';
import { colors, radius, spacing } from '../theme';
import { formatDong, formatMonth, formatSigned } from '../utils/format';

export default function MonthSummary({ summary }) {
  const { language, t } = useLanguage();
  const month = t('overview.month', { month: formatMonth(summary.month) });

  if (summary.count === 0) {
    return (
      <View style={styles.card}>
        <Text style={styles.month}>{month}</Text>
        <Text style={styles.emptyTitle}>{t('overview.noMonthEntries')}</Text>
        <Text style={styles.emptyHint}>{t('overview.noMonthEntries.hint')}</Text>
      </View>
    );
  }

  const over = summary.remaining < 0;
  return (
    <View style={styles.card}>
      <Text style={styles.month}>{month}</Text>
      <View style={styles.row}>
        <Figure label={t('overview.income')} value={formatDong(summary.income, language)} />
        <Figure label={t('overview.spending')} value={formatDong(summary.spending, language)} />
      </View>
      <View style={styles.left}>
        <Text style={styles.leftLabel}>{t('overview.remaining')}</Text>
        <Text style={[styles.leftValue, over && styles.over]}>
          {formatSigned(summary.remaining, language)}
        </Text>
      </View>
    </View>
  );
}

function Figure({ label, value }) {
  return (
    <View style={styles.figure}>
      <Text style={styles.figureLabel}>{label}</Text>
      <Text style={styles.figureValue}>{value}</Text>
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
  month: { color: colors.textMuted, fontSize: 13, fontWeight: '600', marginBottom: spacing.sm },
  row: { flexDirection: 'row', gap: spacing.md },
  figure: { flex: 1 },
  figureLabel: { color: colors.textMuted, fontSize: 13 },
  figureValue: { color: colors.text, fontSize: 17, fontWeight: '700', marginTop: 2 },
  left: {
    borderTopColor: colors.border,
    borderTopWidth: 1,
    marginTop: spacing.md,
    paddingTop: spacing.sm,
  },
  leftLabel: { color: colors.textMuted, fontSize: 13 },
  leftValue: { color: colors.received, fontSize: 28, fontWeight: '800', marginTop: 2 },
  over: { color: colors.spent },
  emptyTitle: { color: colors.text, fontSize: 17, fontWeight: '700' },
  emptyHint: { color: colors.textMuted, fontSize: 14, marginTop: spacing.xs },
});
