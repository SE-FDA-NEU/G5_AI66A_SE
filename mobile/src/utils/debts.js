/**
 * What /debts says about a debt's dates (US13, BR14). Pure functions, so the tests can call them
 * directly. Whether a debt is overdue is the API's answer, `overdue`; these only choose the words.
 */

import { todayIso } from './entryForm';

/** `iso` moved by `days` days, as YYYY-MM-DD: the due-date shortcuts "In a week", "In a month". */
export function addDays(iso, days) {
  const [year, month, day] = iso.split('-').map(Number);
  return todayIso(new Date(year, month - 1, day + days));
}

/**
 * The line under a debt, as a text key and its values: settled on a day, overdue since its due
 * date, due today, due on a later day, or with no due date at all. `today` is YYYY-MM-DD.
 */
export function dueState(debt, today) {
  if (debt.settled_on) return { key: 'debts.settledOn', date: debt.settled_on, tone: 'muted' };
  if (!debt.due_on) return { key: 'debts.noDue', date: null, tone: 'muted' };
  if (debt.overdue) return { key: 'debts.overdue', date: debt.due_on, tone: 'danger' };
  if (debt.due_on === today) return { key: 'debts.dueToday', date: debt.due_on, tone: 'warning' };
  if (debt.due_on === addDays(today, 1)) {
    return { key: 'debts.dueTomorrow', date: debt.due_on, tone: 'warning' };
  }
  return { key: 'debts.dueOn', date: debt.due_on, tone: 'muted' };
}

/** How many open debts are overdue, for the line under the totals. */
export function overdueCount(debts) {
  return debts.filter((debt) => debt.overdue).length;
}
