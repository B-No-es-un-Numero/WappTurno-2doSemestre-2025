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
- El sistema está organizado bajo un patrón de capas. Este enfoque modular permite mantener separación de responsabilidades y facilita testeo y mantenimiento.
    - Presentation: interacción con el usuario (menús).
    - Models: entidades y enumeraciones.
    - Services: lógica de negocio, esto es, los métodos y validaciones correspondientes a las entidades.
    - Persistence: conexión a base de datos, siguiendo patrón DAO, separado de la lógica de negocios e implementado por esta.

Para el sprint 1, atendiendo a que *solamente* se trabajó con las funcionalidades del usuario, se sostuvo una modularización mínima (módulos User.py, User_service.py, User_DAO.py). La misma modularización se mantuvo para las otras clases, sus métodos y conexión a base de datos.

Para el sprint 2 (primer MVP), se realizó la división necesaria en carpetas (models, services, dao, etc) y la creación de las demás clases planteadas en los diagramas, puestos a punto específicamente para representar el estado final de este primer MVP.

- Para facilitar el trabajo colectivo, cada desarrollador generó un entorno virtual en el cual se cargaron los requerimientos de packages con sus correspondientes versiones.

- También se trabajó incorporando .env para evitar la exposición de información sensible sobre la base de datos, así como .gitignore, para no sobrecargar el proyecto con archivos innecesarios. Se agregó un .env template para que otros programadores ajenos al equipo de desarrollo pudieran ejecutar localmente con mayor facilidad el presente programa.

- El módulo connection_mysql.py se encarga de gestionar la conexión a MySQL leyendo las credenciales desde variables de entorno (.env). El método create_connection() devuelve una conexión activa a MySQL sin manejos de error, ya que los mismos son abordados en los métodos de los DAOs que le aplican.

- En el script de creación de las diversas tablas necesarias en la base de datos, se agregó al final una sentencia de poblamiento específica a Medical_consultations; estas son prácticas médicas registradas por código (hay varios a nivel nacional, para este proyecto se utilizó el de PAMI) para dar cuenta de las prácticas más comunes, lo cual reviste valor trabajando con Obras Sociales, equipos de salud y pacientes, tanto para mantener claridad como confidencialidad.
Los códigos ingresados fueron una mínima parte (a modo de ejemplo). En iteraciones posteriores, sería necesario ingresar la totalidad de los mismos.

- Se optó por mantener las ids como String (UUID), dado que se trata en su mayoría de información altamente sensible (Diagnósticos de pacientes, sus tratamientos, etc).

- Tal como se planteó en los diagramas, se procedió a desarrollar eliminado lógico (no físico, sino como "enabled = False") para las entidades, a fin de conservar la integridad de los registros en la base de datos. Asimismo, dado el requerimiento técnico del módulo fullstack de incorporar la función "eliminar usuario" como únicamente accesible a administrador, en este caso también se desarrolló el eliminado *físico* de usuario. El eliminado *lógico* de usuario (dar de baja la cuenta) sigue vigente para el propio usuario aunque no sea administrador.
Por otra parte, se agregó como regla de negocio que no pueda eliminarse un turo (eliminado *lógico* , sólo accesible para administrador) si el mismo no se encuentra cancelado previamente (update de estado, accesible a todos los roles).

- Para conservar la integridad de los registros en base de datos, evitar errores en el guardado de la información o fallas mayores, como dejar la conexión a la base de datos abierta, se pensaron los métodos get -llamados internamente para corroboraciones de otros métodos como register, login, updates...- con parámetros optativos, para definir cuándo la conexión debía mantenerse abierta momentáneamente, para cerrarse luego de que el método de orden superior arrojara el resultado.

- Se refactorizaron menúes, partiendo de Menu.py para el login y register, derivando según rol (enum) a tres menúes específicos que, a su vez, heredan de Base_user_menu.py las funcionalidades compartidas por los tres.

- Si bien se optó por realizar algunas validaciones en la capa menú, la mayoría de las mismas se encuentran en las capas más internas (services, excepcionalmente como parte del select en una query, en DAO). 
Asimismo, lo opuesto sucede con los mensajes de error, estableciendo en menú aquellos que deberían llegar al usuario y limitando en services y DAOs los que deberían ser vistos solamente por el equipo de desarrollo.

- En sprints posteriores se continuará con la refactorización del código, evitando la repetición de funcionalidades, sobre todo a lo que atañe a prints de turnos y funciones relacionadas.

**Frontend**
- Para ejecutar el proyecto de forma local, basta con abrir el archivo `index.html` en cualquier navegador moderno.

- La carpeta `pages/` contiene todas las pantallas del proyecto, entre ellas:
    - `index.html` → **Página principal (home)**
    - `about.html` → **Página Quienes somos**
    - `contact.html` → **Página de contacto**
    - `services.html` → **Listado de servicios**
    - `register.html` y `login.html` → **Pantallas de autenticación**
    - `dashboard.html`, `profile.html`, `my-appointments.html`, `new-appointment.html` → **Páginas de usuario y gestión interna**
- El sitio tiene un diseño **responsivo** y ordenado.  
- Para facilitar la navegación, cada archivo `.html` está vinculado mediante un **menú superior** y enlaces internos.  
- Los **estilos** y **scripts** se mantienen en archivos separados para garantizar una buena organización y facilitar futuras modificaciones.  
- Se agregaron validaciones y funcionalidad al formulario en página de contacto.
- Se agregó cartelería avisando los estados de éxito y error del envío. Se trabajará en posteriores sprints para que este y las demás funcionalidades sean más amigables al usuario.
- Se estableció la lógica de flujo para que, si se trata de sacar un turno sin estar logueado, se realice la redireccion pertinente para ello. 
- El login y otras funcionalidades se encuentran implementados solamente con valores específicos en la app, ya que aún no se encuentra realizada la conexión a base de datos (requisito de sprint posterior).


## Participantes:
 - *Alvaro Fernando Galiño Velez*
 - *Flavia Guadalupe Sicchar Gómez*
 - *Gabriel Natale* 
 - *Guillermo Diván*
 - *Joaquín Romero* 
 - *Melina Belén Bruvera*
