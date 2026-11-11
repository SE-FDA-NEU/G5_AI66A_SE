/**
 * /about: what the app is for and whom it serves, what it is built with and which version runs
 * (US19). Open from the menu, or from the welcome screen before signing in.
 */

import { useEffect, useState } from 'react';
import { Linking, Pressable, ScrollView, StyleSheet, Text, View } from 'react-native';

import pkg from '../../package.json';
import { api } from '../api/client';
import { useLanguage } from '../i18n/LanguageContext';
import { radius, spacing, useStyles } from '../theme';
import appConfig from '../../app.json';

export const SOURCE_URL = 'https://github.com/SE-FDA-NEU/G5_AI66A_SE';

/** "~54.0.37" -> "54.0.37": the version range of package.json, as installed. Pure. */
export function plainVersion(range) {
  return String(range ?? '').replace(/^[~^]/, '');
}

export default function AboutScreen() {
  const styles = useStyles(makeStyles);
  const { t } = useLanguage();
  const [server, setServer] = useState(null);

  useEffect(() => {
    let cancelled = false;
    api.health().then((answer) => {
      if (!cancelled) setServer(answer);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  const rows = [
    [t('about.version'), appConfig.expo.version],
    ['Expo SDK', plainVersion(pkg.dependencies.expo)],
    ['React Native', plainVersion(pkg.dependencies['react-native'])],
    ['React', plainVersion(pkg.dependencies.react)],
    [t('about.server'), server ? `${server.status} · ${server.version}` : '…'],
  ];

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.container}>
      <Text style={styles.heading}>{t('app.title')}</Text>
      <Text style={styles.body}>{t('about.purpose')}</Text>
      <Text style={styles.body}>{t('about.features')}</Text>
      <Text style={styles.body}>{t('about.privacy')}</Text>

      <Text style={styles.section}>{t('about.builtWith')}</Text>
      <View style={styles.card}>
        {rows.map(([label, value]) => (
          <View key={label} style={styles.row}>
            <Text style={styles.label}>{label}</Text>
            <Text style={styles.value}>{value}</Text>
          </View>
        ))}
        <View style={styles.row}>
          <Text style={styles.label}>Backend</Text>
          <Text style={styles.value}>FastAPI · PostgreSQL</Text>
        </View>
      </View>

      <Text style={styles.section}>{t('about.team')}</Text>
      <Text style={styles.body}>{t('about.teamName')}</Text>
      <Pressable onPress={() => Linking.openURL(SOURCE_URL)} accessibilityRole="link">
        <Text style={styles.link}>
          {t('about.source')}: {SOURCE_URL.replace('https://', '')}
        </Text>
      </Pressable>
    </ScrollView>
  );
}

const makeStyles = (colors) =>
  StyleSheet.create({
    screen: { backgroundColor: colors.background, flex: 1 },
    container: { alignSelf: 'center', maxWidth: 640, padding: spacing.lg, width: '100%' },
    heading: { color: colors.text, fontSize: 24, fontWeight: '800', marginBottom: spacing.md },
    body: { color: colors.text, fontSize: 16, lineHeight: 24, marginBottom: spacing.md },
    section: {
      color: colors.textMuted,
      fontSize: 13,
      fontWeight: '700',
      marginBottom: spacing.sm,
      marginTop: spacing.md,
      textTransform: 'uppercase',
    },
    card: {
      backgroundColor: colors.surface,
      borderColor: colors.border,
      borderRadius: radius.md,
      borderWidth: 1,
      paddingHorizontal: spacing.md,
    },
    row: {
      borderBottomColor: colors.border,
      borderBottomWidth: StyleSheet.hairlineWidth,
      flexDirection: 'row',
      justifyContent: 'space-between',
      paddingVertical: spacing.sm + 2,
    },
    label: { color: colors.textMuted, fontSize: 15 },
    value: { color: colors.text, fontSize: 15, fontWeight: '600' },
    link: { color: colors.primary, fontSize: 15, fontWeight: '600', marginBottom: spacing.xl },
  });
