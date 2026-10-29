/**
 * /debts/new: write down one debt or loan (US13). Which way the money went, who it is with, how
 * much, the day it changed hands (today unless changed) and, if one was agreed, when it is due.
 *
 * The API checks BR13 (a name of 1 to 60 characters, a due date not before the start), BR5 and
 * BR11, and this screen shows its answer under the form; nothing is stored when one is broken.
 */

import { useState } from 'react';
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
import { addDays } from '../utils/debts';
import { dayBefore, parseAmount, parseDateInput, todayIso } from '../utils/entryForm';
import { formatDate } from '../utils/format';

const DIRECTIONS = [
  { direction: 'lent', label: 'newDebt.lent' },
  { direction: 'borrowed', label: 'newDebt.borrowed' },
];

export default function NewDebtScreen({ navigation }) {
  const { signOut } = useAuth();
  const { t } = useLanguage();
  const today = todayIso();
  const [direction, setDirection] = useState('lent');
  const [person, setPerson] = useState('');
  const [amountText, setAmountText] = useState('');
  const [startText, setStartText] = useState(formatDate(today));
  const [dueText, setDueText] = useState('');
  const [note, setNote] = useState('');
  const [error, setError] = useState(null);
  const [saving, setSaving] = useState(false);

  function leave() {
    if (navigation.canGoBack()) navigation.goBack();
    else navigation.replace('Debts');
  }

  async function save() {
    setError(null);
    const amount = parseAmount(amountText);
    if (Number.isNaN(amount)) {
      setError({ key: 'error.amountNotPositive' });
      return;
    }
    const startedOn = parseDateInput(startText);
    // An empty due date means none was agreed; anything else must be a real day.
    const dueOn = dueText.trim() === '' ? null : parseDateInput(dueText);
    if (!startedOn || (dueText.trim() !== '' && !dueOn)) {
      setError({ key: 'newEntry.badDate' });
      return;
    }

    setSaving(true);
    try {
      await api.addDebt({
        direction,
        person,
        amount,
        note,
        started_on: startedOn,
        due_on: dueOn,
      });
      leave();
    } catch (err) {
      setSaving(false);
      // BR10: the sign-in has expired, so back to /login.
      if (err.status === 401) {
        await signOut();
        return;
      }
      setError(err);
    }
  }

  const problem = describeError(error, t, api.baseUrl);
  const start = parseDateInput(startText) ?? today;

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
          {DIRECTIONS.map((option) => {
            const selected = option.direction === direction;
            return (
              <Pressable
                key={option.direction}
                style={[styles.segmentOption, selected && styles.segmentSelected]}
                onPress={() => setDirection(option.direction)}
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

        <Text style={formStyles.label}>
          {t(direction === 'lent' ? 'newDebt.lentTo' : 'newDebt.borrowedFrom')}
        </Text>
        <TextInput
          style={formStyles.input}
          value={person}
          onChangeText={setPerson}
          autoFocus
          placeholder="Lan"
          placeholderTextColor={colors.textMuted}
          accessibilityLabel={t(direction === 'lent' ? 'newDebt.lentTo' : 'newDebt.borrowedFrom')}
        />
        <Text style={formStyles.help}>{t('newDebt.personHelp')}</Text>

        <Text style={formStyles.label}>{t('newEntry.amount')}</Text>
        <TextInput
          style={[formStyles.input, styles.amount]}
          value={amountText}
          onChangeText={setAmountText}
          keyboardType="number-pad"
          accessibilityLabel={t('newEntry.amount')}
        />

        <Text style={formStyles.label}>{t('newDebt.started')}</Text>
        <TextInput
          style={formStyles.input}
          value={startText}
          onChangeText={setStartText}
          placeholder="24/10/2026"
          placeholderTextColor={colors.textMuted}
          accessibilityLabel={t('newDebt.started')}
        />
        <View style={styles.chips}>
          <Chip label={t('newEntry.today')} onPress={() => setStartText(formatDate(today))} />
          <Chip
            label={t('newEntry.yesterday')}
            onPress={() => setStartText(formatDate(dayBefore(today)))}
          />
        </View>

        <Text style={formStyles.label}>{t('newDebt.due')}</Text>
        <TextInput
          style={formStyles.input}
          value={dueText}
          onChangeText={setDueText}
          placeholder={t('newDebt.duePlaceholder')}
          placeholderTextColor={colors.textMuted}
          accessibilityLabel={t('newDebt.due')}
        />
        <View style={styles.chips}>
          <Chip label={t('newDebt.inAWeek')} onPress={() => setDueText(formatDate(addDays(start, 7)))} />
          <Chip
            label={t('newDebt.inAMonth')}
            onPress={() => setDueText(formatDate(addDays(start, 30)))}
          />
          <Chip label={t('newDebt.noDue')} onPress={() => setDueText('')} />
        </View>

        <Text style={formStyles.label}>{t('newEntry.note')}</Text>
        <TextInput
          style={formStyles.input}
          value={note}
          onChangeText={setNote}
          maxLength={200}
          placeholder={t('newDebt.notePlaceholder')}
          placeholderTextColor={colors.textMuted}
          onSubmitEditing={save}
          accessibilityLabel={t('newEntry.note')}
        />

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

function Chip({ label, onPress }) {
  return (
    <Pressable style={styles.chip} onPress={onPress}>
      <Text style={styles.chipText}>{label}</Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
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
  chips: { flexDirection: 'row', flexWrap: 'wrap', gap: spacing.sm, marginTop: spacing.xs },
  chip: {
    backgroundColor: colors.surface,
    borderColor: colors.border,
    borderRadius: radius.md,
    borderWidth: 1,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.xs,
  },
  chipText: { color: colors.text, fontSize: 14 },
  cancel: { alignItems: 'center', marginTop: spacing.md, padding: spacing.sm },
});
