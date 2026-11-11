/**
 * A row of two or three choices of which one is on, such as Device · Light · Dark in the menu.
 */

import { Pressable, StyleSheet, Text, View } from 'react-native';

import { radius, spacing, useStyles } from '../theme';

export default function Segmented({ options, value, onChange, label }) {
  const styles = useStyles(makeStyles);

  return (
    <View style={styles.row} role="radiogroup" aria-label={label}>
      {options.map((option) => {
        const selected = option.value === value;
        return (
          <Pressable
            key={option.value}
            onPress={() => onChange(option.value)}
            style={[styles.option, selected && styles.selected]}
            role="radio"
            aria-checked={selected}
            aria-label={option.name ?? option.label}
          >
            <Text style={[styles.text, selected && styles.textSelected]}>{option.label}</Text>
          </Pressable>
        );
      })}
    </View>
  );
}

const makeStyles = (colors) =>
  StyleSheet.create({
    row: {
      borderColor: colors.border,
      borderRadius: radius.sm,
      borderWidth: 1,
      flexDirection: 'row',
      overflow: 'hidden',
    },
    option: {
      alignItems: 'center',
      flex: 1,
      paddingHorizontal: spacing.sm,
      paddingVertical: spacing.sm,
    },
    selected: { backgroundColor: colors.primary },
    text: { color: colors.text, fontSize: 14, fontWeight: '600' },
    textSelected: { color: colors.textInverse },
  });
