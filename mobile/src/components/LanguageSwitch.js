/**
 * The language switch in the top bar of every screen (US11): one button per dictionary in
 * strings.js, labelled with its code (EN, VI) and named in its own language for screen readers.
 */

import { Pressable, StyleSheet, Text, View } from 'react-native';

import { LANGUAGE_NAMES, LANGUAGES } from '../i18n/translate';
import { useLanguage } from '../i18n/LanguageContext';
import { colors, radius, spacing } from '../theme';

export default function LanguageSwitch() {
  const { language, setLanguage, t } = useLanguage();

  return (
    <View style={styles.row} role="radiogroup" aria-label={t('language.switch')}>
      {LANGUAGES.map((code) => {
        const selected = code === language;
        return (
          <Pressable
            key={code}
            onPress={() => setLanguage(code)}
            style={[styles.option, selected && styles.optionSelected]}
            role="radio"
            aria-checked={selected}
            aria-label={LANGUAGE_NAMES[code]}
          >
            <Text style={[styles.label, selected && styles.labelSelected]}>
              {code.toUpperCase()}
            </Text>
          </Pressable>
        );
      })}
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    borderColor: colors.textInverse,
    borderRadius: radius.sm,
    borderWidth: 1,
    flexDirection: 'row',
    marginRight: spacing.sm,
    overflow: 'hidden',
  },
  option: { paddingHorizontal: spacing.sm, paddingVertical: spacing.xs },
  optionSelected: { backgroundColor: colors.textInverse },
  label: { color: colors.textInverse, fontSize: 13, fontWeight: '600' },
  labelSelected: { color: colors.primary },
});
