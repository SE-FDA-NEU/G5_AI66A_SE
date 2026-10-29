/**
 * The address of each screen in a browser, as section 6 of docs/requirements.md names it. Kept
 * apart from AppNavigator so the tests can check it without drawing a screen.
 */

export const ROUTES = {
  Login: 'login',
  Register: 'register',
  Overview: '',
  NewEntry: 'transactions/new',
  EditEntry: 'transactions/:id',
  Stats: 'stats',
};

export const linking = {
  prefixes: [],
  config: { screens: ROUTES },
};
