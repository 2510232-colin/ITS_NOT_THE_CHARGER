import { initializeApp } from "https://www.gstatic.com/firebasejs/12.1.0/firebase-app.js";
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
} from "https://www.gstatic.com/firebasejs/12.1.0/firebase-auth.js";

const firebaseConfig = {
  apiKey: "AIzaSyAMgpZ6mm-AdfWkNYg0ndwF91fRhlrgZQk",
  authDomain: "isnt-f9543.firebaseapp.com",
  projectId: "isnt-f9543",
  storageBucket: "isnt-f9543.firebasestorage.app",
  messagingSenderId: "171550223731",
  appId: "1:171550223731:web:d265d2f4cdd33ae53fa906",
  measurementId: "G-2BVX0N8NMR",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const provider = new GoogleAuthProvider();

const botonGoogle = document.getElementById("boton-login-google");
const estadoGoogle = document.getElementById("estado-login-google");

function setEstado(mensaje, esError = false) {
  if (!estadoGoogle) {
    return;
  }

  estadoGoogle.textContent = mensaje;
  estadoGoogle.style.color = esError ? "#b21f2d" : "#2d3748";
}

async function loginGoogle() {
  try {
    setEstado("Abriendo Google...");
    const result = await signInWithPopup(auth, provider);
    const token = await result.user.getIdToken();

    setEstado("Validando acceso...");
    const respuesta = await fetch("/auth/firebase/google", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ token }),
    });

    const data = await respuesta.json();
    if (!respuesta.ok || !data.ok) {
      throw new Error(data.mensaje || "No fue posible iniciar sesión con Google.");
    }

    setEstado("Acceso correcto. Redirigiendo...");
    window.location.href = data.redirect || "/";
  } catch (error) {
    setEstado(error.message || "Error en inicio con Google.", true);
    console.error(error);
  }
}

if (botonGoogle) {
  botonGoogle.addEventListener("click", loginGoogle);
}
