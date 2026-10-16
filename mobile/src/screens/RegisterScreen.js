/**
 * /register: create an account with an email and a password, and arrive on / already signed in,
 * with no second sign-in (US01). The API checks every rule: the address (400), the password
 * length (BR2, 422) and an address already registered (BR1, 409); this screen shows its answer.
 */

import { useState } from 'react';
import {
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Pressable,
  ScrollView,
  Text,
  TextInput,
  View,
} from 'react-native';

import { api } from '../api/client';
import ErrorMessage from '../components/ErrorMessage';
import { formStyles as styles } from '../components/formStyles';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { describeError } from '../i18n/translate';
import { colors } from '../theme';

export default function RegisterScreen({ navigation }) {
  const { signUp } = useAuth();
  const { t } = useLanguage();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  // Like /login: { key } for this screen's own message, or the error the API client threw.
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit() {
    setError(null);
    if (!email.trim() || !password) {
      setError({ key: 'register.missing' });
      return;
    }

    setSubmitting(true);
    try {
      // On success the account is signed in, and the navigator shows / by itself.
      await signUp(email.trim(), password);
    } catch (err) {
      setError(err);
      setSubmitting(false);
    }
  }

  const problem = describeError(error, t, api.baseUrl);

  return (
    <KeyboardAvoidingView
      style={styles.flex}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView contentContainerStyle={styles.container} keyboardShouldPersistTaps="handled">
        <Text style={styles.title}>{t('register.title')}</Text>
        <Text style={styles.subtitle}>{t('register.subtitle')}</Text>

        <Text style={styles.label}>{t('login.email')}</Text>
        <TextInput
          style={styles.input}
          value={email}
          onChangeText={setEmail}
          autoCapitalize="none"
          autoComplete="email"
          keyboardType="email-address"
          placeholder="you@example.com"
          placeholderTextColor={colors.textMuted}
          accessibilityLabel={t('login.email')}
        />

        <Text style={styles.label}>{t('login.password')}</Text>
        <TextInput
          style={styles.input}
          value={password}
          onChangeText={setPassword}
          secureTextEntry
          autoComplete="new-password"
          placeholder="••••••••"
          placeholderTextColor={colors.textMuted}
          onSubmitEditing={handleSubmit}
          accessibilityLabel={t('login.password')}
        />
        <Text style={styles.help}>{t('register.passwordHelp')}</Text>

        <ErrorMessage problem={problem} style={styles.error} />

        <Pressable
          style={[styles.button, submitting && styles.buttonDisabled]}
          onPress={handleSubmit}
          disabled={submitting}
          accessibilityRole="button"
        >
          {submitting ? (
            <ActivityIndicator color={colors.textInverse} />
          ) : (
            <Text style={styles.buttonText}>{t('register.submit')}</Text>
          )}
        </Pressable>

        <View style={styles.switchRow}>
          <Text style={styles.switchText}>{t('register.haveAccount')}</Text>
          <Pressable onPress={() => navigation.navigate('Login')} accessibilityRole="link">
            <Text style={styles.link}>{t('register.toLogin')}</Text>
          </Pressable>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}
