import { initializeApp } from 'firebase/app';
import { getAuth, GoogleAuthProvider, signInWithPopup, signOut } from 'firebase/auth';
import {
  PUBLIC_FIREBASE_API_KEY,
  PUBLIC_FIREBASE_AUTH_DOMAIN,
  PUBLIC_FIREBASE_PROJECT_ID,
  PUBLIC_FIREBASE_MESSAGING_SENDER,
  PUBLIC_FIREBASE_APP_ID,
  PUBLIC_FIREBASE_STORAGE_BUCKET,
} from '$env/static/public';

const firebaseConfig = {
  apiKey:            PUBLIC_FIREBASE_API_KEY,
  authDomain:        PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId:         PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket:     PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: PUBLIC_FIREBASE_MESSAGING_SENDER,
  appId:             PUBLIC_FIREBASE_APP_ID,
};

const app             = initializeApp(firebaseConfig);
export const auth     = getAuth(app);
export const provider = new GoogleAuthProvider();

export async function signInWithGoogle() {
  const result = await signInWithPopup(auth, provider);
  return result.user;
}

export async function logout() {
  await signOut(auth);
}