/**
 * /login: sign in with an email and a password (US02), in the chosen language (US11). A link leads
 * to /register for someone with no account yet (US01).
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

export default function LoginScreen({ navigation }) {
  const { signIn } = useAuth();
  const { t } = useLanguage();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  // Either { key } for a message of this screen, or the error the API client threw. It is
  // translated when shown, so switching language also switches a message already on screen.
  const [error, setError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit() {
    setError(null);
    if (!email.trim() || !password) {
      setError({ key: 'login.missing' });
      return;
    }

    setSubmitting(true);
    try {
      await signIn(email.trim(), password);
    } catch (err) {
      // BR3: the API sends "Incorrect email or password" for every failure.
      setError(err);
      setSubmitting(false);
    }
  }

  const problem = describeError(error, t, api.baseUrl);

  return (
    <KeyboardAvoidingView
      style={styles.flex}
      // On iOS the keyboard would otherwise cover the fields.
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView contentContainerStyle={styles.container} keyboardShouldPersistTaps="handled">
        <Text style={styles.title}>{t('app.title')}</Text>
        <Text style={styles.subtitle}>{t('login.subtitle')}</Text>

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
          autoComplete="password"
          placeholder="••••••••"
          placeholderTextColor={colors.textMuted}
          onSubmitEditing={handleSubmit}
          accessibilityLabel={t('login.password')}
        />

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
            <Text style={styles.buttonText}>{t('login.submit')}</Text>
          )}
        </Pressable>

        <View style={styles.switchRow}>
          <Text style={styles.switchText}>{t('login.noAccount')}</Text>
          <Pressable onPress={() => navigation.navigate('Register')} accessibilityRole="link">
            <Text style={styles.link}>{t('login.toRegister')}</Text>
          </Pressable>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}
