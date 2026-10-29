/**
 * A bar chart of money spent and received, one group per month or per year (US12). Drawn with
 * plain views, so it looks the same in the browser and on a phone and needs no chart library.
 *
 * Spent and received have their own colour and are named in the legend under the chart, and the
 * month that cost the most carries its amount in words above its bar, so the chart reads without
 * colour vision as well. Tapping a group selects it.
 */

import { Pressable, StyleSheet, Text, View } from 'react-native';

import { useLanguage } from '../i18n/LanguageContext';
import { colors, radius, spacing } from '../theme';
import { barHeight, chartMax, periodLabel, shortAmount } from '../utils/chart';
import { formatDong } from '../utils/format';

const HEIGHT = 160;

export default function BarChart({ periods, selected, onSelect, busiest }) {
  const { language, t } = useLanguage();
  const max = chartMax(periods);

  return (
    <View>
      <View style={styles.chart}>
        {periods.map((period) => {
          const isSelected = period.period === selected;
          const label = `${periodLabel(period.period, language)}: ${t('stats.spent')} ${formatDong(
            period.spending,
            language,
          )}, ${t('stats.received')} ${formatDong(period.income, language)}`;
          return (
            <Pressable
              key={period.period}
              style={[styles.group, isSelected && styles.groupSelected]}
              onPress={onSelect ? () => onSelect(period.period) : undefined}
              disabled={!onSelect}
              accessibilityRole={onSelect ? 'button' : undefined}
              accessibilityLabel={label}
              aria-selected={isSelected}
            >
              <Text style={[styles.value, period.period === busiest && styles.valueBusiest]}>
                {period.spending > 0 ? shortAmount(period.spending, language) : ''}
              </Text>
              <View style={styles.bars}>
                <View
                  style={[
                    styles.bar,
                    styles.spent,
                    { height: barHeight(period.spending, max, HEIGHT) },
                  ]}
                />
                <View
                  style={[
                    styles.bar,
                    styles.received,
                    { height: barHeight(period.income, max, HEIGHT) },
                  ]}
                />
              </View>
              <Text style={[styles.label, isSelected && styles.labelSelected]}>
                {periodLabel(period.period, language)}
              </Text>
            </Pressable>
          );
        })}
      </View>
      <View style={styles.legend}>
        <View style={[styles.key, styles.spent]} />
        <Text style={styles.legendText}>{t('stats.spent')}</Text>
        <View style={[styles.key, styles.received]} />
        <Text style={styles.legendText}>{t('stats.received')}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  chart: {
    alignItems: 'flex-end',
    borderBottomColor: colors.border,
    borderBottomWidth: 1,
    flexDirection: 'row',
    gap: 2,
  },
  group: {
    alignItems: 'center',
    borderRadius: radius.sm,
    flex: 1,
    minWidth: 0,
    paddingBottom: spacing.xs,
    paddingTop: spacing.xs,
  },
  groupSelected: { backgroundColor: colors.primaryLight },
  value: { color: colors.textMuted, fontSize: 10, marginBottom: 2 },
  valueBusiest: { color: colors.spent, fontWeight: '700' },
  bars: { alignItems: 'flex-end', flexDirection: 'row', gap: 2, height: HEIGHT },
  bar: { borderTopLeftRadius: 3, borderTopRightRadius: 3, width: 9 },
  spent: { backgroundColor: colors.spent },
  received: { backgroundColor: colors.receivedSoft },
  label: { color: colors.textMuted, fontSize: 11, marginTop: spacing.xs },
  labelSelected: { color: colors.primary, fontWeight: '700' },
  legend: { alignItems: 'center', flexDirection: 'row', gap: spacing.xs, marginTop: spacing.sm },
  key: { borderRadius: 2, height: 10, marginLeft: spacing.sm, width: 10 },
  legendText: { color: colors.textMuted, fontSize: 12 },
});
