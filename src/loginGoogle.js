import { signInWithPopup } from "firebase/auth";

import { auth, provider } from "./firebase";

export async function loginGoogle() {
  try {
    const result = await signInWithPopup(auth, provider);

    const user = result.user;
    console.log(user);

    // TOKEN
    const token = await user.getIdToken();
    console.log(token);

    await fetch("http://localhost:8080/auth/firebase/google", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        token: token
      })
    });
  } catch (error) {
    console.log(error);
  }
}
