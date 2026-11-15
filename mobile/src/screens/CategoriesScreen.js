/**
 * /categories: every category with what the account put in it, this month and in all (US17).
 * The kinds of spending first, then the kinds of money received. A tap opens /categories/:id.
 *
 * A search box filters the list as you type, without capitals or accents ("an uong" finds
 * "Ăn uống"). At the end, the account can add a category of its own for what "Other" does not
 * say, such as Coffee (BR17); the API checks the name and the form shows its answer.
 */

import { useFocusEffect } from '@react-navigation/native';
import { useCallback, useState } from 'react';
import {
  ActivityIndicator,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  TextInput,
  useWindowDimensions,
  View,
} from 'react-native';

import { api } from '../api/client';
import ErrorMessage from '../components/ErrorMessage';
import { useFormStyles } from '../components/formStyles';
import MainLayout from '../components/MainLayout';
import Segmented from '../components/Segmented';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { describeError } from '../i18n/translate';
import { radius, spacing, useStyles, useTheme } from '../theme';
import { categoryName, matchesSearch } from '../utils/categories';
import { formatDong } from '../utils/format';

export default function CategoriesScreen({ navigation }) {
  const styles = useStyles(makeStyles);
  const formStyles = useFormStyles();
  const { colors } = useTheme();
  const { signOut } = useAuth();
  const { language, t } = useLanguage();
  // On a phone the two amounts sit one above the other, so the name keeps its width.
  const narrow = useWindowDimensions().width < 520;
  const [rows, setRows] = useState(null);
  const [error, setError] = useState(null);
  const [query, setQuery] = useState('');
  // The form that adds a category of the account's own (BR17).
  const [newName, setNewName] = useState('');
  const [newKind, setNewKind] = useState('expense');
  const [adding, setAdding] = useState(false);
  const [addError, setAddError] = useState(null);
  const [added, setAdded] = useState(null);

  const load = useCallback(
    () =>
      api
        .categorySpending()
        .then((answer) => {
          setRows(answer);
          setError(null);
        })
        .catch((err) => {
          if (err.status === 401) signOut();
          else setError(err);
        }),
    [signOut],
  );

  useFocusEffect(
    useCallback(() => {
      load();
    }, [load]),
  );

  async function addCategory() {
    setAddError(null);
    setAdded(null);
    if (!newName.trim()) {
      setAddError({ key: 'error.categoryNameLength' });
      return;
    }
    setAdding(true);
    try {
      const category = await api.addCategory(newName, newKind);
      setAdded(category.name);
      setNewName('');
      // The search shows the new category at once, with its "Yours" badge, near the form.
      setQuery(category.name);
      await load();
    } catch (err) {
      if (err.status === 401) signOut();
      else setAddError(err);
    } finally {
      setAdding(false);
    }
  }

  if (rows === null && error === null) {
    return (
      <MainLayout current="Categories">
        <View style={styles.center}>
          <ActivityIndicator size="large" color={colors.primary} />
          <Text style={styles.muted}>{t('categories.loading')}</Text>
        </View>
      </MainLayout>
    );
  }

  const shown = (rows ?? []).filter((row) => matchesSearch(categoryName(row.category, t), query));

  const section = (kind, title) => {
    const inKind = shown.filter((row) => row.category.kind === kind);
    if (inKind.length === 0) return null;
    return (
      <View style={styles.section}>
        <Text style={styles.sectionTitle}>{title}</Text>
        {inKind.map((row) => (
          <Pressable
            key={row.category.id}
            style={({ hovered }) => [styles.row, hovered && styles.rowHovered]}
            onPress={() => navigation.navigate('Category', { id: row.category.id })}
            accessibilityRole="button"
          >
            <View style={styles.left}>
              <View style={styles.nameLine}>
                <Text style={styles.name}>{categoryName(row.category, t)}</Text>
                {row.category.custom ? (
                  <Text style={styles.badge}>{t('categories.mine')}</Text>
                ) : null}
              </View>
              <Text style={styles.muted}>
                {row.count > 0
                  ? t('categories.entries', { count: row.count })
                  : t('categories.unused')}
              </Text>
            </View>
            {narrow ? (
              <View style={styles.rightNarrow}>
                <Text style={[styles.amount, kind === 'income' ? styles.in : styles.out]}>
                  <Text style={styles.label}>{t('categories.thisMonth')} </Text>
                  {formatDong(row.this_month, language)}
                </Text>
                <Text style={styles.total}>
                  <Text style={styles.label}>{t('categories.allTime')} </Text>
                  {formatDong(row.all_time, language)}
                </Text>
              </View>
            ) : (
              <>
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
              </>
            )}
            <Text style={styles.chevron}>›</Text>
          </Pressable>
        ))}
      </View>
    );
  };

  return (
    <MainLayout current="Categories">
      <ScrollView
        style={styles.screen}
        contentContainerStyle={styles.container}
        keyboardShouldPersistTaps="handled"
      >
        <ErrorMessage problem={describeError(error, t, api.baseUrl)} />
        <Text style={styles.intro}>{t('categories.intro')}</Text>

        <View style={styles.search}>
          <Text style={styles.searchIcon}>⌕</Text>
          <TextInput
            style={styles.searchInput}
            value={query}
            onChangeText={setQuery}
            placeholder={t('categories.search')}
            placeholderTextColor={colors.textMuted}
            accessibilityLabel={t('categories.search')}
            autoCorrect={false}
            role="searchbox"
          />
          {query ? (
            <Pressable onPress={() => setQuery('')} accessibilityRole="button" accessibilityLabel="×">
              <Text style={styles.clear}>×</Text>
            </Pressable>
          ) : null}
        </View>

        {section('expense', t('categories.spending'))}
        {section('income', t('categories.income'))}
        {rows && shown.length === 0 ? (
          <Text style={styles.noMatch}>{t('categories.noMatch', { query: query.trim() })}</Text>
        ) : null}

        <View style={styles.card}>
          <Text style={styles.cardTitle}>{t('categories.addTitle')}</Text>
          <Text style={formStyles.help}>{t('categories.addHelp')}</Text>
          <View style={styles.kind}>
            <Segmented
              options={[
                { value: 'expense', label: t('categories.spending') },
                { value: 'income', label: t('categories.income') },
              ]}
              value={newKind}
              onChange={setNewKind}
            />
          </View>
          <Text style={formStyles.label}>{t('categories.addName')}</Text>
          <View style={styles.addRow}>
            <TextInput
              style={[formStyles.input, styles.addInput]}
              value={newName}
              onChangeText={(text) => {
                setNewName(text);
                setAdded(null);
              }}
              maxLength={60}
              placeholder={t('categories.addPlaceholder')}
              placeholderTextColor={colors.textMuted}
              onSubmitEditing={addCategory}
              accessibilityLabel={t('categories.addName')}
            />
            <Pressable
              style={[styles.addButton, adding && formStyles.buttonDisabled]}
              onPress={addCategory}
              disabled={adding}
              accessibilityRole="button"
            >
              {adding ? (
                <ActivityIndicator color={colors.textInverse} />
              ) : (
                <Text style={formStyles.buttonText}>{t('categories.add')}</Text>
              )}
            </Pressable>
          </View>
          <ErrorMessage
            problem={describeError(addError, t, api.baseUrl)}
            style={formStyles.error}
          />
          {added ? <Text style={styles.added}>{t('categories.added', { name: added })}</Text> : null}
        </View>
      </ScrollView>
    </MainLayout>
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
    search: {
      alignItems: 'center',
      backgroundColor: colors.surface,
      borderColor: colors.border,
      borderRadius: radius.md,
      borderWidth: 1,
      flexDirection: 'row',
      marginBottom: spacing.lg,
      paddingHorizontal: spacing.md,
    },
    searchIcon: { color: colors.textMuted, fontSize: 20, marginRight: spacing.sm },
    searchInput: { color: colors.text, flex: 1, fontSize: 16, paddingVertical: spacing.sm + 2 },
    clear: { color: colors.textMuted, fontSize: 22, paddingHorizontal: spacing.xs },
    noMatch: { color: colors.textMuted, fontSize: 15, marginBottom: spacing.lg },
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
    // Room for "19,850,000 ₫", so this month's amount and the total never run together.
    right: { alignItems: 'flex-end', marginLeft: spacing.lg, minWidth: 112 },
    rightNarrow: { alignItems: 'flex-end', gap: 2, marginLeft: spacing.sm },
    nameLine: { alignItems: 'center', flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm },
    name: { color: colors.text, fontSize: 16, fontWeight: '600' },
    badge: {
      backgroundColor: colors.primaryLight,
      borderRadius: radius.sm,
      color: colors.primary,
      fontSize: 11,
      fontWeight: '700',
      overflow: 'hidden',
      paddingHorizontal: spacing.xs + 2,
      paddingVertical: 1,
    },
    muted: { color: colors.textMuted, fontSize: 13, marginTop: 2 },
    label: { color: colors.textMuted, fontSize: 12, fontWeight: '400' },
    amount: { fontSize: 15, fontWeight: '700' },
    out: { color: colors.spent },
    in: { color: colors.received },
    total: { color: colors.text, fontSize: 15, fontWeight: '600' },
    chevron: { color: colors.textMuted, fontSize: 24, marginLeft: spacing.sm },
    card: {
      backgroundColor: colors.surface,
      borderColor: colors.border,
      borderRadius: radius.md,
      borderWidth: 1,
      marginBottom: spacing.lg,
      padding: spacing.md,
    },
    cardTitle: { color: colors.text, fontSize: 16, fontWeight: '700' },
    kind: { marginTop: spacing.md },
    addRow: { alignItems: 'stretch', flexDirection: 'row', gap: spacing.sm },
    addInput: { flex: 1 },
    addButton: {
      alignItems: 'center',
      backgroundColor: colors.primary,
      borderRadius: radius.sm,
      justifyContent: 'center',
      minWidth: 88,
      paddingHorizontal: spacing.md,
    },
    added: { color: colors.received, fontSize: 14, fontWeight: '600', marginTop: spacing.sm },
  });
