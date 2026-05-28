import { initializeApp } from "firebase/app";

import {
  getAuth,
  GoogleAuthProvider
} from "firebase/auth";

const firebaseConfig = {
  apiKey: "AIzaSyAMgpZ6mm-AdfWkNYg0ndwF91fRhlrgZQk",
  authDomain: "isnt-f9543.firebaseapp.com",
  projectId: "isnt-f9543",
  storageBucket: "isnt-f9543.firebasestorage.app",
  messagingSenderId: "171550223731",
  appId: "1:171550223731:web:d265d2f4cdd33ae53fa906",
  measurementId: "G-2BVX0N8NMR"
};

const app = initializeApp(firebaseConfig);

export const auth = getAuth(app);

export const provider = new GoogleAuthProvider();
