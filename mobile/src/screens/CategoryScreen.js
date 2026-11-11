/**
 * /categories/:id: one category for the signed-in account (US17). How much went into it this
 * month and in all, the last six months as bars, and its ten newest entries; a tap on an entry
 * opens it to correct or remove (US06).
 */

import { useFocusEffect } from '@react-navigation/native';
import { useCallback, useState } from 'react';
import { ActivityIndicator, ScrollView, StyleSheet, Text, View } from 'react-native';

import { api } from '../api/client';
import EntryRow from '../components/EntryRow';
import ErrorMessage from '../components/ErrorMessage';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { describeError } from '../i18n/translate';
import { radius, spacing, useStyles, useTheme } from '../theme';
import { formatDong, formatMonth } from '../utils/format';

export default function CategoryScreen({ navigation, route }) {
  const styles = useStyles(makeStyles);
  const { colors } = useTheme();
  const { signOut } = useAuth();
  const { language, t } = useLanguage();
  const id = Number(route.params?.id);
  const [detail, setDetail] = useState(null);
  const [error, setError] = useState(null);

  useFocusEffect(
    useCallback(() => {
      let cancelled = false;
      api
        .categoryDetail(id)
        .then((answer) => {
          if (cancelled) return;
          setDetail(answer);
          setError(null);
          navigation.setOptions({ title: t(`category.${answer.category.name}`) });
        })
        .catch((err) => {
          if (cancelled) return;
          if (err.status === 401) signOut();
          else setError(err);
        });
      return () => {
        cancelled = true;
      };
    }, [id, navigation, signOut, t]),
  );

  if (detail === null && error === null) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }
  if (detail === null) {
    return (
      <View style={styles.center}>
        <View style={styles.narrow}>
          <ErrorMessage problem={describeError(error, t, api.baseUrl)} />
        </View>
      </View>
    );
  }

  const received = detail.category.kind === 'income';
  const highest = Math.max(1, ...detail.months.map((m) => m.amount));

  return (
    <ScrollView style={styles.screen} contentContainerStyle={styles.container}>
      <View style={styles.cards}>
        <View style={styles.card}>
          <Text style={styles.label}>{t('categories.thisMonth')}</Text>
          <Text style={[styles.big, received ? styles.in : styles.out]}>
            {formatDong(detail.this_month, language)}
          </Text>
        </View>
        <View style={styles.card}>
          <Text style={styles.label}>{t('categories.allTime')}</Text>
          <Text style={styles.big}>{formatDong(detail.all_time, language)}</Text>
          <Text style={styles.muted}>{t('categories.entries', { count: detail.count })}</Text>
        </View>
      </View>

      <Text style={styles.title}>{t('category.months')}</Text>
      <View style={styles.card}>
        {detail.months.map((m) => (
          <View key={m.month} style={styles.barRow}>
            <Text style={styles.barMonth}>{formatMonth(m.month)}</Text>
            <View style={styles.barTrack}>
              <View
                style={[
                  styles.bar,
                  received ? styles.barIn : styles.barOut,
                  { width: `${(m.amount / highest) * 100}%` },
                ]}
              />
            </View>
            <Text style={styles.barAmount}>{formatDong(m.amount, language)}</Text>
          </View>
        ))}
      </View>

      <Text style={styles.title}>{t('category.recent')}</Text>
      {detail.recent.length === 0 ? (
        <Text style={styles.muted}>{t('category.none')}</Text>
      ) : (
        detail.recent.map((entry) => (
          <EntryRow
            key={entry.id}
            entry={entry}
            onPress={() => navigation.navigate('EditEntry', { id: entry.id })}
          />
        ))
      )}
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
      padding: spacing.lg,
    },
    narrow: { maxWidth: 480, width: '100%' },
    cards: { flexDirection: 'row', gap: spacing.sm },
    card: {
      backgroundColor: colors.surface,
      borderColor: colors.border,
      borderRadius: radius.md,
      borderWidth: 1,
      flex: 1,
      marginBottom: spacing.sm,
      padding: spacing.md,
    },
    label: { color: colors.textMuted, fontSize: 13 },
    big: { color: colors.text, fontSize: 22, fontWeight: '800', marginTop: spacing.xs },
    out: { color: colors.spent },
    in: { color: colors.received },
    muted: { color: colors.textMuted, fontSize: 13, marginTop: spacing.xs },
    title: {
      color: colors.textMuted,
      fontSize: 13,
      fontWeight: '700',
      marginBottom: spacing.sm,
      marginTop: spacing.md,
      textTransform: 'uppercase',
    },
    barRow: { alignItems: 'center', flexDirection: 'row', marginVertical: spacing.xs },
    barMonth: { color: colors.textMuted, fontSize: 13, width: 64 },
    barTrack: {
      backgroundColor: colors.background,
      borderRadius: radius.sm,
      flex: 1,
      height: 14,
      overflow: 'hidden',
    },
    bar: { borderRadius: radius.sm, height: '100%' },
    barOut: { backgroundColor: colors.spent },
    barIn: { backgroundColor: colors.received },
    barAmount: { color: colors.text, fontSize: 13, textAlign: 'right', width: 110 },
  });
