/**
 * Keeps the sign-in token on the device.
 *
 * On a phone the token goes into expo-secure-store, which the operating system encrypts
 * (Keychain on iOS, Keystore on Android). SecureStore does not exist in a browser, so there the
 * token goes into localStorage instead. The rest of the app never needs to know which is used.
 */

import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

const inBrowser = Platform.OS === 'web';

export async function setItem(key, value) {
  if (inBrowser) {
    window.localStorage.setItem(key, value);
    return;
  }
  await SecureStore.setItemAsync(key, value);
}

export async function getItem(key) {
  if (inBrowser) {
    return window.localStorage.getItem(key);
  }
  return SecureStore.getItemAsync(key);
}

export async function removeItem(key) {
  if (inBrowser) {
    window.localStorage.removeItem(key);
    return;
  }
  await SecureStore.deleteItemAsync(key);
}
