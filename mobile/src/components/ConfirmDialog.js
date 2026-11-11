/**
 * A question that must be answered before something that cannot be undone, such as deleting the
 * account (BR16). The safe answer is the second button and the one a stray tap outside chooses.
 */

import { ActivityIndicator, Modal, Pressable, StyleSheet, Text, View } from 'react-native';

import { radius, spacing, useStyles, useTheme } from '../theme';

export default function ConfirmDialog({
  visible,
  title,
  body,
  confirmLabel,
  cancelLabel,
  onConfirm,
  onCancel,
  busy = false,
}) {
  const styles = useStyles(makeStyles);
  const { colors } = useTheme();

  return (
    <Modal visible={visible} transparent animationType="fade" onRequestClose={onCancel}>
      <Pressable style={styles.scrim} onPress={busy ? undefined : onCancel}>
        <Pressable style={styles.card} role="alertdialog" aria-label={title} onPress={() => {}}>
          <Text style={styles.title}>{title}</Text>
          <Text style={styles.body}>{body}</Text>
          <Pressable
            style={[styles.confirm, busy && styles.busy]}
            onPress={onConfirm}
            disabled={busy}
            accessibilityRole="button"
          >
            {busy ? (
              <ActivityIndicator color={colors.textInverse} />
            ) : (
              <Text style={styles.confirmText}>{confirmLabel}</Text>
            )}
          </Pressable>
          <Pressable
            style={styles.cancel}
            onPress={onCancel}
            disabled={busy}
            accessibilityRole="button"
          >
            <Text style={styles.cancelText}>{cancelLabel}</Text>
          </Pressable>
        </Pressable>
      </Pressable>
    </Modal>
  );
}

const makeStyles = (colors) =>
  StyleSheet.create({
    scrim: {
      alignItems: 'center',
      backgroundColor: colors.scrim,
      flex: 1,
      justifyContent: 'center',
      padding: spacing.lg,
    },
    card: {
      backgroundColor: colors.surface,
      borderRadius: radius.md,
      maxWidth: 420,
      padding: spacing.lg,
      width: '100%',
    },
    title: { color: colors.text, fontSize: 20, fontWeight: '700' },
    body: { color: colors.textMuted, fontSize: 15, lineHeight: 22, marginVertical: spacing.md },
    confirm: {
      alignItems: 'center',
      backgroundColor: colors.danger,
      borderRadius: radius.sm,
      paddingVertical: spacing.md,
    },
    busy: { opacity: 0.6 },
    confirmText: { color: colors.textInverse, fontSize: 16, fontWeight: '700' },
    cancel: { alignItems: 'center', marginTop: spacing.sm, paddingVertical: spacing.md },
    cancelText: { color: colors.primary, fontSize: 16, fontWeight: '600' },
  });
