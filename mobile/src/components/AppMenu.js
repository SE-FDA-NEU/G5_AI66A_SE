/**
 * The ☰ button in the top bar of every signed-in screen, and the menu it opens (US16 to US19):
 * the profile, the categories, light or dark, the language, about this app, deleting the
 * account, and signing out. It slides in from the right edge, over a dimmed screen; a tap on the
 * dimmed part, the ✕ or the Escape key closes it.
 */

import { useNavigation } from '@react-navigation/native';
import { useState } from 'react';
import {
  Modal,
  Pressable,
  ScrollView,
  StyleSheet,
  Text,
  useWindowDimensions,
  View,
} from 'react-native';

import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import { LANGUAGE_NAMES, LANGUAGES } from '../i18n/translate';
import { radius, spacing, THEME_CHOICES, useStyles, useTheme } from '../theme';
import { displayName } from '../utils/profile';
import Avatar from './Avatar';
import Segmented from './Segmented';

export const MENU_WIDTH = 340;

export function MenuButton() {
  const styles = useStyles(makeStyles);
  const { t } = useLanguage();
  const [open, setOpen] = useState(false);

  return (
    <>
      <Pressable
        onPress={() => setOpen(true)}
        style={styles.button}
        accessibilityRole="button"
        aria-label={t('menu.open')}
        aria-expanded={open}
      >
        <Text style={styles.burger}>☰</Text>
      </Pressable>
      <AppMenu visible={open} onClose={() => setOpen(false)} />
    </>
  );
}

function Item({ icon, label, onPress, danger }) {
  const styles = useStyles(makeStyles);
  return (
    <Pressable
      onPress={onPress}
      style={({ hovered }) => [styles.item, hovered && styles.itemHovered]}
      accessibilityRole="button"
    >
      <Text style={[styles.icon, danger && styles.danger]}>{icon}</Text>
      <Text style={[styles.itemText, danger && styles.danger]}>{label}</Text>
    </Pressable>
  );
}

export default function AppMenu({ visible, onClose }) {
  const styles = useStyles(makeStyles);
  const navigation = useNavigation();
  const { user, signOut } = useAuth();
  const { language, setLanguage, t } = useLanguage();
  const { choice, setChoice } = useTheme();
  const { width } = useWindowDimensions();

  const go = (screen) => {
    onClose();
    navigation.navigate(screen);
  };

  return (
    <Modal visible={visible} transparent animationType="fade" onRequestClose={onClose}>
      <View style={styles.backdrop}>
        <Pressable style={styles.scrim} onPress={onClose} aria-label={t('menu.close')} />
        <View
          style={[styles.panel, { width: Math.min(MENU_WIDTH, width * 0.88) }]}
          role="dialog"
          aria-label={t('menu.open')}
        >
          <ScrollView contentContainerStyle={styles.content}>
            <View style={styles.head}>
              <Avatar user={user} size={56} />
              <View style={styles.who}>
                <Text style={styles.name} numberOfLines={1}>
                  {displayName(user)}
                </Text>
                <Text style={styles.email} numberOfLines={1}>
                  {user?.email ?? ''}
                </Text>
              </View>
              <Pressable
                onPress={onClose}
                style={styles.close}
                accessibilityRole="button"
                aria-label={t('menu.close')}
              >
                <Text style={styles.closeText}>✕</Text>
              </Pressable>
            </View>

            <Item icon="◉" label={t('menu.profile')} onPress={() => go('Profile')} />
            <Item icon="▤" label={t('menu.categories')} onPress={() => go('Categories')} />

            <Text style={styles.section}>{t('menu.appearance')}</Text>
            <Segmented
              label={t('menu.appearance')}
              value={choice}
              onChange={setChoice}
              options={THEME_CHOICES.map((value) => ({ value, label: t(`menu.theme.${value}`) }))}
            />

            <Text style={styles.section}>{t('menu.language')}</Text>
            <Segmented
              label={t('menu.language')}
              value={language}
              onChange={setLanguage}
              options={LANGUAGES.map((code) => ({ value: code, label: LANGUAGE_NAMES[code] }))}
            />

            <View style={styles.divider} />
            <Item icon="ⓘ" label={t('menu.about')} onPress={() => go('About')} />
            <Item
              icon="⌫"
              label={t('menu.deleteAccount')}
              onPress={() => go('DeleteAccount')}
              danger
            />
            <Item
              icon="⎋"
              label={t('menu.signOut')}
              onPress={() => {
                onClose();
                signOut();
              }}
            />
          </ScrollView>
        </View>
      </View>
    </Modal>
  );
}

const makeStyles = (colors) =>
  StyleSheet.create({
    button: { marginRight: spacing.sm, paddingHorizontal: spacing.sm, paddingVertical: spacing.xs },
    burger: { color: colors.headerText, fontSize: 24, lineHeight: 28 },
    backdrop: { flex: 1, flexDirection: 'row' },
    scrim: { backgroundColor: colors.scrim, flex: 1 },
    panel: {
      backgroundColor: colors.surface,
      borderLeftColor: colors.border,
      borderLeftWidth: 1,
      height: '100%',
    },
    content: { padding: spacing.md },
    head: {
      alignItems: 'center',
      borderBottomColor: colors.border,
      borderBottomWidth: 1,
      flexDirection: 'row',
      marginBottom: spacing.sm,
      paddingBottom: spacing.md,
    },
    who: { flex: 1, marginLeft: spacing.md },
    name: { color: colors.text, fontSize: 18, fontWeight: '700' },
    email: { color: colors.textMuted, fontSize: 13, marginTop: 2 },
    close: { padding: spacing.sm },
    closeText: { color: colors.textMuted, fontSize: 18 },
    item: {
      alignItems: 'center',
      borderRadius: radius.sm,
      flexDirection: 'row',
      paddingHorizontal: spacing.sm,
      paddingVertical: spacing.md,
    },
    itemHovered: { backgroundColor: colors.primaryLight },
    icon: { color: colors.primary, fontSize: 18, textAlign: 'center', width: 28 },
    itemText: { color: colors.text, fontSize: 16, marginLeft: spacing.sm },
    danger: { color: colors.danger },
    section: {
      color: colors.textMuted,
      fontSize: 13,
      fontWeight: '600',
      marginBottom: spacing.sm,
      marginTop: spacing.md,
      textTransform: 'uppercase',
    },
    divider: { backgroundColor: colors.border, height: 1, marginVertical: spacing.md },
  });
