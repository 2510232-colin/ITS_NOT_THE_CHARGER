# DOCUMENTO DE EXPOSICIÓN — FERIA DE INGENIERÍAS

## 1. Nombre del proyecto

**IT'S NOT THE CHARGER**

Sistema web para gestión de servicios técnicos, seguimiento de tickets y recomendación inteligente de soluciones para equipos de cómputo.

---

## 2. Idea principal en una frase

Nuestro proyecto ayuda a un negocio de soporte técnico a **atender clientes, recomendar servicios, organizar tickets y administrar operaciones** desde una sola plataforma web.

---

## 3. Problema que resuelve

Muchos negocios de soporte técnico todavía trabajan con:

- mensajes desordenados por WhatsApp,
- recomendaciones improvisadas,
- cotizaciones poco claras,
- seguimiento manual de tickets,
- y poca trazabilidad de los servicios que se ofrecen.

Esto provoca:

- pérdida de tiempo,
- mala experiencia del cliente,
- errores al recomendar soluciones,
- dificultad para dar seguimiento,
- y poca profesionalización del negocio.

Nuestro sistema resuelve eso con una plataforma que:

1. **guía al cliente** para describir su problema,
2. **recomienda servicios** según la intención del usuario,
3. **registra tickets y cotizaciones**,
4. **permite seguimiento por roles**,
5. y **centraliza la operación técnica y administrativa**.

---

## 4. Propuesta de valor

Lo que hace especial al proyecto no es solo que “sea una página web”, sino que combina:

- **experiencia de usuario clara**,
- **lógica de recomendación inteligente**,
- **operación real de un taller técnico**,
- **roles diferenciados**,
- **persistencia en MySQL**,
- y una arquitectura suficientemente sólida para crecer.

En otras palabras:

> No es un catálogo estático; es una herramienta funcional para digitalizar un negocio de soporte técnico.

---

## 5. Objetivo general

Desarrollar una aplicación web que permita administrar un negocio de soporte técnico, mejorando el proceso de atención al cliente, la recomendación de servicios y el seguimiento de tickets.

---

## 6. Objetivos específicos

- Diseñar una interfaz web accesible y entendible para clientes y personal interno.
- Implementar autenticación por roles: cliente, técnico y administrador.
- Centralizar servicios, productos, contenido y tickets en una base de datos MySQL.
- Automatizar recomendaciones de servicios a partir de la descripción del problema del cliente.
- Permitir cotización inicial y seguimiento del estado del servicio.
- Agregar un componente de IA opcional para desempatar recomendaciones ambiguas.

---

## 7. Público objetivo

### Usuarios directos
- Clientes que necesitan soporte técnico.
- Técnicos que gestionan diagnósticos y reparaciones.
- Administradores del negocio.

### Beneficiarios indirectos
- Pequeños negocios de reparación de computadoras.
- Emprendimientos tecnológicos.
- Centros de servicio que quieran digitalizar procesos.

---

## 8. Tecnologías utilizadas

### Backend
- **Python**
- **Flask**

### Base de datos
- **MySQL**

### Frontend
- **HTML**
- **CSS**
- **JavaScript**
- **Jinja2** para plantillas

### Seguridad y utilidades
- `werkzeug.security` para hash de contraseñas
- `python-dotenv` para variables de entorno

### IA opcional
- **Gemini** para desempate en consultas ambiguas

---

## 9. Arquitectura del proyecto explicada de forma sencilla

El sistema está dividido en módulos:

### [server.py](server.py)
Es el punto de entrada. Inicializa Flask, configura seguridad básica y registra las rutas.

### [routes_public.py](routes_public.py)
Maneja lo que ve el cliente público:

- inicio,
- servicios,
- productos,
- contacto,
- cotización,
- detalle de servicios.

### [routes_auth.py](routes_auth.py)
Maneja:

- registro,
- login,
- logout.

### [panel_routes.py](panel_routes.py)
Maneja paneles internos:

- panel de cliente,
- panel técnico,
- panel administrador,
- tickets,
- usuarios,
- servicios,
- contenido,
- pedidos.

### [app_core.py](app_core.py)
Contiene la lógica más importante del proyecto:

- recomendación de servicios,
- reglas de negocio,
- estados de tickets,
- helpers,
- estimaciones,
- y normalización de roles.

### [db.py](db.py)
Centraliza conexión y consultas MySQL.

### [validaciones.py](validaciones.py)
Valida correos, nombres, teléfonos, textos, listas CSV y prioridad.

