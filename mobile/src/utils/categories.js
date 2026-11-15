/**
 * Category names on screen, and the search on /categories. Pure functions, so the tests can check
 * them directly.
 */

/**
 * The name to show: a shared category such as "Food" in the chosen language ("Ăn uống"), and one
 * the account added itself (BR17) exactly as it was typed.
 */
export function categoryName(category, t) {
  if (!category) return '';
  return category.custom ? category.name : t(`category.${category.name}`);
}

/**
 * Text folded for searching: lower case, without accents, so "an uong", "ĂN UỐNG" and "Ăn uống"
 * all match. Vietnamese đ is not an accent in Unicode, so it is folded by hand.
 */
export function fold(text) {
  return String(text ?? '')
    .normalize('NFD')
    .replace(/[̀-ͯ]/g, '')
    .replace(/đ/gi, 'd')
    .toLowerCase()
    .trim();
}

/** Whether a category's shown name contains what was typed; an empty search matches all. */
export function matchesSearch(name, query) {
  const wanted = fold(query);
  return wanted === '' || fold(name).includes(wanted);
}
