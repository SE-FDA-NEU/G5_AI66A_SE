/**
 * What /debts says about a debt's dates (US13, BR14). "Overdue" itself is the API's answer; these
 * tests check that the words follow it, and the dates around today.
 */

import { addDays, dueState, overdueCount } from '../src/utils/debts';

const TODAY = '2026-10-24';
const debt = (fields) => ({ settled_on: null, due_on: null, overdue: false, ...fields });

describe('addDays', () => {
  test('moves across the end of a month and of a year', () => {
    expect(addDays('2026-10-24', 7)).toBe('2026-10-31');
    expect(addDays('2026-10-25', 7)).toBe('2026-11-01');
    expect(addDays('2026-12-30', 30)).toBe('2027-01-29');
  });
});

describe('dueState', () => {
  test('says overdue, in red, when the API says so (BR14)', () => {
    expect(dueState(debt({ due_on: '2026-10-23', overdue: true }), TODAY)).toEqual({
      key: 'debts.overdue',
      date: '2026-10-23',
      tone: 'danger',
    });
  });

  test('says due today, not overdue, on the due date itself (BR14)', () => {
    expect(dueState(debt({ due_on: TODAY }), TODAY).key).toBe('debts.dueToday');
  });

  test('says due tomorrow the day before', () => {
    expect(dueState(debt({ due_on: '2026-10-25' }), TODAY).key).toBe('debts.dueTomorrow');
  });

  test('gives the date of a later due date, and says when there is none', () => {
    expect(dueState(debt({ due_on: '2026-11-03' }), TODAY)).toMatchObject({
      key: 'debts.dueOn',
      date: '2026-11-03',
    });
    expect(dueState(debt({}), TODAY).key).toBe('debts.noDue');
  });

  test('says when a debt was settled, whatever its due date', () => {
    const settled = debt({ due_on: '2026-09-29', settled_on: '2026-09-28' });
    expect(dueState(settled, TODAY)).toMatchObject({ key: 'debts.settledOn', date: '2026-09-28' });
  });
});

test('overdueCount counts the overdue debts only', () => {
  expect(overdueCount([debt({ overdue: true }), debt({}), debt({ overdue: true })])).toBe(2);
  expect(overdueCount([])).toBe(0);
});