### [ai_disambiguator.py](ai_disambiguator.py)
Solo se usa cuando una consulta es ambigua. Si está activado Gemini, intenta elegir el mejor servicio entre varios candidatos. Si falla, el sistema sigue funcionando con la heurística local.

---

## 10. ¿Cómo funciona la parte inteligente?

La recomendación no depende completamente de IA externa.

Primero funciona así:

1. El usuario describe su problema.
2. El sistema tokeniza palabras relevantes.
3. Usa un mapa de intenciones, por ejemplo:
	- lenta → rendimiento, SSD, RAM, mantenimiento
	- virus → malware, seguridad, limpieza
	- sobrecalienta → ventilador, pasta térmica, limpieza
4. Compara esas palabras con:
	- título del servicio,
	- categoría,
	- descripción,
	- palabras clave del servicio.
5. Asigna puntajes.
6. Si la recomendación es clara, muestra un servicio principal.
7. Si hay ambigüedad, puede usar Gemini solo para desempatar.
8. Si Gemini no responde, el sistema hace fallback y continúa normal.

### Esto es importante para decir en la exposición:

> “No dependemos totalmente de la IA. Diseñamos una solución híbrida: primero resolvemos localmente con reglas e intención; solo si la consulta es ambigua usamos IA como apoyo.”

Eso transmite criterio técnico, control de costos y robustez.

---

## 11. Funcionalidades principales

### Para clientes
- Registro e inicio de sesión
- Búsqueda guiada de servicios
- Recomendación inteligente
- Solicitud de cotización
- Seguimiento de tickets
- Visualización de servicios y productos

### Para técnicos
- Ver tickets asignados o activos
- Cambiar estados
- Consultar historial
- Dar seguimiento operativo

### Para administradores
- Gestionar servicios
- Gestionar usuarios
- Gestionar contenido del sitio
- Gestionar pedidos
- Ver panel general del negocio

---

## 12. Lo más fuerte del proyecto

### 1. Pensado para un caso real
No es un CRUD aislado. Responde a una necesidad real de negocios técnicos.

### 2. Tiene roles y flujo operativo
Cliente, técnico y administrador tienen responsabilidades distintas.

### 3. Tiene recomendación inteligente útil
No solo muestra servicios: guía al usuario hacia una solución probable.

### 4. Tiene fallback y tolerancia a fallos
Aunque la IA externa falle, el sistema sigue funcionando.

### 5. Tiene enfoque profesional
Arquitectura modular, validaciones, seguridad básica, manejo de sesiones y persistencia real.

---

## 13. Limitaciones actuales

Decir esto suma madurez y honestidad técnica:

- La recomendación aún es principalmente heurística, no usa embeddings ni aprendizaje entrenado.
- La precisión depende de la calidad de metadatos y palabras clave registradas.
- No se ha desplegado todavía como SaaS multiempresa.
- Aún se puede mejorar con analítica, métricas de uso y dashboard de negocio más avanzado.

---

## 14. Posibles mejoras futuras

- Panel de analítica con métricas de servicios más solicitados.
- Historial de recomendaciones aceptadas para retroalimentar el sistema.
- Chat de soporte integrado.
- Notificaciones por correo o WhatsApp.
- Gestión avanzada de inventario y refacciones.
- Despliegue en nube con dominio y HTTPS productivo.
- Modelo de recomendación más avanzado entrenado con consultas reales.

---

## 15. ¿Por qué este proyecto puede interesarle a un buscador de talento?

Porque demuestra varias competencias valiosas a la vez:

### Competencias técnicas
- backend con Flask,
- integración con base de datos relacional,
- autenticación,
- validaciones,
- diseño modular,
- frontend funcional,
- integración con IA externa,
- y razonamiento sobre ranking/relevancia.

### Competencias de producto
- entendimiento de usuario real,
- priorización de MVP,
- enfoque en experiencia de usuario,
- solución a un problema de negocio.

### Competencias de ingeniería
- fallback,
- análisis de errores,
- pruebas de regresión,
- ajustes finos de recomendación,
- balance entre simpleza y funcionalidad.

### Mensaje clave para reclutadores

> “No solo programamos una interfaz; diseñamos una solución digital completa, con lógica de negocio, base de datos, experiencia de usuario y componente inteligente con fallback.”

---

## 16. Guion de exposición para 4 integrantes (5 a 8 minutos)

