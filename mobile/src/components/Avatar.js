/**
 * The round picture of an account (US16): its own picture when it has one, else its initials on
 * the brand colour. Used in the menu, on the profile screen and next to the greeting on /.
 */

import { Image, StyleSheet, Text, View } from 'react-native';

import { useStyles } from '../theme';
import { initials } from '../utils/profile';

export default function Avatar({ user, size = 40 }) {
  const styles = useStyles(makeStyles);
  const round = { borderRadius: size / 2, height: size, width: size };

  if (user?.avatar) {
    return (
      <Image
        source={{ uri: user.avatar }}
        style={[styles.image, round]}
        accessibilityIgnoresInvertColors
        alt=""
      />
    );
  }
  return (
    <View style={[styles.circle, round]} aria-hidden>
      <Text style={[styles.letters, { fontSize: size * 0.4 }]}>{initials(user)}</Text>
    </View>
  );
}

const makeStyles = (colors) =>
  StyleSheet.create({
    image: { backgroundColor: colors.border },
    circle: {
      alignItems: 'center',
      backgroundColor: colors.primaryLight,
      borderColor: colors.primary,
      borderWidth: 2,
      justifyContent: 'center',
    },
    letters: { color: colors.primary, fontWeight: '700' },
  });
