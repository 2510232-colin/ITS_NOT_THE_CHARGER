# Exposición - Semana de las Ingenierías

## Proyecto
**IT'S NOT THE CHARGER**

Plataforma web para un negocio de reparación y soporte técnico de computadoras con atención organizada por tickets, seguimiento al cliente, catálogo de servicios y opción de atención en sucursal o a domicilio.

---

# 1. Qué es realmente este proyecto

Este proyecto no está pensado para un departamento interno de sistemas de una empresa.

La idea real es la de un **negocio propio de reparación de computadoras** que necesita atender mejor a sus clientes.

Es decir:

- un cliente entra al sitio,
- revisa servicios,
- inicia sesión,
- solicita atención,
- genera un ticket,
- lleva su equipo a sucursal o solicita servicio a domicilio,
- y después puede darle seguimiento a su caso desde la plataforma.

La inspiración sí viene de la organización por tickets que usan muchos entornos técnicos, pero aquí se adapta a un **modelo comercial de atención al cliente**.

---

# 2. Idea base del proyecto

Cuando una persona necesita reparar su computadora, muchas veces el proceso se maneja de forma informal:

- manda un mensaje,
- llama,
- explica el problema varias veces,
- no tiene un número de seguimiento,
- no sabe en qué estado va su equipo,
- y el negocio tampoco tiene un control claro de sus casos.

Nuestro proyecto nace justamente para resolver eso.

Queríamos transformar un negocio de reparación en una atención más profesional, donde cada servicio solicitado quede registrado y pueda ser seguido de principio a fin.

---

# 3. Problema que resuelve

El proyecto resuelve principalmente la **falta de orden y seguimiento en la atención de clientes de soporte técnico**.

Antes de una solución así, pueden existir problemas como:

- pérdida de información del cliente,
- falta de historial del caso,
- desorganización entre solicitudes,
- poca claridad sobre el estado de la reparación,
- dificultad para cotizar o priorizar servicios,
- mala comunicación entre negocio y cliente.

Con nuestra plataforma, cada caso queda registrado como ticket y puede consultarse posteriormente.

---

# 4. Qué ofrece la solución

La plataforma permite:

- mostrar servicios del negocio,
- explicar cada servicio con mayor detalle,
- registrar usuarios,
- iniciar sesión,
- solicitar cotizaciones,
- generar tickets con folio,
- dar seguimiento al estado del ticket,
- mantener mensajes asociados al caso,
- administrar servicios, usuarios y contenido del sitio.

Esto convierte la página en algo más que un catálogo: la vuelve una herramienta de operación para el negocio.

---

# 5. Objetivo del proyecto

Diseñar e implementar una plataforma web para un negocio de reparación de computadoras que permita centralizar el catálogo de servicios, la generación de tickets, la atención al cliente y el seguimiento técnico, mejorando la organización del trabajo y la experiencia del usuario.

---

# 6. Cómo funciona el sistema

## Cliente
El cliente puede:

- crear su cuenta,
- iniciar sesión,
- revisar servicios,
- solicitar una cotización,
- generar un ticket,
- consultar el estado de su caso,
- ver mensajes de seguimiento.

## Técnico
El técnico puede:

- revisar tickets,
- actualizar estados,
- responder mensajes,
- dar continuidad a los casos,
- revisar solicitudes de contacto.

## Administrador
El administrador puede:

- gestionar servicios,
- gestionar productos,
- gestionar usuarios,
- revisar pedidos,
- modificar contenido principal del sitio,
- supervisar tickets y contactos.

---

# 7. Flujo del cliente dentro del sistema

1. El cliente entra al sitio.
2. Ve los servicios disponibles.
3. Se registra o inicia sesión.
4. Solicita una cotización.
5. Describe el problema de su equipo.
6. El sistema genera un ticket con folio.
7. El negocio atiende el caso en sucursal o a domicilio.
8. El cliente consulta el avance desde su cuenta.

---

# 8. Por qué está basado en tickets

Decidimos usar tickets porque permiten que cada caso tenga:

- un identificador,
- una descripción clara,
- un historial,
- un estado de avance,
- y un seguimiento ordenado.

Aunque los tickets suelen verse mucho en empresas, también tienen mucho sentido en un negocio de reparación, porque ayudan a profesionalizar la atención al cliente.

---

# 9. Qué hace diferente a este proyecto

Hay muchos sitios de reparación que solo muestran información o un número telefónico.