## Duración recomendada: 6 minutos 30 segundos

---

### Integrante 1 — Apertura y problema (1 min 20 s)

**Qué dice:**

“Hola, somos el equipo de **IT'S NOT THE CHARGER**. Nuestro proyecto es una plataforma web para negocios de soporte técnico. Detectamos que muchos talleres todavía atienden de forma desordenada: reciben mensajes sin estructura, recomiendan servicios de forma manual y les cuesta dar seguimiento a tickets y cotizaciones.

Nosotros propusimos una solución que organiza todo ese proceso: desde que el cliente describe su problema, hasta que el negocio le recomienda un servicio, genera seguimiento y administra la operación interna.”

**Objetivo de esta parte:**
- captar atención,
- dejar claro el problema,
- y mostrar que el proyecto tiene aplicación real.

---

### Integrante 2 — Demostración funcional del sistema (1 min 40 s)

**Qué dice mientras navega:**

“Aquí tenemos la parte pública. El usuario puede entrar al inicio, usar el buscador guiado y escribir un problema como ‘mi computadora está lenta’ o usar una sugerencia rápida.

El sistema analiza la consulta y recomienda un servicio principal o varias opciones comparables si detecta ambigüedad.

Además, el usuario puede ver detalle del servicio, solicitar cotización e iniciar sesión para dar seguimiento a su ticket.”

**Mostrar idealmente:**
- [templates/index.html](templates/index.html) visualmente en ejecución
- buscador en inicio
- página de servicios
- recomendación principal
- acceso a cotización

---

### Integrante 3 — Parte técnica e inteligencia (1 min 40 s)

**Qué dice:**

“La parte interesante es que nuestra recomendación no depende totalmente de una IA externa. Primero usamos una lógica heurística en [app_core.py](app_core.py): tomamos palabras del usuario, las relacionamos con un mapa de intenciones y las comparamos contra títulos, categorías, descripciones y palabras clave de los servicios.

Si el resultado no es suficientemente claro, entonces usamos Gemini de forma opcional para desempatar entre varios candidatos. Y si Gemini no responde, el sistema sigue funcionando con fallback local.

Esto nos permitió tener una solución más robusta, más barata y más controlable.”

**Frase poderosa:**

> “Diseñamos una arquitectura híbrida: heurística local para velocidad y confiabilidad, IA externa solo para casos ambiguos.”

---

### Integrante 4 — Impacto, administración y cierre (1 min 30 s)

**Qué dice:**

“El proyecto no solo recomienda servicios. También incluye autenticación, paneles por rol, administración de servicios, gestión de usuarios y seguimiento de tickets. Esto lo convierte en una plataforma funcional para digitalizar un negocio técnico completo.

Lo valioso de nuestro trabajo es que combina desarrollo web, base de datos, diseño de producto y un componente inteligente aplicado a un problema real.

A futuro podríamos escalarlo con analítica, notificaciones, inventario y modelos de recomendación más avanzados.”

**Cierre recomendado:**

“En resumen, **IT'S NOT THE CHARGER** transforma un proceso técnico informal en una experiencia digital organizada, trazable e inteligente.”

---

## 17. Versión ultra corta por si solo tienen 3 minutos

“Nuestro proyecto es una plataforma web para negocios de soporte técnico. Permite que el cliente describa su problema, el sistema recomiende servicios de forma inteligente, genere cotizaciones y dé seguimiento a tickets. Internamente también incluye paneles por rol para técnicos y administradores. Lo innovador es que usamos una arquitectura híbrida: reglas heurísticas locales para resolver rápido y Gemini solo para consultas ambiguas, con fallback automático. Es una solución realista, escalable y enfocada en una necesidad concreta del mercado.”

---

## 18. Flujo ideal de demostración en el stand

### Demo de 2 minutos

1. Abrir inicio.
2. Mostrar buscador guiado.
3. Escribir: “mi computadora está lenta”.
4. Mostrar recomendación.
5. Entrar a detalle del servicio.
6. Mostrar botón de cotización.
7. Mencionar que existen roles y seguimiento interno.

### Demo alternativa rápida

1. Buscar “tengo virus”.
2. Mostrar recomendación.
3. Explicar heurística + IA opcional.

---

## 19. Preguntas importantes que podrían hacerles y respuestas sugeridas

### 1. ¿Qué hace diferente su proyecto?
**Respuesta:**
No es solo una web informativa. Integra operación real, roles, tickets y recomendación inteligente de servicios.

