/**
 * /welcome: the first screen of someone signed out (US15). A picture and one sentence say what the
 * app is for; then three choices: Sign in, Create an account, and the language. Only after a
 * choice does a form appear (/login or /register).
 *
 * The layout follows the screen's shape, not the device: wider than it is tall, from 720 pixels,
 * the picture sits on the left and the choices on the right (a laptop, a phone or a tablet held
 * sideways); otherwise the picture sits on top (a phone held upright, a narrow window).
 */

import { Image, Pressable, ScrollView, StyleSheet, Text, useWindowDimensions, View } from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';

import welcomePicture from '../../assets/welcome.png';
import Segmented from '../components/Segmented';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { LANGUAGE_NAMES, LANGUAGES } from '../i18n/translate';
import { radius, spacing, useStyles } from '../theme';

// The picture is drawn at 1200 × 900.
const PICTURE_RATIO = 4 / 3;

/** "side" when the choices go beside the picture, "stack" when they go under it. Pure. */
export function welcomeLayout(width, height) {
  return width > height && width >= 720 ? 'side' : 'stack';
}

export default function WelcomeScreen({ navigation }) {
  const styles = useStyles(makeStyles);
  const { language, setLanguage, t } = useLanguage();
  const { notice, clearNotice } = useAuth();
  const { width, height } = useWindowDimensions();
  const insets = useSafeAreaInsets();
  const side = welcomeLayout(width, height) === 'side';

  const go = (screen) => {
    clearNotice();
    navigation.navigate(screen);
  };

  // Upright, the picture takes the width but never more than 40% of the height, so the buttons
  // stay in view without scrolling on a small phone.
  const pictureStyle = side
    ? { aspectRatio: PICTURE_RATIO, width: '100%' }
    : { aspectRatio: PICTURE_RATIO, maxHeight: height * 0.4, width: '100%' };

  return (
    <ScrollView
      style={styles.screen}
      contentContainerStyle={[
        styles.container,
        side ? styles.containerSide : styles.containerStack,
        { paddingTop: insets.top + spacing.lg, paddingBottom: insets.bottom + spacing.lg },
      ]}
    >
      <View style={side ? styles.pictureSide : styles.pictureStack}>
        <Image
          source={welcomePicture}
          style={[styles.picture, pictureStyle]}
          resizeMode="contain"
          accessibilityLabel={t('welcome.imageLabel')}
          alt={t('welcome.imageLabel')}
        />
      </View>

      <View style={side ? styles.panelSide : styles.panelStack}>
        <Text style={styles.app}>{t('app.title')}</Text>
        <Text style={styles.heading} role="heading">
          {t('welcome.heading')}
        </Text>
        <Text style={styles.body}>{t('welcome.body')}</Text>

        {notice ? (
          <View style={styles.notice} role="status">
            <Text style={styles.noticeText}>{t(notice)}</Text>
          </View>
        ) : null}

        <Pressable style={styles.primary} onPress={() => go('Login')} accessibilityRole="button">
          <Text style={styles.primaryText}>{t('welcome.signIn')}</Text>
        </Pressable>
        <Pressable
          style={styles.secondary}
          onPress={() => go('Register')}
          accessibilityRole="button"
        >
          <Text style={styles.secondaryText}>{t('welcome.register')}</Text>
        </Pressable>

        <Text style={styles.label}>{t('welcome.language')}</Text>
        <Segmented
          label={t('welcome.language')}
          value={language}
          onChange={setLanguage}
          options={LANGUAGES.map((code) => ({ value: code, label: LANGUAGE_NAMES[code] }))}
        />

        <Pressable onPress={() => go('About')} accessibilityRole="link" style={styles.aboutLink}>
          <Text style={styles.link}>{t('welcome.about')}</Text>
        </Pressable>
      </View>
    </ScrollView>
  );
}

const makeStyles = (colors) =>
  StyleSheet.create({
    screen: { backgroundColor: colors.background, flex: 1 },
    container: { flexGrow: 1, paddingHorizontal: spacing.lg },
    containerSide: {
      alignItems: 'center',
      alignSelf: 'center',
      flexDirection: 'row',
      maxWidth: 1180,
      width: '100%',
    },
    containerStack: { alignItems: 'center' },
    pictureSide: { flex: 1.15, paddingRight: spacing.xl },
    pictureStack: { alignItems: 'center', maxWidth: 520, width: '100%' },
    picture: { borderRadius: radius.md },
    panelSide: { flex: 1, maxWidth: 440 },
    panelStack: { maxWidth: 480, paddingTop: spacing.lg, width: '100%' },
    app: {
      color: colors.primary,
      fontSize: 14,
      fontWeight: '700',
      letterSpacing: 0.5,
      textTransform: 'uppercase',
    },
    heading: {
      color: colors.text,
      fontSize: 30,
      fontWeight: '800',
      lineHeight: 36,
      marginTop: spacing.sm,
    },
    body: {
      color: colors.textMuted,
      fontSize: 16,
      lineHeight: 24,
      marginBottom: spacing.lg,
      marginTop: spacing.sm,
    },
    notice: {
      backgroundColor: colors.primaryLight,
      borderRadius: radius.sm,
      marginBottom: spacing.md,
      padding: spacing.md,
    },
    noticeText: { color: colors.text, fontSize: 15 },
    primary: {
      alignItems: 'center',
      backgroundColor: colors.primary,
      borderRadius: radius.sm,
      paddingVertical: spacing.md,
    },
    primaryText: { color: colors.textInverse, fontSize: 16, fontWeight: '700' },
    secondary: {
      alignItems: 'center',
      borderColor: colors.primary,
      borderRadius: radius.sm,
      borderWidth: 2,
      marginTop: spacing.sm,
      paddingVertical: spacing.md - 2,
    },
    secondaryText: { color: colors.primary, fontSize: 16, fontWeight: '700' },
    label: {
      color: colors.textMuted,
      fontSize: 13,
      fontWeight: '600',
      marginBottom: spacing.sm,
      marginTop: spacing.lg,
      textTransform: 'uppercase',
    },
    aboutLink: { alignSelf: 'center', marginTop: spacing.lg, padding: spacing.sm },
    link: { color: colors.primary, fontSize: 15, fontWeight: '600' },
  });
