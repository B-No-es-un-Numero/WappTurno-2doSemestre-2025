# WappTurno: Gestión de Turnos con WhatsApp

## Descripción del proyecto
El proyecto elegido para desarrollar en el área de la salud es un sistema web de gestión de turnos, que permitirá a los usuarios realizar altas, ediciones y cancelaciones de sus turnos de manera sencilla y eficiente. Además como incorporación de la futura tienda virtual se agregará como parte del flujo una pasarela de pago donde los usuarios puedan pagar sus consultas de forma adelantada.

Como valor agregado, el sistema incorporará la integración con WhatsApp para el envío automático de mensajes de confirmación y recordatorio de los turnos solicitados, mejorando así la comunicación con los pacientes


## Funcionalidades y/o areas de enfoque del proyecto 

Esta aplicación de gestión de turnos buscaria optimizar la asignación y administración de citas, reduciendo tiempos de espera y mejorando la experiencia tanto para los proveedores de servicios como para los usuarios finales.

- Reserva Online 24/7: Permitiria a los usuarios solicitar y confirmar turnos en cualquier momento y desde cualquier lugar, eliminando la necesidad de llamadas telefónicas.
- Visualización de Disponibilidad en Tiempo Real: Mostraria los horarios disponibles de profesionales o recursos (salas, equipos) de forma clara y actualizada.
- Confirmación y Recordatorios Automatizados: Envío de notificaciones por WhatsApp, SMS, email o dentro de la aplicación para confirmar el turno y recordar la cita, reduciendo el ausentismo.
- Anulación y Reprogramación Sencilla: Facilita a los usuarios la cancelación o el cambio de sus turnos de manera autónoma, liberando espacios para otros.
- Gestión de Recurrentes: Posibilidad de programar turnos periódicos para tratamientos o consultas regulares.
- Perfiles de Profesionales/Servicios: Creación de perfiles detallados para cada profesional o servicio, incluyendo especialidad, disponibilidad, datos de contacto y, si aplica, biografía o experiencia.
- Servicios Configurables: Definicion de diferentes tipos de servicios (consultas, estudios, tratamientos) con duraciones y costos asociados.

## Posibles Usuarios de la Aplicación
La versatilidad de esta aplicación de gestión de turnos permitiria abarcar un amplio abanico de usuarios, tanto proveedores como consumidores de servicios.

1. Sector Salud (Enfoque Principal)

- Clínicas y Hospitales: Gestión de turnos para consultas médicas, estudios de laboratorio, resonancias, fisioterapia, etc.
- Consultorios Médicos Independientes: Médicos, odontólogos, psicólogos, nutricionistas.
- Centros de Kinesiología y Rehabilitación.
- Laboratorios de Análisis Clínicos.
- Veterinarias.
- Centros de Estética Médica.


## Tecnologías utilizadas
**Front end:**
- **HTML5** → estructura del contenido.
- **CSS3** → estilos y diseño responsivo.
- **Boostrap** → utilización de componentes.
- **JavaScript** → interacción y lógica en el navegador.

**Back end:**
- **Python** → lenguaje principal para la lógica del servidor.
- **MySQL** → base de datos relacional para almacenar la información.


## Consideraciones técnicas
**Backend**
- Se optó por un patrón arquitectónico DAO, a fin de separar claramente la lógica de negocio de la conexión y trabajo con la db.
- Para el sprint 1, atendiendo a que solamente se trabajó con las funcionalidades del usuario, se sostuvo una modularización mínima (módulos User.py, User_service.py, User_DAO.py). Las carpetas necesarias (models, services, dao, etc), así como interfases y demás clases planteadas en los diagramas serán añadidas en posteriores sprint, de acuerdo a los requerimientos específicos del módulo de fullstack. 
- Para facilitar el trabajo colectivo, cada desarrollador generó un entorno virtual en el cual se cargaron los requerimientos de packages con sus correspondientes versiones.
- También se trabajó incorporando .env para evitar la exposición de información sensible sobre la base de datos, así como .gitignore, para no sobrecargar el proyecto con archivos innecesarios.

- Se optó por mantener las ids como String (UUID), dado que se trata en su mayoría de información altamente sensible (Diagnósticos de pacientes, sus tratamientos, etc).

- Tal como se planteó en los diagramas, se procedió a desarrollar eliminado lógico (no físico, sino como "enabled = False") para las entidades, a fin de conservar la integridad de los registros en la base de datos. Asimismo, dado el requerimiento técnico del módulo fullstack de incorporar la función "eliminar usuario" como únicamente accesible a administrador, en este caso también se desarrolló el eliminado *físico* de usuario. El eliminado *lógico* de usuario (dar de baja la cuenta) sigue vigente para el propio usuario aunque no sea administrador.

- Para conservar la integridad de los registros en base de datos, evitar errores en el guardado de la información o fallas mayores, como dejar la conexión a la base de datos abierta, se pensaron los métodos get -llamados internamente para corroboraciones de otros métodos como register, login, updates...- con parámetros optativos, para definir cuándo la conexión debía mantenerse abierta momentáneamente, para cerrarse luego de que el método de orden superior arrojara el resultado.

**Frontend**
- Para ejecutar el proyecto de forma local, basta con abrir el archivo `index.html` en cualquier navegador moderno.

- La carpeta `pages/` contiene todas las pantallas del proyecto, entre ellas:
    - `index.html` → **Página principal (home)**
    - `contact.html` → **Página de contacto**
    - `services.html` → **Listado de servicios**
    - `register.html` y `login.html` → **Pantallas de autenticación**
    - `dashboard.html`, `profile.html`, `my-appointments.html`, `new-appointment.html` → **Páginas de usuario y gestión interna**
- El sitio tiene un diseño **responsivo** y ordenado.  
- Para facilitar la navegación, cada archivo `.html` está vinculado mediante un **menú superior** y enlaces internos.  
- Los **estilos** y **scripts** se mantienen en archivos separados para garantizar una buena organización y facilitar futuras modificaciones.  


## Participantes:
 - *Alvaro Fernando Galiño Velez*
 - *Flavia Guadalupe Sicchar Gómez*
 - *Gabriel Natale* 
 - *Guillermo Diván*
 - *Joaquín Romero* 
 - *Melina Belén Bruvera*