Lo que hace diferente a este proyecto es que:

1. **no se queda en lo informativo**,
2. **sí organiza la operación del negocio**,
3. **permite seguimiento posterior**,
4. **integra cotización, ticket y atención**,
5. **maneja roles distintos**, 
6. **considera atención en sucursal y a domicilio**, 
7. **está pensado para evolucionar a algo más real**.

En pocas palabras: no es solo una página bonita, sino una propuesta funcional para administrar mejor un negocio técnico.

---

# 10. Qué tecnologías usamos

- **Python** como lenguaje principal.
- **Flask** para la lógica web.
- **MySQL** para la base de datos.
- **HTML, CSS y JavaScript** para la interfaz.
- **Jinja2** para contenido dinámico.
- **dotenv** para configuración del entorno.

También se trabajó con una estructura modular para separar autenticación, rutas públicas, paneles y lógica compartida.

---

# 11. Qué aprendimos al desarrollarlo

Durante el proyecto aprendimos a:

- desarrollar una aplicación web completa,
- conectar frontend y backend,
- trabajar con base de datos relacional,
- crear roles y permisos,
- modularizar código,
- documentar e inicializar un proyecto para trabajo en equipo,
- pensar una solución tecnológica basada en una necesidad real.

---

# 12. Retos que resolvimos

Entre los retos más importantes estuvieron:

- estructurar correctamente la base de datos,
- mantener el código ordenado,
- controlar accesos por rol,
- validar información de usuarios,
- permitir seguimiento por ticket,
- dejar el sistema replicable en otras computadoras,
- mejorar la interfaz para que se viera más profesional.

---

# 13. Valor del proyecto

El valor del proyecto está en que propone una forma más profesional de atender clientes dentro de un negocio de reparación de computadoras.

No solo busca mostrar servicios, sino organizar:

- quién solicitó el servicio,
- qué problema reportó,
- qué estado tiene el caso,
- qué seguimiento se ha dado,
- y cómo se mantiene la comunicación con el cliente.

Eso ayuda a mejorar la experiencia de atención y la imagen del negocio.

---

# 14. Guion corto para exposición (2 a 3 minutos)

## Versión lista para decir

> Buenas tardes. Nuestro proyecto se llama **IT'S NOT THE CHARGER** y consiste en una plataforma web para un negocio de reparación y soporte técnico de computadoras.
>
> La idea surge porque muchos negocios de este tipo atienden a sus clientes de forma muy informal, por ejemplo por mensajes o llamadas, lo que puede generar desorden, pérdida de seguimiento o mala comunicación.
>
> Nosotros propusimos una solución en la que el cliente puede entrar al sitio, revisar servicios, registrarse, solicitar una cotización y generar un ticket con folio para darle seguimiento a su caso. Después, el negocio puede atenderlo en sucursal o a domicilio y actualizar el estado del servicio dentro de la misma plataforma.
>
> El sistema maneja roles como cliente, técnico y administrador. De esta forma, cada usuario tiene funciones específicas y el flujo de trabajo se mantiene organizado.
>
> A nivel técnico utilizamos Python, Flask, MySQL, HTML, CSS y JavaScript. También estructuramos el proyecto por módulos para hacerlo más limpio y mantenible.
>
> Consideramos que este proyecto tiene valor porque no es solo una página de presentación, sino una propuesta funcional para mejorar la operación de un negocio real de soporte técnico. Muchas gracias.

---

# 15. Guion más completo (4 a 5 minutos)

> Buenas tardes. Nosotros desarrollamos **IT'S NOT THE CHARGER**, una plataforma web orientada a la gestión de un negocio de reparación y soporte técnico de computadoras.
>
> La inspiración del proyecto viene de observar que muchos negocios técnicos todavía trabajan de forma poco organizada: reciben solicitudes por mensajes, llamadas o redes sociales, pero no siempre existe un control claro de los casos, del seguimiento o del estado de cada reparación.
>
> A partir de esa necesidad, diseñamos una plataforma donde el cliente puede consultar servicios, registrarse, iniciar sesión y generar una solicitud de atención por medio de una cotización que se convierte en ticket. Ese ticket queda registrado con un folio y puede ser consultado posteriormente.
>
> El sistema también contempla la realidad del negocio, ya que el servicio puede brindarse en sucursal o a domicilio. Además, el cliente puede dar seguimiento a su caso desde su panel.
>
> Una parte importante del proyecto es el manejo de roles. El cliente puede consultar sus tickets, el técnico puede revisar y actualizar incidencias, y el administrador puede gestionar usuarios, servicios, productos y contenido del sitio.
>
> En la parte técnica utilizamos Flask, MySQL, HTML, CSS y JavaScript. También modularizamos el proyecto para separar lógica pública, autenticación, paneles y reglas compartidas del negocio.
>
> Lo que hace diferente a nuestro proyecto es que no se limita a ser una página informativa, sino que organiza la operación del negocio mediante tickets, seguimiento y control por roles.
>
> En conclusión, nuestra propuesta busca mostrar cómo un negocio de reparación puede mejorar su atención al cliente mediante una plataforma digital más organizada, profesional y escalable. Muchas gracias.