### 2. ¿Por qué no usar solo IA?
**Respuesta:**
Porque sería más costoso, menos controlable y más frágil. Nuestra lógica local resuelve la mayoría de casos, y la IA solo se usa cuando aporta valor.

### 3. ¿Qué tan preciso es?
**Respuesta:**
Depende de la calidad de metadatos y del tipo de consulta, pero ya probamos regresiones y ajustamos scoring para mejorar casos reales como “computadora lenta” o “armar una PC gamer”.

### 4. ¿Qué aprendieron técnicamente?
**Respuesta:**
Aprendimos integración backend-frontend, diseño modular, conexión segura a base de datos, manejo de sesiones, validaciones, pruebas de regresión y ajuste fino de un motor de recomendación.

### 5. ¿Qué parte fue la más difícil?
**Respuesta:**
Balancear precisión sin sobreingeniería: lograr buenas recomendaciones manteniendo una solución simple, explicable y funcional.

### 6. ¿Cómo lo llevarían a producción?
**Respuesta:**
Con variables de entorno, despliegue en servidor Linux o nube, HTTPS, base de datos administrada, backups y monitoreo.

### 7. ¿Qué impacto tendría en un negocio real?
**Respuesta:**
Mejoraría la experiencia del cliente, reduciría tiempo de atención, ordenaría tickets y profesionalizaría la operación del taller.

---

## 20. Preguntas inteligentes para impresionar a reclutadores o jurados

Si un jurado o reclutador muestra interés, ustedes también pueden responder con madurez y hacer preguntas como:

- “¿Ustedes valorarían más la parte de arquitectura, la de producto o la de experiencia de usuario en un proyecto así?”
- “¿En industria ven más potencial en este tipo de solución como SaaS o como sistema interno especializado?”
- “¿Qué le agregarían para volverlo más competitivo comercialmente?”

Eso cambia la conversación de alumno-expositor a perfil con criterio profesional.

---

## 21. Cómo hablar para que los estudiantes de preparatoria sí entiendan

Usen esta idea:

> “Imaginen una tienda o taller de computadoras donde el cliente llega y dice: ‘mi laptop está lenta’. En vez de responder improvisadamente, nuestro sistema analiza el problema, propone opciones, registra el caso y permite darle seguimiento. Es como digitalizar el cerebro operativo del negocio.”

Eso aterriza el proyecto muy bien.

---

## 22. Cómo hablar para que un reclutador sí se interese

Usen esta idea:

> “Este proyecto demuestra que podemos construir una solución completa: backend, base de datos, autenticación, lógica de negocio, UX e integración inteligente, pero sin caer en complejidad innecesaria.”

Esa frase vende bien perfil de ingeniería aplicada.

---

## 23. Reparto práctico del trabajo en el stand

### Integrante 1
- saluda,
- rompe el hielo,
- plantea el problema.

### Integrante 2
- maneja la demo en vivo.

### Integrante 3
- explica tecnología y arquitectura.

### Integrante 4
- explica impacto, mejoras futuras y responde preguntas.

Tip: si llega mucha gente, pueden rotar cada 10–15 minutos para que todos participen igual.

---

## 24. Frases listas para usar durante la expo

### Frase de apertura
“Más que una página, desarrollamos una herramienta para profesionalizar la atención técnica.”

### Frase técnica
“Nuestra recomendación es híbrida: heurística local primero, IA opcional después.”

### Frase de impacto
“Buscamos convertir un proceso informal en un flujo digital ordenado y escalable.”

### Frase de cierre
“IT'S NOT THE CHARGER demuestra cómo la ingeniería de software puede resolver problemas reales de negocio con soluciones prácticas y bien diseñadas.”

---

## 25. Recomendación final para la feria

Si quieren destacar de verdad:

1. No lean diapositivas.
2. Hagan una demo breve en vivo.
3. Expliquen el problema antes que la tecnología.
4. Mencionen el valor real para negocio.
5. Usen la parte de IA como complemento, no como único gancho.
6. Muestren seguridad, orden y dominio técnico.

---

## 26. Cierre final sugerido

“Nuestro proyecto demuestra que un equipo universitario puede desarrollar una solución funcional, útil y con visión de crecimiento. Integra desarrollo web, base de datos, experiencia de usuario y lógica inteligente para resolver un problema real del sector técnico. Ese equilibrio entre utilidad, diseño e ingeniería es precisamente lo que quisimos construir.”

