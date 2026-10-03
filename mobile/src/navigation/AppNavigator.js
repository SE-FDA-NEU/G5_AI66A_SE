/**
 * Which screen shows. Signed out, only /login exists; signed in, only the overview at / exists,
 * so no signed-in screen can ever be reached without a session (BR4 as navigation).
 */

import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { ActivityIndicator, StyleSheet, View } from 'react-native';

import LanguageSwitch from '../components/LanguageSwitch';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import LoginScreen from '../screens/LoginScreen';
import OverviewScreen from '../screens/OverviewScreen';
import { colors } from '../theme';

const Stack = createNativeStackNavigator();

// In a browser the address bar follows section 6 of docs/requirements.md: /login and /.
const linking = {
  prefixes: [],
  config: {
    screens: {
      Login: 'login',
      Overview: '',
    },
  },
};

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
          <Stack.Screen name="Login" component={LoginScreen} options={{ title: t('login.title') }} />
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
