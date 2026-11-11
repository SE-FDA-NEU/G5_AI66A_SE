/**
 * /profile: who is signed in (US16). The email is shown but cannot be changed (BR15); the full
 * name, the name to call them, the phone number and the picture are all optional. Only what
 * changed is sent to PATCH /api/users/me, and the greeting on / uses the new name at once.
 */

import { useEffect, useState } from 'react';
import {
  ActivityIndicator,
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
import Avatar from '../components/Avatar';
import ErrorMessage from '../components/ErrorMessage';
import { useFormStyles } from '../components/formStyles';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { describeError } from '../i18n/translate';
import { spacing, useStyles, useTheme } from '../theme';
import { pickAvatar } from '../utils/pickAvatar';
import { profileChanges } from '../utils/profile';

function formOf(user) {
  return {
    full_name: user?.full_name ?? '',
    nickname: user?.nickname ?? '',
    phone: user?.phone ?? '',
    avatar: user?.avatar ?? null,
  };
}

export default function ProfileScreen() {
  const styles = useStyles(makeStyles);
  const formStyles = useFormStyles();
  const { colors } = useTheme();
  const { user, updateProfile, signOut } = useAuth();
  const { t } = useLanguage();
  const [saved, setSaved] = useState(user);
  const [form, setForm] = useState(formOf(user));
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);
  const [done, setDone] = useState(false);

  // Read the profile again: another device may have changed it since this one signed in.
  useEffect(() => {
    let cancelled = false;
    api
      .profile()
      .then((fresh) => {
        if (cancelled) return;
        setSaved(fresh);
        setForm(formOf(fresh));
      })
      .catch((err) => {
        if (!cancelled && err.status === 401) signOut();
      });
    return () => {
      cancelled = true;
    };
  }, [signOut]);

  const set = (field) => (value) => {
    setDone(false);
    setForm((before) => ({ ...before, [field]: value }));
  };

  async function choosePicture() {
    setError(null);
    try {
      const picture = await pickAvatar();
      if (picture) set('avatar')(picture);
    } catch {
      setError({ key: 'error.pictureFailed' });
    }
  }

  async function save() {
    setError(null);
    const changes = profileChanges(saved, form);
    if (Object.keys(changes).length === 0) {
      setDone(true);
      return;
    }
    setSaving(true);
    try {
      const fresh = await updateProfile(changes);
      setSaved(fresh);
      setForm(formOf(fresh));
      setDone(true);
    } catch (err) {
      if (err.status === 401) {
        await signOut();
        return;
      }
      setError(err);
    } finally {
      setSaving(false);
    }
  }

  const problem = error?.key
    ? { message: t(error.key), hint: t(`${error.key}.hint`) }
    : describeError(error, t, api.baseUrl);
  const optional = ` (${t('profile.optional')})`;

  return (
    <KeyboardAvoidingView
      style={formStyles.flex}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView contentContainerStyle={[formStyles.container, styles.container]}>
        <View style={styles.pictureRow}>
          <Avatar user={{ ...saved, ...form, email: saved?.email }} size={88} />
          <View style={styles.pictureButtons}>
            <Text style={formStyles.label}>
              {t('profile.photo')}
              {optional}
            </Text>
            <Pressable onPress={choosePicture} accessibilityRole="button">
              <Text style={formStyles.link}>{t('profile.choosePhoto')}</Text>
            </Pressable>
            {form.avatar ? (
              <Pressable onPress={() => set('avatar')(null)} accessibilityRole="button">
                <Text style={[formStyles.link, styles.remove]}>{t('profile.removePhoto')}</Text>
              </Pressable>
            ) : null}
          </View>
        </View>

        <Text style={formStyles.label}>{t('profile.email')}</Text>
        <TextInput
          style={[formStyles.input, styles.readOnly]}
          value={saved?.email ?? ''}
          editable={false}
          accessibilityLabel={t('profile.email')}
        />
        <Text style={formStyles.help}>{t('profile.emailFixed')}</Text>

        <Text style={formStyles.label}>
          {t('profile.fullName')}
          {optional}
        </Text>
        <TextInput
          style={formStyles.input}
          value={form.full_name}
          onChangeText={set('full_name')}
          autoComplete="name"
          placeholder="Nguyen Thi Mai"
          placeholderTextColor={colors.textMuted}
          accessibilityLabel={t('profile.fullName')}
        />

        <Text style={formStyles.label}>
          {t('profile.nickname')}
          {optional}
        </Text>
        <TextInput
          style={formStyles.input}
          value={form.nickname}
          onChangeText={set('nickname')}
          autoComplete="nickname"
          placeholder="Mai"
          placeholderTextColor={colors.textMuted}
          accessibilityLabel={t('profile.nickname')}
        />
        <Text style={formStyles.help}>{t('profile.nicknameHelp')}</Text>

        <Text style={formStyles.label}>
          {t('profile.phone')}
          {optional}
        </Text>
        <TextInput
          style={formStyles.input}
          value={form.phone}
          onChangeText={set('phone')}
          keyboardType="phone-pad"
          autoComplete="tel"
          placeholder="+84 912 345 678"
          placeholderTextColor={colors.textMuted}
          accessibilityLabel={t('profile.phone')}
          onSubmitEditing={save}
        />

        <ErrorMessage problem={problem} style={formStyles.error} />
        {done ? (
          <Text style={styles.saved} role="status">
            {t('profile.saved')}
          </Text>
        ) : null}

        <Pressable
          style={[formStyles.button, saving && formStyles.buttonDisabled]}
          onPress={save}
          disabled={saving}
          accessibilityRole="button"
        >
          {saving ? (
            <ActivityIndicator color={colors.textInverse} />
          ) : (
            <Text style={formStyles.buttonText}>{t('profile.save')}</Text>
          )}
        </Pressable>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const makeStyles = (colors) =>
  StyleSheet.create({
    container: { justifyContent: 'flex-start' },
    pictureRow: { alignItems: 'center', flexDirection: 'row', marginBottom: spacing.sm },
    pictureButtons: { marginLeft: spacing.lg },
    remove: { color: colors.danger, marginTop: spacing.sm },
    readOnly: { backgroundColor: colors.background, color: colors.textMuted },
    saved: { color: colors.primary, fontSize: 15, fontWeight: '600', marginTop: spacing.md },
  });
