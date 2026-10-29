/**
 * /transactions/new: write down one amount spent or received, in seconds (US03).
 *
 * The amount field has the focus when the screen opens, the date is today unless changed, and a
 * kind of spending is one tap, so an entry takes a few seconds. The form, and how it shows a rule
 * the API refused, is components/EntryForm.js. After a save the overview shows the new totals and
 * the entry at the top of the list.
 */

import { api } from '../api/client';
import EntryForm from '../components/EntryForm';
import { useLanguage } from '../i18n/LanguageContext';

export default function NewEntryScreen({ navigation }) {
  const { t } = useLanguage();

  function leave() {
    if (navigation.canGoBack()) navigation.goBack();
    else navigation.replace('Overview');
  }

  async function save(entry) {
    await api.createEntry(entry);
    // US04: the overview reloads when it comes back into view, with the new totals.
    leave();
  }

  return <EntryForm onSubmit={save} onCancel={leave} submitLabel={t('newEntry.save')} />;
}
