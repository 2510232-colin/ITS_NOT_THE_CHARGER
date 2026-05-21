# SPEECH DE EXPOSICIÓN — IT'S NOT THE CHARGER

## Versión principal para 4 integrantes

**Duración estimada:** 5 a 8 minutos

---

## Integrante 1 — Apertura

“Hola, mucho gusto. Somos el equipo de **IT'S NOT THE CHARGER** y hoy les vamos a presentar nuestro proyecto.

Nuestro sistema es una plataforma web diseñada para negocios de soporte técnico. La idea nace de un problema muy común: en muchos talleres o negocios de reparación de computadoras, la atención al cliente sigue siendo desordenada. Muchas veces todo se maneja por mensajes, de forma improvisada, sin seguimiento claro, sin recomendación bien estructurada y sin un control real de tickets o servicios.

Nosotros quisimos resolver eso desarrollando una solución que ayuda a organizar todo el flujo: desde que el cliente describe su problema, hasta que el negocio recomienda un servicio, registra la solicitud y le da seguimiento.

En pocas palabras, nuestro proyecto busca digitalizar y profesionalizar la operación de un negocio de soporte técnico.”

---

## Integrante 2 — Explicación funcional

“En la parte pública del sistema, el usuario puede entrar al sitio y usar un buscador guiado donde describe su problema con lenguaje natural. Por ejemplo, puede escribir: ‘mi computadora está lenta’, ‘no enciende’, ‘se sobrecalienta’ o ‘quiero actualizar RAM o SSD’.

Con base en esa consulta, el sistema analiza la intención del usuario y propone uno o varios servicios recomendados.

Si el caso es muy claro, muestra una recomendación principal. Si detecta varias opciones parecidas, presenta servicios comparables para ayudar al usuario a elegir mejor. Y si todavía falta contexto, muestra preguntas guía para que el cliente especifique mejor su necesidad.

Además, el sistema también permite ver detalles del servicio, solicitar una cotización y consultar información del negocio. Todo esto mejora la experiencia del cliente porque hace que la atención sea más clara, rápida y profesional.”

---

## Integrante 3 — Parte técnica

“En la parte técnica, nuestro proyecto está desarrollado con **Python y Flask** en el backend, **MySQL** como base de datos y **HTML, CSS, JavaScript y Jinja** para la interfaz.

La aplicación también cuenta con autenticación por roles. Esto significa que no todos ven lo mismo: tenemos usuarios cliente, técnico y administrador. Cada uno tiene funciones diferentes dentro del sistema.

Ahora, una de las partes más interesantes del proyecto es la lógica de recomendación. Nosotros no quisimos depender completamente de una inteligencia artificial externa, porque eso puede ser más costoso, menos controlable y más frágil.

Por eso diseñamos una solución híbrida. Primero usamos una lógica heurística local: tomamos palabras importantes de la consulta del usuario, las relacionamos con un mapa de intenciones y las comparamos contra títulos, categorías, descripciones y palabras clave de los servicios.

Por ejemplo, si el usuario escribe que su computadora está lenta, el sistema relaciona eso con conceptos como rendimiento, SSD, RAM, mantenimiento y optimización. Con base en eso asigna puntajes y ordena los servicios más probables.

Si la consulta resulta ambigua, entonces podemos usar Gemini de manera opcional para desempatar entre varios candidatos. Y si Gemini no responde, el sistema sigue funcionando gracias al fallback local. Eso hace que la plataforma sea más robusta.”

---

## Integrante 4 — Impacto, valor y cierre

“Además de recomendar servicios, nuestro proyecto también administra tickets, usuarios, contenido y paneles internos. Eso lo convierte en una herramienta mucho más completa que una simple página informativa.

Creemos que el valor del proyecto está en que combina varias áreas de ingeniería de software: desarrollo web, bases de datos, validaciones, experiencia de usuario, lógica de negocio y un componente inteligente aplicado a un problema real.

También consideramos que este proyecto puede crecer en el futuro. Por ejemplo, podría incorporar analítica de servicios más solicitados, notificaciones, inventario, métricas operativas o una recomendación todavía más avanzada basada en datos históricos.

En resumen, **IT'S NOT THE CHARGER** demuestra cómo una solución tecnológica bien diseñada puede transformar un proceso informal en una operación digital ordenada, útil y escalable.

