/**
 * /transactions/new: write down one amount spent or received, in seconds (US03).
 *
 * The amount field has the focus when the screen opens, the date is today unless changed, and a
 * kind of spending is one tap, so an entry takes a few seconds. The API checks every rule, BR5,
 * BR6 and BR11, and this screen shows its answer under the form; nothing is stored when one is
 * broken. After a save the overview shows the new totals and the entry at the top of the list.
 */

import { useCallback, useEffect, useState } from 'react';
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
import ErrorMessage from '../components/ErrorMessage';
import { formStyles } from '../components/formStyles';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { describeError } from '../i18n/translate';
import { colors, radius, spacing } from '../theme';
import { dayBefore, parseAmount, parseDateInput, todayIso } from '../utils/entryForm';
import { formatDate } from '../utils/format';

const KINDS = [
  { kind: 'expense', label: 'newEntry.spent' },
  { kind: 'income', label: 'newEntry.received' },
];

export default function NewEntryScreen({ navigation }) {
  const { signOut } = useAuth();
  const { t } = useLanguage();
  const [kind, setKind] = useState('expense');
  const [amountText, setAmountText] = useState('');
  const [categoryId, setCategoryId] = useState(null);
  const [note, setNote] = useState('');
  const [dateText, setDateText] = useState(formatDate(todayIso()));
  // The picker's categories: null while they load, then the list from GET /api/categories.
  const [categories, setCategories] = useState(null);
  const [loadError, setLoadError] = useState(null);
  // Like every form: { key } for this screen's own message, or the error the API client threw.
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  const handleApiError = useCallback(
    async (err, show) => {
      // BR10: the sign-in has expired, so back to /login.
      if (err.status === 401) {
        await signOut();
        return;
      }
      show(err);
    },
    [signOut],
  );

  const loadCategories = useCallback(async () => {
    setLoadError(null);
    setCategories(null);
    try {
      setCategories(await api.categories());
    } catch (err) {
      await handleApiError(err, setLoadError);
    }
  }, [handleApiError]);

  useEffect(() => {
    loadCategories();
  }, [loadCategories]);

  function chooseKind(next) {
    setKind(next);
    // A kind of spending belongs to money spent, Salary to money received (BR6).
    setCategoryId(null);
  }

  function leave() {
    if (navigation.canGoBack()) navigation.goBack();
    else navigation.replace('Overview');
  }

  async function save() {
    setError(null);
    const amount = parseAmount(amountText);
    if (Number.isNaN(amount)) {
      setError({ key: 'error.amountNotPositive' });
      return;
    }
    const occurredOn = parseDateInput(dateText);
    if (!occurredOn) {
      setError({ key: 'newEntry.badDate' });
      return;
    }

    setSaving(true);
    try {
      await api.createEntry({
        kind,
        amount,
        note,
        occurred_on: occurredOn,
        category_id: categoryId,
      });
      // US04: the overview reloads when it comes back into view, with the new totals.
      leave();
    } catch (err) {
      setSaving(false);
      await handleApiError(err, setError);
    }
  }

  const problem = describeError(error, t, api.baseUrl);
  const loadProblem = describeError(loadError, t, api.baseUrl);
  const choices = (categories ?? []).filter((category) => category.kind === kind);
  const today = todayIso();

  return (
    <KeyboardAvoidingView
      style={formStyles.flex}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView
        contentContainerStyle={[formStyles.container, styles.container]}
        keyboardShouldPersistTaps="handled"
      >
        <View style={styles.segment} role="radiogroup">
          {KINDS.map((option) => {
            const selected = option.kind === kind;
            return (
              <Pressable
                key={option.kind}
                style={[styles.segmentOption, selected && styles.segmentSelected]}
                onPress={() => chooseKind(option.kind)}
                role="radio"
                aria-checked={selected}
              >
                <Text style={[styles.segmentText, selected && styles.segmentTextSelected]}>
                  {t(option.label)}
                </Text>
              </Pressable>
            );
          })}
        </View>

        <Text style={formStyles.label}>{t('newEntry.amount')}</Text>
        <TextInput
          style={[formStyles.input, styles.amount]}
          value={amountText}
          onChangeText={setAmountText}
          keyboardType="number-pad"
          autoFocus
          accessibilityLabel={t('newEntry.amount')}
        />

        <Text style={formStyles.label}>
          {t(kind === 'income' ? 'newEntry.kindOfIncome' : 'newEntry.kindOfSpending')}
        </Text>
        {categories === null && !loadError ? (
          <View style={styles.loadingRow}>
            <ActivityIndicator color={colors.primary} />
            <Text style={formStyles.help}>{t('newEntry.loading')}</Text>
          </View>
        ) : null}
        {loadProblem ? (
          <View>
            <ErrorMessage problem={loadProblem} />
            <Pressable onPress={loadCategories} accessibilityRole="button">
              <Text style={formStyles.link}>{t('newEntry.tryAgain')}</Text>
            </Pressable>
          </View>
        ) : null}
        <View style={styles.chips}>
          {choices.map((category) => {
            const selected = category.id === categoryId;
            return (
              <Pressable
                key={category.id}
                style={[styles.chip, selected && styles.chipSelected]}
                // Tapping the chosen kind again clears it: none is allowed (BR6).
                onPress={() => setCategoryId(selected ? null : category.id)}
                role="radio"
                aria-checked={selected}
              >
                <Text style={[styles.chipText, selected && styles.chipTextSelected]}>
                  {t(`category.${category.name}`)}
                </Text>
              </Pressable>
            );
          })}
        </View>
        {choices.length > 0 ? (
          <Text style={formStyles.help}>{t('newEntry.kindOptional')}</Text>
        ) : null}

        <Text style={formStyles.label}>{t('newEntry.note')}</Text>
        <TextInput
          style={formStyles.input}
          value={note}
          onChangeText={setNote}
          maxLength={200}
          placeholder={t('newEntry.notePlaceholder')}
          placeholderTextColor={colors.textMuted}
          accessibilityLabel={t('newEntry.note')}
        />

        <Text style={formStyles.label}>{t('newEntry.date')}</Text>
        <TextInput
          style={formStyles.input}
          value={dateText}
          onChangeText={setDateText}
          placeholder="12/11/2026"
          placeholderTextColor={colors.textMuted}
          onSubmitEditing={save}
          accessibilityLabel={t('newEntry.date')}
        />
        <View style={styles.chips}>
          <Pressable style={styles.chip} onPress={() => setDateText(formatDate(today))}>
            <Text style={styles.chipText}>{t('newEntry.today')}</Text>
          </Pressable>
          <Pressable style={styles.chip} onPress={() => setDateText(formatDate(dayBefore(today)))}>
            <Text style={styles.chipText}>{t('newEntry.yesterday')}</Text>
          </Pressable>
        </View>

        <ErrorMessage problem={problem} style={formStyles.error} />

        <Pressable
          style={[formStyles.button, saving && formStyles.buttonDisabled]}
          onPress={save}
          disabled={saving}
          accessibilityRole="button"
        >
          {saving ? (
            <ActivityIndicator color={colors.textInverse} />
          ) : (
            <Text style={formStyles.buttonText}>{t('newEntry.save')}</Text>
          )}
        </Pressable>
        <Pressable style={styles.cancel} onPress={leave} accessibilityRole="button">
          <Text style={formStyles.link}>{t('newEntry.cancel')}</Text>
        </Pressable>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  // A long form starts at the top instead of in the middle of the page.
  container: { justifyContent: 'flex-start' },
  segment: {
    borderColor: colors.primary,
    borderRadius: radius.sm,
    borderWidth: 1,
    flexDirection: 'row',
    overflow: 'hidden',
  },
  segmentOption: { alignItems: 'center', flex: 1, paddingVertical: spacing.sm },
  segmentSelected: { backgroundColor: colors.primary },
  segmentText: { color: colors.primary, fontSize: 15, fontWeight: '600' },
  segmentTextSelected: { color: colors.textInverse },
  amount: { fontSize: 22, fontWeight: '700' },
  loadingRow: { alignItems: 'center', flexDirection: 'row', gap: spacing.sm },
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginTop: spacing.xs },
  chip: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderRadius: radius.md,
    borderWidth: 1,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
  },
  chipSelected: { backgroundColor: colors.primaryLight, borderColor: colors.primary },
  chipText: { color: colors.text, fontSize: 14 },
  chipTextSelected: { color: colors.primary, fontWeight: '700' },
  cancel: { alignItems: 'center', marginTop: spacing.md, padding: spacing.sm },
});