---

# 16. Orden recomendado para la demostración en vivo

## Demo corta de 2 minutos

1. Mostrar inicio.
2. Explicar que es un negocio de reparación de computadoras.
3. Mostrar catálogo de servicios.
4. Entrar con usuario cliente.
5. Mostrar ticket o detalle de seguimiento.
6. Entrar a panel técnico o admin.
7. Mostrar cambio de estado o mensajes.

## Frase guía para la demo

> Aquí podemos ver cómo el cliente solicita atención y cómo el negocio puede organizar el seguimiento del caso dentro de la misma plataforma.

---

# 17. Preguntas que podrían hacer y cómo responderlas

## ¿En qué se basaron?

> Nos basamos en la lógica de organización por tickets, pero la adaptamos a un negocio de reparación de computadoras orientado a clientes externos, no a una empresa interna.

## ¿Qué problema soluciona?

> Soluciona la falta de seguimiento y organización en la atención de clientes, permitiendo registrar, consultar y administrar cada caso de manera más ordenada.

## ¿Por qué usar tickets en un negocio pequeño?

> Porque incluso en un negocio pequeño puede haber varios casos simultáneos. Los tickets ayudan a identificar cada servicio, mantener historial y evitar desorden.

## ¿Por qué es diferente a otros sitios de reparación?

> Porque no solo informa sobre servicios, sino que permite operación real: registro, cotización, tickets, seguimiento y gestión por roles.

## ¿Por qué sería útil en la vida real?

> Porque mejora la atención al cliente, da mayor control al negocio y permite llevar mejor registro de cada solicitud.

## ¿Qué es lo más valioso del proyecto?

> Que une la parte comercial del negocio con una organización operativa real mediante una plataforma digital.

## ¿Qué fue lo más difícil?

> Organizar correctamente la lógica por roles, la base de datos y el flujo de tickets sin que el proyecto se volviera desordenado.

## ¿Qué mejorarían en el futuro?

> Notificaciones, métricas, despliegue en nube, pagos en línea y funciones más avanzadas de seguimiento al cliente.

---

# 18. Reparto sugerido para 4 integrantes

## Integrante 1
- Presentación del negocio y del problema.
- Explicación de la idea base.

## Integrante 2
- Explicación del flujo del cliente.
- Sistema de tickets y seguimiento.

## Integrante 3
- Tecnologías utilizadas.
- Arquitectura y organización del sistema.

## Integrante 4
- Demostración en vivo.
- Valor, diferencias y mejoras futuras.

---

# 19. Versión ultra corta por si solo tienes 1 minuto

> Nuestro proyecto se llama **IT'S NOT THE CHARGER** y es una plataforma web para un negocio de reparación de computadoras. Permite mostrar servicios, registrar clientes, generar tickets, dar seguimiento a casos y organizar la atención en sucursal o a domicilio. Fue desarrollado con Flask, MySQL, HTML, CSS y JavaScript y busca profesionalizar la atención de un negocio técnico.

---

# 20. Recomendaciones al exponer

- No expliquen el código desde el principio.
- Primero expliquen el negocio.
- Después expliquen el problema.
- Luego expliquen la solución.
- Al final mencionen la tecnología y el aprendizaje.

La estructura más fuerte para presentar este proyecto es:

**negocio -> problema -> solución -> demo -> valor -> mejoras futuras**

---

# 21. Cierre sugerido

> En conclusión, nuestro proyecto propone una forma más organizada, profesional y funcional de atender clientes dentro de un negocio de reparación de computadoras, usando herramientas web que permiten dar seguimiento real a cada caso.
