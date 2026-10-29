/**
 * Every screen built so far opens at the address section 6 of docs/requirements.md gives it, so
 * the instructor can reach each P0 story from a link and the address bar shows where they are.
 */

import { ROUTES, linking } from '../src/navigation/linking';

test('each screen has the route of the requirements', () => {
  expect(ROUTES).toEqual({
    Login: 'login',
    Register: 'register',
    Overview: '',
    NewEntry: 'transactions/new',
    EditEntry: 'transactions/:id',
    Stats: 'stats',
    Debts: 'debts',
    NewDebt: 'debts/new',
  });
});

test('the navigator reads its routes from the same table', () => {
  expect(linking.config.screens).toBe(ROUTES);
});
