/**
 * One entry in the list on /: its note, its kind of spending, its amount and its date (US05).
 * The kind of spending is shown in the chosen language; the note stays exactly as typed (US11).
 */

import { StyleSheet, Text, View } from 'react-native';

import { useLanguage } from '../i18n/LanguageContext';
import { colors, radius, spacing } from '../theme';
import { formatAmount, formatDate } from '../utils/format';

export default function EntryRow({ entry }) {
  const { language, t } = useLanguage();
  const received = entry.kind === 'income';
  const note = entry.note || t('entry.noNote');
  const kindOfSpending = entry.category
    ? t(`category.${entry.category.name}`)
    : t('entry.noKind');
  const amount = formatAmount(entry.amount, entry.kind, language);
  const date = formatDate(entry.occurred_on);

  return (
    <View style={styles.row} accessibilityLabel={`${note}, ${kindOfSpending}, ${amount}, ${date}`}>
      <View style={styles.left}>
        <Text style={styles.note} numberOfLines={1}>
          {note}
        </Text>
        <Text style={styles.kind}>{kindOfSpending}</Text>
      </View>
      <View style={styles.right}>
        <Text style={[styles.amount, received ? styles.received : styles.spent]}>{amount}</Text>
        <Text style={styles.date}>{date}</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderRadius: radius.sm,
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: spacing.sm,
    padding: spacing.md,
  },
  left: { flex: 1, paddingRight: spacing.sm },
  note: { color: colors.text, fontSize: 15, fontWeight: '600' },
  kind: { color: colors.textMuted, fontSize: 13, marginTop: 2 },
  right: { alignItems: 'flex-end' },
  amount: { fontSize: 15, fontWeight: '700' },
  received: { color: colors.received },
  spent: { color: colors.spent },
  date: { color: colors.textMuted, fontSize: 12, marginTop: 2 },
});