Muchas gracias. Si quieren, con gusto les mostramos una demostración rápida del sistema en funcionamiento.”

---

# Versión más natural y fluida para hablar sin sonar leído

“Hola, somos el equipo de **IT'S NOT THE CHARGER**. Nuestro proyecto es una plataforma web pensada para negocios de soporte técnico.

La idea surgió porque vimos que muchos talleres todavía trabajan de manera muy manual: el cliente manda mensajes, explica su problema de forma desordenada, alguien le recomienda algo casi de memoria, y luego no hay un seguimiento claro del servicio o del ticket.

Nosotros quisimos cambiar eso creando una solución que organizara todo el proceso.

Primero, el cliente entra al sistema y puede escribir qué problema tiene, por ejemplo si su computadora está lenta, si no enciende o si se sobrecalienta. A partir de esa descripción, el sistema analiza la intención del usuario y le recomienda el servicio más probable.

Lo interesante es que la recomendación no depende únicamente de inteligencia artificial. Nosotros primero construimos una lógica local que trabaja con palabras clave, categorías, descripciones y reglas de intención. De esa manera, la mayoría de casos se pueden resolver rápido y de forma controlada.

Si la consulta es ambigua, entonces el sistema puede apoyarse en Gemini para desempatar entre varias opciones. Pero si la IA no está disponible, la aplicación sigue funcionando normalmente. Eso nos permitió hacer una solución más sólida y más realista.

Además, el sistema no solo recomienda servicios. También incluye autenticación, cotizaciones, seguimiento de tickets y paneles por rol para clientes, técnicos y administradores. Eso hace que el proyecto no sea solo una web bonita, sino una herramienta funcional para digitalizar la operación de un negocio técnico.

Nos parece valioso porque combina backend, frontend, base de datos, validaciones, UX y lógica inteligente aplicada a una necesidad real.

En resumen, nuestro proyecto busca profesionalizar la atención técnica y convertir un proceso informal en un flujo digital más ordenado, claro y escalable.”

---

# Versión corta de 2 a 3 minutos

“Hola, somos el equipo de **IT'S NOT THE CHARGER** y nuestro proyecto es una plataforma web para negocios de soporte técnico.

El problema que buscamos resolver es que muchos talleres todavía atienden clientes de forma desordenada, con recomendaciones improvisadas y sin un seguimiento claro de tickets o servicios.

Nuestra solución permite que el usuario describa su problema con lenguaje natural, por ejemplo si su computadora está lenta o no enciende, y el sistema le recomienda servicios de forma inteligente.

La parte interesante es que usamos una arquitectura híbrida: primero una lógica heurística local basada en palabras clave e intención, y solo en casos ambiguos usamos Gemini como apoyo para desempatar. Si la IA falla, el sistema sigue funcionando con fallback.

Además, el proyecto incluye autenticación, cotizaciones, administración de servicios y seguimiento por roles. Eso lo convierte en una herramienta funcional para digitalizar la operación de un negocio técnico.

En resumen, nuestro proyecto combina desarrollo web, base de datos y lógica inteligente para resolver un problema real de negocio.”

---

# Frases clave para memorizar

## Apertura
- “Nuestro proyecto digitaliza y organiza la atención de un negocio de soporte técnico.”
- “No es solo una página web; es una herramienta operativa.”

## Parte técnica
- “Diseñamos una arquitectura híbrida: heurística local primero, IA opcional después.”
- “La aplicación sigue funcionando incluso si la IA externa no responde.”

## Valor del proyecto
- “Resuelve un problema real con una solución funcional y escalable.”
- “Integra backend, base de datos, experiencia de usuario y lógica inteligente.”

## Cierre
- “Buscamos transformar un proceso informal en una operación digital profesional.”
- “Si quieren, les mostramos una demo rápida del sistema.”

---

# Consejos para decirlo bien

- Hablen como si se lo explicaran a alguien que no conoce programación.
- No corran; hagan pausas cortas después de cada idea importante.
- No memoricen palabra por palabra: memoricen bloques.
- Mientras uno habla, otro puede ir mostrando la demo.
- Si llega un reclutador o jurado, destaquen la parte de arquitectura híbrida y el enfoque de problema real.
