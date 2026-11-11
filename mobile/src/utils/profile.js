/**
 * How the app names a person (US16): the name they asked to be called, else their full name, else
 * their email, so an account that never filled in its profile is greeted as before. Pure
 * functions, kept apart from the screens so the tests can call them.
 */

function given(value) {
  return typeof value === 'string' && value.trim() ? value.trim() : null;
}

/** The name the greeting and the menu use. */
export function displayName(user) {
  if (!user) return '';
  return given(user.nickname) ?? given(user.full_name) ?? user.email ?? '';
}

/** One or two capitals for the round picture of an account without one: "NM", or "M". */
export function initials(user) {
  const name = given(user?.nickname) ?? given(user?.full_name);
  if (name) {
    const words = name.split(/\s+/);
    const letters = words.length > 1 ? words[0][0] + words[words.length - 1][0] : words[0][0];
    return letters.toUpperCase();
  }
  return (user?.email?.[0] ?? '?').toUpperCase();
}

/**
 * The fields of the profile form that differ from the saved profile, ready for PATCH /users/me.
 * An emptied field is sent as "" so that the server clears it (BR15).
 */
export function profileChanges(saved, form) {
  const changes = {};
  for (const field of ['full_name', 'nickname', 'phone']) {
    const before = saved?.[field] ?? '';
    const after = (form[field] ?? '').trim();
    if (after !== before) changes[field] = after;
  }
  if ((form.avatar ?? null) !== (saved?.avatar ?? null)) changes.avatar = form.avatar ?? null;
  return changes;
}
