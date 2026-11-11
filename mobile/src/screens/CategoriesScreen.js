/**
 * /categories: every category with what the account put in it, this month and in all (US17).
 * The kinds of spending first, then the kinds of money received. A tap opens /categories/:id.
 */

import { useFocusEffect } from '@react-navigation/native';
import { useCallback, useState } from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  View,
} from 'react-native';

import { api } from '../api/client';
import ErrorMessage from '../components/ErrorMessage';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { describeError } from '../i18n/translate';
import { radius, spacing, useStyles, useTheme } from '../theme';
import { formatDong } from '../utils/format';

export default function CategoriesScreen({ navigation }) {
  const styles = useStyles(makeStyles);
  const { colors } = useTheme();
  const { signOut } = useAuth();
  const { language, t } = useLanguage();
  const [rows, setRows] = useState(null);
  const [error, setError] = useState(null);

  useFocusEffect(
    useCallback(() => {
      let cancelled = false;
      api
        .categorySpending()
        .then((answer) => {
          if (!cancelled) {
            setRows(answer);
            setError(null);
          }
        })
        .catch((err) => {
          if (cancelled) return;
          if (err.status === 401) signOut();
          else setError(err);
        });
      return () => {
        cancelled = true;
      };
    }, [signOut]),
  );

  if (rows === null && error === null) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
        <Text style={styles.muted}>{t('categories.loading')}</Text>
      </View>
    );
  }

  const section = (kind, title) => (
    <View style={styles.section}>
      <Text style={styles.sectionTitle}>{title}</Text>
      {(rows ?? [])
        .filter((row) => row.category.kind === kind)
        .map((row) => (
          <Pressable
            key={row.category.id}
            style={({ hovered }) => [styles.row, hovered && styles.rowHovered]}
            onPress={() => navigation.navigate('Category', { id: row.category.id })}
            accessibilityRole="button"
          >
            <View style={styles.left}>
              <Text style={styles.name}>{t(`category.${row.category.name}`)}</Text>
              <Text style={styles.muted}>
                {row.count > 0
                  ? t('categories.entries', { count: row.count })
                  : t('categories.unused')}
              </Text>
            </View>
            <View style={styles.right}>
              <Text style={styles.label}>{t('categories.thisMonth')}</Text>
              <Text style={[styles.amount, kind === 'income' ? styles.in : styles.out]}>
                {formatDong(row.this_month, language)}
              </Text>
            </View>
            <View style={styles.right}>
              <Text style={styles.label}>{t('categories.allTime')}</Text>
              <Text style={styles.total}>{formatDong(row.all_time, language)}</Text>
            </View>
            <Text style={styles.chevron}>›</Text>
          </Pressable>
        ))}
    </View>
  );

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.container}>
      <ErrorMessage problem={describeError(error, t, api.baseUrl)} />
      <Text style={styles.intro}>{t('categories.intro')}</Text>
      {section('expense', t('categories.spending'))}
      {section('income', t('categories.income'))}
    </ScrollView>
  );
}

const makeStyles = (colors) =>
  StyleSheet.create({
    screen: { backgroundColor: colors.background, flex: 1 },
    container: { alignSelf: 'center', maxWidth: 760, padding: spacing.md, width: '100%' },
    center: {
      alignItems: 'center',
      backgroundColor: colors.background,
      flex: 1,
      justifyContent: 'center',
    },
    intro: { color: colors.textMuted, fontSize: 15, marginBottom: spacing.md },
    section: { marginBottom: spacing.lg },
    sectionTitle: {
      color: colors.textMuted,
      fontSize: 13,
      fontWeight: '700',
      marginBottom: spacing.sm,
      textTransform: 'uppercase',
    },
    row: {
      alignItems: 'center',
      backgroundColor: colors.surface,
      borderColor: colors.border,
      borderRadius: radius.md,
      borderWidth: 1,
      flexDirection: 'row',
      marginBottom: spacing.sm,
      padding: spacing.md,
    },
    rowHovered: { borderColor: colors.primary },
    left: { flex: 1 },
    right: { alignItems: 'flex-end', marginLeft: spacing.md, minWidth: 92 },
    name: { color: colors.text, fontSize: 16, fontWeight: '600' },
    muted: { color: colors.textMuted, fontSize: 13, marginTop: 2 },
    label: { color: colors.textMuted, fontSize: 12 },
    amount: { fontSize: 15, fontWeight: '700' },
    out: { color: colors.spent },
    in: { color: colors.received },
    total: { color: colors.text, fontSize: 15, fontWeight: '600' },
    chevron: { color: colors.textMuted, fontSize: 24, marginLeft: spacing.sm },
  });
