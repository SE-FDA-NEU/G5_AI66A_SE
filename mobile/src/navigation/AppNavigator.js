/**
 * Which screens exist. Signed out: /welcome first (US15), then /login, /register and /about. Signed in,
 * only the screens of an account. A signed-in screen typed into the address bar without a session
 * lands on /welcome (BR4 as navigation), and signing in or creating an account lands on / by
 * itself. The top bar takes the palette in use, light or dark (US19).
 */

import { DarkTheme, DefaultTheme, NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { useMemo } from 'react';
import { ActivityIndicator, StyleSheet, View } from 'react-native';

import LanguageSwitch from '../components/LanguageSwitch';
import { useAuth } from '../context/AuthContext';
import { useLanguage } from '../i18n/LanguageContext';
import AboutScreen from '../screens/AboutScreen';
import CategoriesScreen from '../screens/CategoriesScreen';
import CategoryScreen from '../screens/CategoryScreen';
import DebtsScreen from '../screens/DebtsScreen';
import DeleteAccountScreen from '../screens/DeleteAccountScreen';
import EditEntryScreen from '../screens/EditEntryScreen';
import LoginScreen from '../screens/LoginScreen';
import NewDebtScreen from '../screens/NewDebtScreen';
import NewEntryScreen from '../screens/NewEntryScreen';
import OverviewScreen from '../screens/OverviewScreen';
import RegisterScreen from '../screens/RegisterScreen';
import StatsScreen from '../screens/StatsScreen';
import WelcomeScreen from '../screens/WelcomeScreen';
import { useTheme } from '../theme';
import { linking } from './linking';

const Stack = createNativeStackNavigator();

export default function AppNavigator() {
  const { status } = useAuth();
  const { t } = useLanguage();
  const { colors, scheme } = useTheme();
  const signedIn = status === 'signed-in';

  const screenOptions = useMemo(
    () => ({
      headerStyle: { backgroundColor: colors.header },
      headerTintColor: colors.headerText,
      headerTitleStyle: { fontWeight: '600' },
      // The language switch sits in the top bar of every screen (US11).
      headerRight: () => <LanguageSwitch />,
      contentStyle: { backgroundColor: colors.background },
    }),
    [colors],
  );

  // The navigator's own colours (the space behind a screen while it slides in) follow the theme.
  const navigationTheme = useMemo(() => {
    const base = scheme === 'dark' ? DarkTheme : DefaultTheme;
    return {
      ...base,
      colors: {
        ...base.colors,
        primary: colors.primary,
        background: colors.background,
        card: colors.header,
        text: colors.headerText,
        border: colors.border,
      },
    };
  }, [colors, scheme]);

  // While the stored token is read, show a spinner rather than flash the welcome screen.
  if (status === 'loading') {
    return (
      <View style={[styles.splash, { backgroundColor: colors.background }]}>
        <ActivityIndicator size="large" color={colors.primary} />
      </View>
    );
  }

  // The browser tab reads "<screen> · <app name>", in the chosen language.
  const documentTitle = {
    formatter: (options, route) => `${options?.title ?? route?.name} · ${t('app.title')}`,
  };

  const about = (
    <Stack.Screen name="About" component={AboutScreen} options={{ title: t('about.title') }} />
  );

  return (
    <NavigationContainer linking={linking} documentTitle={documentTitle} theme={navigationTheme}>
      <Stack.Navigator screenOptions={screenOptions}>
        {signedIn ? (
          <>
            <Stack.Screen
              name="Overview"
              component={OverviewScreen}
              options={{ title: t('overview.title') }}
            />
            <Stack.Screen
              name="NewEntry"
              component={NewEntryScreen}
              options={{ title: t('newEntry.title') }}
            />
            <Stack.Screen
              name="EditEntry"
              component={EditEntryScreen}
              options={{ title: t('editEntry.title') }}
            />
            <Stack.Screen
              name="Stats"
              component={StatsScreen}
              options={{ title: t('stats.title') }}
            />
            <Stack.Screen
              name="Debts"
              component={DebtsScreen}
              options={{ title: t('debts.title') }}
            />
            <Stack.Screen
              name="NewDebt"
              component={NewDebtScreen}
              options={{ title: t('newDebt.title') }}
            />
            <Stack.Screen
              name="Categories"
              component={CategoriesScreen}
              options={{ title: t('categories.title') }}
            />
            <Stack.Screen
              name="Category"
              component={CategoryScreen}
              options={{ title: t('categories.title') }}
            />
            <Stack.Screen
              name="DeleteAccount"
              component={DeleteAccountScreen}
              options={{ title: t('deleteAccount.title') }}
            />
            {about}
          </>
        ) : (
          <>
            <Stack.Screen
              name="Welcome"
              component={WelcomeScreen}
              options={{ title: t('welcome.title'), headerShown: false }}
            />
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
            {about}
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}

const styles = StyleSheet.create({
  splash: { alignItems: 'center', flex: 1, justifyContent: 'center' },
});
