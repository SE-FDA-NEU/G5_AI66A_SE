/**
 * /account/delete: delete the account and everything in it (US18, BR16). Three steps, so it is
 * never done by accident: the warning, the email and current password typed again, then "Are you
 * sure?". The server checks the email and password once more; a mistake deletes nothing and says
 * so. After the deletion the app is signed out and the welcome screen says what happened.
 */

import { useState } from 'react';
import {
  KeyboardAvoidingView,
  Platform,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  View,
} from 'react-native';

import { api } from '../api/client';
import ConfirmDialog from '../components/ConfirmDialog';
import ErrorMessage from '../components/ErrorMessage';
import { useFormStyles } from '../components/formStyles';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { describeError } from '../i18n/translate';
import { radius, spacing, useStyles, useTheme } from '../theme';

export default function DeleteAccountScreen() {
  const styles = useStyles(makeStyles);
  const formStyles = useFormStyles();
  const { colors } = useTheme();
  const { user, deleteAccount } = useAuth();
  const { t } = useLanguage();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const [asking, setAsking] = useState(false);
  const [deleting, setDeleting] = useState(false);

  function ask() {
    setError(null);
    if (!email.trim() || !password) {
      setError({ key: 'deleteAccount.missing' });
      return;
    }
    setAsking(true);
  }

  async function confirm() {
    setDeleting(true);
    try {
      await deleteAccount(email.trim(), password);
      // Signed out: the navigator shows the welcome screen, with its notice.
    } catch (err) {
      setAsking(false);
      setDeleting(false);
      setError(err);
    }
  }

  const problem = error?.key
    ? { message: t(error.key), hint: null }
    : describeError(error, t, api.baseUrl);

  return (
    <KeyboardAvoidingView
      style={formStyles.flex}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView contentContainerStyle={formStyles.container} keyboardShouldPersistTaps="handled">
        <View style={styles.warning} role="alert">
          <Text style={styles.warningTitle}>⚠ {t('deleteAccount.title')}</Text>
          <Text style={styles.warningText}>{t('deleteAccount.warning')}</Text>
        </View>
        <Text style={formStyles.subtitle}>{t('deleteAccount.instructions')}</Text>

        <Text style={formStyles.label}>{t('login.email')}</Text>
        <TextInput
          style={formStyles.input}
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          autoComplete="email"
          keyboardType="email-address"
          placeholder={user?.email ?? 'you@example.com'}
          placeholderTextColor={colors.textMuted}
          accessibilityLabel={t('login.email')}
        />

        <Text style={formStyles.label}>{t('login.password')}</Text>
        <TextInput
          style={formStyles.input}
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          autoComplete="current-password"
          placeholder="••••••••"
          placeholderTextColor={colors.textMuted}
          onSubmitEditing={ask}
          accessibilityLabel={t('login.password')}
        />

        <ErrorMessage problem={problem} style={formStyles.error} />

        <Pressable style={styles.danger} onPress={ask} accessibilityRole="button">
          <Text style={styles.dangerText}>{t('deleteAccount.submit')}</Text>
        </Pressable>
      </ScrollView>

      <ConfirmDialog
        visible={asking}
        title={t('deleteAccount.confirmTitle')}
        body={t('deleteAccount.confirmBody', { email: user?.email ?? email })}
        confirmLabel={t('deleteAccount.confirm')}
        cancelLabel={t('deleteAccount.cancel')}
        onConfirm={confirm}
        onCancel={() => setAsking(false)}
        busy={deleting}
      />
    </KeyboardAvoidingView>
  );
}

const makeStyles = (colors) =>
  StyleSheet.create({
    warning: {
      backgroundColor: colors.dangerLight,
      borderColor: colors.danger,
      borderRadius: radius.md,
      borderWidth: 1,
      marginBottom: spacing.md,
      padding: spacing.md,
    },
    warningTitle: { color: colors.danger, fontSize: 18, fontWeight: '800' },
    warningText: { color: colors.text, fontSize: 15, lineHeight: 22, marginTop: spacing.xs },
    danger: {
      alignItems: 'center',
      backgroundColor: colors.danger,
      borderRadius: radius.sm,
      marginTop: spacing.md,
      paddingVertical: spacing.md,
    },
    dangerText: { color: colors.textInverse, fontSize: 16, fontWeight: '700' },
  });
