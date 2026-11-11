/**
 * Choose a profile picture and make it small enough to keep (US16, BR15): cut to a square from
 * the middle, 256 pixels wide, JPEG. A photo from a phone is several megabytes; what is sent is
 * about 20 KB, well under the 200 KB the server accepts.
 *
 * Works the same in a browser (a file chooser) and on a phone (the photo library).
 */

import * as ImagePicker from 'expo-image-picker';
import { ImageManipulator, SaveFormat } from 'expo-image-manipulator';

export const AVATAR_SIZE = 256;

/** The largest square in the middle of a picture of this size. Pure, for the tests. */
export function centreSquare(width, height) {
  const side = Math.min(width, height);
  return {
    originX: Math.floor((width - side) / 2),
    originY: Math.floor((height - side) / 2),
    width: side,
    height: side,
  };
}

/** A data: URL of the chosen picture, or null when the person closed the chooser. */
export async function pickAvatar() {
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ['images'],
    allowsEditing: true,
    aspect: [1, 1],
    quality: 1,
  });
  if (result.canceled || !result.assets?.length) return null;

  const { uri, width, height } = result.assets[0];
  const context = ImageManipulator.manipulate(uri);
  if (width && height && width !== height) context.crop(centreSquare(width, height));
  context.resize({ width: AVATAR_SIZE, height: AVATAR_SIZE });
  const image = await context.renderAsync();
  const saved = await image.saveAsync({ format: SaveFormat.JPEG, compress: 0.7, base64: true });
  return `data:image/jpeg;base64,${saved.base64}`;
}
