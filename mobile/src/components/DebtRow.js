/**
 * One debt on /debts (US13): who, which way, how much, and its due date, with "Overdue" in words
 * as well as in red (BR14). An open debt can be marked settled; any debt can be removed, after
 * "Remove this debt?" on the row itself.
 */

import { useState } from 'react';
import { Pressable, StyleSheet, Text, View } from 'react-native';

import { useLanguage } from '../i18n/LanguageContext';
import { colors, radius, spacing } from '../theme';
import { dueState } from '../utils/debts';
import { todayIso } from '../utils/entryForm';
import { formatDate, formatDong } from '../utils/format';

export default function DebtRow({ debt, onSettle, onRemove, busy }) {
  const { language, t } = useLanguage();
  const [confirming, setConfirming] = useState(false);
  const borrowed = debt.direction === 'borrowed';
  const state = dueState(debt, todayIso());
  const open = !debt.settled_on;

  return (
    <View style={[styles.row, debt.overdue && styles.rowOverdue, !open && styles.rowSettled]}>
      <View style={styles.top}>
        <View style={styles.left}>
          <Text style={styles.person} numberOfLines={1}>
            {debt.person}
          </Text>
          <Text style={styles.direction}>
            {t(borrowed ? 'debts.youBorrowed' : 'debts.youLent', {
              date: formatDate(debt.started_on),
            })}
          </Text>
        </View>
        <Text style={[styles.amount, borrowed ? styles.owe : styles.owed]}>
          {formatDong(debt.amount, language)}
        </Text>
      </View>

      <View style={styles.bottom}>
        <View style={[styles.badge, styles[state.tone]]}>
          <Text style={[styles.badgeText, styles[`${state.tone}Text`]]}>
            {t(state.key, { date: formatDate(state.date) })}
          </Text>
        </View>
        {debt.note ? (
          <Text style={styles.note} numberOfLines={1}>
            {debt.note}
          </Text>
        ) : null}
      </View>

      {confirming ? (
        <View style={styles.confirm} role="alertdialog">
          <Text style={styles.confirmText}>{t('debts.confirmRemove')}</Text>
          <Pressable style={styles.small} onPress={() => setConfirming(false)}>
            <Text style={styles.smallText}>{t('editEntry.keep')}</Text>
          </Pressable>
          <Pressable
            style={[styles.small, styles.smallDanger]}
            onPress={() => onRemove(debt)}
            disabled={busy}
          >
            <Text style={styles.smallDangerText}>{t('debts.remove')}</Text>
          </Pressable>
        </View>
      ) : (
        <View style={styles.actions}>
          {open ? (
            <Pressable
              style={[styles.small, styles.smallPrimary]}
              onPress={() => onSettle(debt)}
              disabled={busy}
              accessibilityRole="button"
            >
              <Text style={styles.smallPrimaryText}>{t('debts.settle')}</Text>
            </Pressable>
          ) : null}
          <Pressable style={styles.small} onPress={() => setConfirming(true)} accessibilityRole="button">
            <Text style={styles.smallText}>{t('debts.remove')}</Text>
          </Pressable>
        </View>
      )}
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    backgroundColor: colors.surface,
    borderLeftColor: colors.border,
    borderLeftWidth: 4,
    borderRadius: radius.sm,
    marginBottom: spacing.sm,
    padding: spacing.md,
  },
  rowOverdue: { borderLeftColor: colors.danger },
  rowSettled: { opacity: 0.75 },
  top: { alignItems: 'flex-start', flexDirection: 'row', justifyContent: 'space-between' },
  left: { flex: 1, paddingRight: spacing.sm },
  person: { color: colors.text, fontSize: 16, fontWeight: '700' },
  direction: { color: colors.textMuted, fontSize: 13, marginTop: 2 },
  amount: { fontSize: 16, fontWeight: '700' },
  owe: { color: colors.spent },
  owed: { color: colors.received },
  bottom: { alignItems: 'center', flexDirection: 'row', gap: spacing.sm, marginTop: spacing.sm },
  badge: { borderRadius: radius.md, paddingHorizontal: spacing.sm, paddingVertical: 2 },
  badgeText: { fontSize: 12, fontWeight: '600' },
  muted: { backgroundColor: colors.background },
  mutedText: { color: colors.textMuted },
  danger: { backgroundColor: colors.dangerLight },
  dangerText: { color: colors.danger },
  warning: { backgroundColor: colors.warningLight },
  warningText: { color: colors.warning },
  note: { color: colors.textMuted, flex: 1, fontSize: 13 },
  actions: { flexDirection: 'row', gap: spacing.sm, justifyContent: 'flex-end', marginTop: spacing.sm },
  confirm: {
    alignItems: 'center',
    backgroundColor: colors.dangerLight,
    borderRadius: radius.sm,
    flexDirection: 'row',
    gap: spacing.sm,
    marginTop: spacing.sm,
    padding: spacing.sm,
  },
  confirmText: { color: colors.danger, flex: 1, fontSize: 14, fontWeight: '700' },
  small: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderRadius: radius.sm,
    borderWidth: 1,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
  },
  smallText: { color: colors.text, fontSize: 13, fontWeight: '600' },
  smallPrimary: { backgroundColor: colors.primary, borderColor: colors.primary },
  smallPrimaryText: { color: colors.textInverse, fontSize: 13, fontWeight: '700' },
  smallDanger: { backgroundColor: colors.danger, borderColor: colors.danger },
  smallDangerText: { color: colors.textInverse, fontSize: 13, fontWeight: '700' },
});
