/**
 * Which screens exist. Signed out, only /login and /register; signed in, only the screens of an
 * account. A signed-in screen typed into the address bar without a session lands on /login
 * (BR4 as navigation), and signing in or creating an account lands on / by itself.
 */

import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { ActivityIndicator, StyleSheet, View } from 'react-native';

import LanguageSwitch from '../components/LanguageSwitch';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import LoginScreen from '../screens/LoginScreen';
import OverviewScreen from '../screens/OverviewScreen';
import RegisterScreen from '../screens/RegisterScreen';
import { colors } from '../theme';
import { linking } from './linking';

const Stack = createNativeStackNavigator();

const screenOptions = {
  headerStyle: { backgroundColor: colors.primary },
  headerTintColor: colors.textInverse,
  headerTitleStyle: { fontWeight: '600' },
  // The language switch sits in the top bar of every screen (US11).
  headerRight: () => <LanguageSwitch />,
};

export default function AppNavigator() {
  const { status } = useAuth();
  const { t } = useLanguage();

  // While the stored token is read, show a spinner rather than flash the sign-in screen.
  if (status === 'loading') {
    return (
      <View style={styles.splash}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  // The browser tab reads "<screen> · <app name>", in the chosen language.
  const documentTitle = {
    formatter: (options, route) => `${options?.title ?? route?.name} · ${t('app.title')}`,
  };

  return (
    <NavigationContainer linking={linking} documentTitle={documentTitle}>
      <Stack.Navigator screenOptions={screenOptions}>
        {status === 'signed-in' ? (
          <Stack.Screen
            name="Overview"
            component={OverviewScreen}
            options={{ title: t('overview.title') }}
          />
        ) : (
          <>
            <Stack.Screen
              name="Login"
              component={LoginScreen}
              options={{ title: t('login.title') }}
            />
            <Stack.Screen
              name="Register"
              component={RegisterScreen}
              options={{ title: t('register.title') }}
            />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  splash: {
    alignItems: 'center',
    backgroundColor: colors.background,
    flex: 1,
    justifyContent: 'center',
  },
});
