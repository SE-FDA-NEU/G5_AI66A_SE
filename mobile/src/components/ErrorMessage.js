/**
 * One problem on screen: what happened, in bold, and under it why and what to do next (docs/ui.md,
 * section 3). Takes the `{ message, hint }` that describeError returns, or null to show nothing.
 */

import { StyleSheet, Text, View } from 'react-native';

import { colors, radius, spacing } from '../theme';

export default function ErrorMessage({ problem, style }) {
  if (!problem) return null;
  return (
    <View style={[styles.box, style]} role="alert">
      <Text style={styles.message}>{problem.message}</Text>
      {problem.hint ? <Text style={styles.hint}>{problem.hint}</Text> : null}
    </View>
  );
}

const styles = StyleSheet.create({
  box: {
    backgroundColor: colors.dangerLight,
    borderLeftColor: colors.danger,
    borderLeftWidth: 4,
    borderRadius: radius.sm,
    marginBottom: spacing.md,
    padding: spacing.md,
  },
  message: { color: colors.danger, fontSize: 15, fontWeight: '700' },
  hint: { color: colors.text, fontSize: 14, marginTop: spacing.xs },
});
