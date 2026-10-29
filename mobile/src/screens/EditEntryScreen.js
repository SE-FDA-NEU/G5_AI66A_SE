/**
 * /transactions/:id: correct or remove one entry (US06).
 *
 * The entry is read from GET /api/transactions/{id} and shown in the same form as a new one, so a
 * correction follows the same rules (BR5, BR6, BR11). Removing asks "Delete this entry?" first,
 * on the screen itself, because a browser has no native dialog the app can style; Cancel keeps the
 * entry. Another account's entry, or one already removed, reads "Entry not found" (BR4).
 */

import { useCallback, useEffect, useState } from 'react';
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from 'react-native';

import { api } from '../api/client';
import EntryForm from '../components/EntryForm';
import ErrorMessage from '../components/ErrorMessage';
import { formStyles } from '../components/formStyles';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { describeError } from '../i18n/translate';
import { colors, radius, spacing } from '../theme';
import { formFromEntry } from '../utils/entryForm';

export default function EditEntryScreen({ navigation, route }) {
  const { signOut } = useAuth();
  const { t } = useLanguage();
  const id = route.params?.id;
  // null while the entry loads; then the form's starting values.
  const [initial, setInitial] = useState(null);
  const [problem, setProblem] = useState(null);
  const [confirming, setConfirming] = useState(false);
  const [removing, setRemoving] = useState(false);

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

  useEffect(() => {
    let current = true;
    api
      .getEntry(id)
      .then((entry) => current && setInitial(formFromEntry(entry)))
      .catch((err) => current && handleApiError(err));
    return () => {
      current = false;
    };
  }, [id, handleApiError]);

  function leave() {
    if (navigation.canGoBack()) navigation.goBack();
    else navigation.replace('Overview');
  }

  async function save(entry) {
    await api.correctEntry(id, entry);
    // US06: the overview reloads when it comes back into view, with the corrected totals.
    leave();
  }

  async function remove() {
    setRemoving(true);
    try {
      await api.removeEntry(id);
      leave();
    } catch (err) {
      setRemoving(false);
      setConfirming(false);
      await handleApiError(err);
    }
  }

  const shown = describeError(problem, t, api.baseUrl);

  if (initial === null) {
    return (
      <View style={styles.center}>
        {shown ? (
          <View style={styles.narrow}>
            <ErrorMessage problem={shown} />
            <Pressable style={formStyles.button} onPress={leave} accessibilityRole="button">
              <Text style={formStyles.buttonText}>{t('editEntry.back')}</Text>
            </Pressable>
          </View>
        ) : (
          <>
            <ActivityIndicator size="large" color={colors.primary} />
            <Text style={styles.centerText}>{t('editEntry.loading')}</Text>
          </>
        )}
      </View>
    );
  }

  return (
    <EntryForm
      initial={initial}
      onSubmit={save}
      onCancel={leave}
      submitLabel={t('editEntry.save')}
    >
      <View style={styles.danger}>
        <ErrorMessage problem={shown} />
        {confirming ? (
          <View style={styles.confirm} role="alertdialog">
            <Text style={styles.confirmTitle}>{t('editEntry.confirm')}</Text>
            <Text style={styles.confirmHint}>{t('editEntry.confirm.hint')}</Text>
            <View style={styles.confirmRow}>
              <Pressable
                style={styles.keep}
                onPress={() => setConfirming(false)}
                accessibilityRole="button"
              >
                <Text style={styles.keepText}>{t('editEntry.keep')}</Text>
              </Pressable>
              <Pressable
                style={[styles.delete, removing && formStyles.buttonDisabled]}
                onPress={remove}
                disabled={removing}
                accessibilityRole="button"
              >
                <Text style={styles.deleteText}>{t('editEntry.delete')}</Text>
              </Pressable>
            </View>
          </View>
        ) : (
          <Pressable
            style={styles.removeLink}
            onPress={() => setConfirming(true)}
            accessibilityRole="button"
          >
            <Text style={styles.removeText}>{t('editEntry.remove')}</Text>
          </Pressable>
        )}
      </View>
    </EntryForm>
  );
}

const styles = StyleSheet.create({
  center: {
    alignItems: 'center',
    backgroundColor: colors.background,
    flex: 1,
    justifyContent: 'center',
    padding: spacing.lg,
  },
  centerText: { color: colors.textMuted, fontSize: 15, marginTop: spacing.md },
  narrow: { maxWidth: 480, width: '100%' },
  danger: {
    borderTopColor: colors.border,
    borderTopWidth: 1,
    marginTop: spacing.lg,
    paddingTop: spacing.md,
  },
  removeLink: { alignItems: 'center', padding: spacing.sm },
  removeText: { color: colors.danger, fontSize: 15, fontWeight: '600' },
  confirm: {
    backgroundColor: colors.dangerLight,
    borderRadius: radius.sm,
    padding: spacing.md,
  },
  confirmTitle: { color: colors.danger, fontSize: 16, fontWeight: '700' },
  confirmHint: { color: colors.text, fontSize: 14, marginTop: spacing.xs },
  confirmRow: { flexDirection: 'row', gap: spacing.sm, marginTop: spacing.md },
  keep: {
    alignItems: 'center',
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderRadius: radius.sm,
    borderWidth: 1,
    flex: 1,
    padding: spacing.sm,
  },
  keepText: { color: colors.text, fontSize: 15, fontWeight: '600' },
  delete: {
    alignItems: 'center',
    backgroundColor: colors.danger,
    borderRadius: radius.sm,
    flex: 1,
    padding: spacing.sm,
  },
  deleteText: { color: colors.textInverse, fontSize: 15, fontWeight: '700' },
});
