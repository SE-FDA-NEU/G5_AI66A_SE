/**
 * The overview at /. For now it only confirms the sign-in; #65 fills it with the most recent
 * entries (US05).
 */

import { Pressable, StyleSheet, Text, View } from 'react-native';

import { useAuth } from '../context/AuthContext';
import { colors, spacing } from '../theme';

export default function OverviewScreen() {
  const { user, signOut } = useAuth();

  return (
    <View style={styles.container}>
      <Text style={styles.text}>Signed in{user ? ` as ${user.email}` : ''}.</Text>
      <Pressable onPress={signOut} accessibilityRole="button">
        <Text style={styles.link}>Sign out</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    alignItems: 'center',
    backgroundColor: colors.background,
    flex: 1,
    justifyContent: 'center',
    padding: spacing.lg,
  },
  text: { color: colors.text, fontSize: 16, marginBottom: spacing.md },
  link: { color: colors.primary, fontSize: 15, fontWeight: '600' },
});
