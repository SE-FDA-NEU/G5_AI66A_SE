/**
 * The frame of the main screens of an account: the screen itself and the tabs that move between
 * them. On a wide screen the tabs sit in a strip under the top bar; on a phone they sit at the
 * bottom, where a thumb reaches them. Every tab is a screen with its own address, so the browser's
 * back button and a typed address still work.
 */

import { useNavigation } from '@react-navigation/native';
import { Pressable, StyleSheet, Text, useWindowDimensions, View } from 'react-native';

import { useLanguage } from '../i18n/LanguageContext';
import { colors, spacing } from '../theme';

export const WIDE = 768;

const TABS = [
  { name: 'Overview', label: 'nav.overview', icon: '◐' },
  { name: 'Stats', label: 'nav.stats', icon: '▥' },
];

export default function MainLayout({ current, children }) {
  const navigation = useNavigation();
  const { t } = useLanguage();
  const { width } = useWindowDimensions();
  const wide = width >= WIDE;

  const tabs = (
    <View style={wide ? styles.strip : styles.bottom} role="tablist">
      {TABS.map((tab) => {
        const selected = tab.name === current;
        return (
          <Pressable
            key={tab.name}
            style={[wide ? styles.stripTab : styles.bottomTab, selected && styles.selected]}
            onPress={() => !selected && navigation.navigate(tab.name)}
            role="tab"
            aria-selected={selected}
          >
            {wide ? null : (
              <Text style={[styles.icon, selected && styles.textSelected]}>{tab.icon}</Text>
            )}
            <Text style={[styles.tabText, selected && styles.textSelected]}>{t(tab.label)}</Text>
          </Pressable>
        );
      })}
    </View>
  );

  return (
    <View style={styles.frame}>
      {wide ? tabs : null}
      <View style={styles.content}>{children}</View>
      {wide ? null : tabs}
    </View>
  );
}

const styles = StyleSheet.create({
  frame: { backgroundColor: colors.background, flex: 1 },
  content: { flex: 1 },
  strip: {
    backgroundColor: colors.surface,
    borderBottomColor: colors.border,
    borderBottomWidth: 1,
    flexDirection: 'row',
    justifyContent: 'center',
    paddingHorizontal: spacing.md,
  },
  stripTab: {
    borderBottomColor: 'transparent',
    borderBottomWidth: 3,
    marginHorizontal: spacing.sm,
    paddingHorizontal: spacing.md,
    paddingVertical: spacing.sm,
  },
  bottom: {
    backgroundColor: colors.surface,
    borderTopColor: colors.border,
    borderTopWidth: 1,
    flexDirection: 'row',
  },
  bottomTab: {
    alignItems: 'center',
    borderTopColor: 'transparent',
    borderTopWidth: 3,
    flex: 1,
    paddingVertical: spacing.xs,
  },
  selected: { borderBottomColor: colors.primary, borderTopColor: colors.primary },
  icon: { color: colors.textMuted, fontSize: 18 },
  tabText: { color: colors.textMuted, fontSize: 14, fontWeight: '600' },
  textSelected: { color: colors.primary },
});
