/**
 * One month's spending by kind, the biggest first, each with its amount, its share and a bar
 * (US10). Entries with no kind chosen are one line of their own (BR6). An empty month reads
 * "No data yet this month" and draws no empty chart (US10, criterion 2).
 *
 * `limit` keeps only the biggest few, for the card on the overview; /stats shows them all.
 */

import { StyleSheet, Text, View } from 'react-native';

import { useLanguage } from '../i18n/LanguageContext';
import { colors, radius, spacing } from '../theme';
import { formatDong } from '../utils/format';

export default function KindBreakdown({ breakdown, limit }) {
  const { language, t } = useLanguage();

  if (!breakdown || breakdown.total === 0) {
    return <Text style={styles.empty}>{t('stats.noData')}</Text>;
  }

  const items = limit ? breakdown.items.slice(0, limit) : breakdown.items;
  return (
    <View>
      {items.map((item) => {
        const name = item.category ? t(`category.${item.category.name}`) : t('entry.noKind');
        return (
          <View key={item.category?.id ?? 'none'} style={styles.row}>
            <View style={styles.line}>
              <Text style={styles.name} numberOfLines={1}>
                {name}
              </Text>
              <Text style={styles.amount}>
                {formatDong(item.amount, language)} · {item.share}%
              </Text>
            </View>
            <View style={styles.track}>
              <View style={[styles.fill, { width: `${Math.max(item.share, 1)}%` }]} />
            </View>
          </View>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  row: { marginBottom: spacing.sm },
  line: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 4 },
  name: { color: colors.text, flex: 1, fontSize: 14, fontWeight: '600', paddingRight: spacing.sm },
  amount: { color: colors.textMuted, fontSize: 13 },
  track: { backgroundColor: colors.background, borderRadius: radius.sm, height: 8 },
  fill: { backgroundColor: colors.spent, borderRadius: radius.sm, height: 8 },
  empty: { color: colors.textMuted, fontSize: 14, paddingVertical: spacing.md, textAlign: 'center' },
});
