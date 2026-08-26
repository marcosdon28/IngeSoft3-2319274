# Decisiones

Bitácora de decisiones técnicas del semestre. Se acumula: cada TP agrega su sección abajo, sin
reescribir lo anterior.

Repositorio: <https://github.com/marcosdon28/IngeSoft3-2319274>

---

## TP1 — Git colaborativo

### Por qué Git no pudo resolver el conflicto solo

Git fusiona automáticamente cuando dos ramas tocan **partes distintas** del archivo: compara ambas
puntas contra el ancestro común y, si los cambios no se superponen, los aplica a los dos.

Acá eso no era posible. Las ramas `feature/titulo-a` y `feature/titulo-b` salieron **las dos del
mismo commit de `main`** y modificaron **exactamente la misma línea** — la primera del `README.md`.
Cuando la rama A entró a `main`, esa línea decía `# Proyecto IngSoft3 - versión A`; la rama B, que
seguía viendo el texto viejo, quería dejarla en `# Proyecto IngSoft3 - versión B`.

Git tiene toda la información del problema y **ninguna para resolverlo**: sabe que la línea cambió
de dos formas incompatibles, pero no puede saber cuál es "la correcta" — eso no es una pregunta
técnica, es una decisión de contenido. Elegir por su cuenta significaría descartar silenciosamente
el trabajo de alguien. Por eso hace lo único razonable: marca el archivo con `<<<<<<<`, `=======` y
`>>>>>>>`, y delega la decisión a una persona.

**Qué habría tenido que pasar para que nunca apareciera.** Tres cosas, en orden de importancia:

1. **Integrar seguido.** Si antes de empezar la rama B hubiera hecho `git switch main && git pull`,
   B habría nacido del `main` que ya tenía el cambio de A: no hay dos versiones compitiendo, hay una
   sobre la otra. El conflicto no nace de tocar la misma línea, nace de **tocarla partiendo de
   estados distintos**.
2. **Ramas cortas.** Cuanto más vive una rama, más se aleja de `main` y más superficie de choque
   acumula. Ramas de horas producen conflictos triviales; ramas de semanas producen *merge hell*.
   Es lo que la investigación DORA correlaciona con alto rendimiento: integrar a trunk al menos una
   vez por día.
3. **Trabajo repartido.** Si dos personas necesitan tocar la misma línea al mismo tiempo, en general
   es señal de que las tareas no estaban bien separadas.

**Qué elegí al resolverlo.** Ni la versión A ni la B: una **síntesis**. Los sufijos «versión A» y
«versión B» existían sólo para fabricar el conflicto — quedarme con cualquiera de los dos habría
dejado el README del semestre con un título de ejercicio. Resolví con
`# Proyecto IngSoft3 — Inventario de productos (UCC 2026)`, que es el título que el proyecto
necesita. Es justamente el punto: resolver un conflicto es **decidir contenido**, y a veces el
contenido correcto no es ninguna de las dos ramas.

Y una aclaración que importa: **el conflicto no es un error ni una falla de Git**. Es la consecuencia
natural del trabajo en paralelo, y que Git lo exponga en vez de resolverlo mal es la conducta
correcta. Lo evitable no es el conflicto: es el conflicto *gigante*.

### Decisiones de configuración y por qué

| Decisión | Por qué |
|---|---|
| **Protección de `main` con `enforce_admins: true`** | Sin esto GitHub deja que el dueño del repo saltee la regla, y una protección que el dueño puede saltear no protege nada. Con esto, la regla me alcanza a mí también — y es lo que se ve en la evidencia 1 |
| **Cero aprobaciones obligatorias** | GitHub **nunca** permite aprobar el propio Pull Request (la opción aparece deshabilitada; por API devuelve `422 Can not approve your own pull request`). Como el TP es individual, exigir 1 aprobación haría imposible mergear. En un equipo real acá iría 1 o más |
| **Protección configurada por API (`gh api`) y no por la web** | Queda **reproducible y auditable**: es un comando que puedo volver a correr y versionar, en vez de tres tildes que nadie sabe si se movieron. Es el mismo principio de *policy as code* que después aplica a los pipelines. Verifiqué el resultado leyendo la protección de vuelta con `gh api … --jq` |
| **Squash and merge** | Un commit por PR: el historial de `main` queda lineal y legible, y revertir un cambio completo es un solo `git revert`. Se pierde el paso a paso interno de la rama, que en ramas cortas no aporta. La alternativa (merge commit) conserva trazabilidad total a costa de ruido visual con muchos PRs |
| **Convención de ramas `feature/`, `fix/`, `docs/`, `ci/`** | Es la de la materia, y hace que el nombre de la rama diga de qué tipo es el cambio antes de abrirla |
| **`aprendizajes.md` y `notas-defensa-p1.md` ignorados vía `.git/info/exclude`** | Son notas personales de estudio, no parte del entregable. `.gitignore` se versiona y viaja a todo el que clone; `.git/info/exclude` es el ignore **privado de este clon**. Contrapartida asumida: si clono el repo en otra máquina, el exclude no viene y hay que rehacerlo — queda anotado en `CLAUDE.md` |
| **`CLAUDE.md` en la raíz** | Deja escritas las reglas de trabajo del repo (todo por PR, cuándo se actualiza cada archivo, cómo se cierra cada TP). Que la convención esté en un archivo y no en la memoria es la misma idea que la protección de rama: el proceso no debería depender de que alguien se acuerde |

### Problemas encontrados y cómo los resolví

- **El orden de los pasos no es opcional.** El `.gitignore` y el `CLAUDE.md` se commitearon **antes**
  de activar la protección. Si hubiera activado la protección primero, ese commit inicial también
  habría necesitado un PR — que es correcto, pero significa que el repo nunca tiene un push directo,
  ni siquiera el primero. Lo dejé así a propósito y lo declaro: **hay exactamente un push directo a
  `main` en el historial**, el commit `05444d1`, hecho antes de que la protección existiera.

- **Al fabricar el conflicto casi lo arruino.** La rama B tiene que salir de `main`, no de la A. Si
  B nace de A ya tiene el cambio de A adentro y el merge entra limpio: no hay conflicto y el
  ejercicio se pierde. Lo resolví creando explícitamente cada rama desde `main`
  (`git switch -c feature/titulo-b main`, nombrando la base) en vez de confiar en dónde estaba
  parado.

- **GitHub no sabe al instante si un PR tiene conflicto.** Apenas mergeé la rama A, consultar el
  estado del PR de B devolvía `mergeable: UNKNOWN` / `mergeStateStatus: UNKNOWN`. No estaba roto:
  GitHub recalcula la mergeabilidad de forma asíncrona. Volviendo a consultar unos segundos después
  pasó a `CONFLICTING` / `DIRTY`. Es el mismo motivo por el que la guía avisa que, después de
  resolver, a veces hay que esperar unos segundos antes de poder mergear.

- **`sed -i` en macOS no es el de Linux.** Para reemplazar la primera línea del README, `sed -i` pide
  un argumento de sufijo de backup: en macOS hay que escribir `sed -i '' '1s/.*/…/' README.md` (con
  las comillas vacías), mientras que en Linux es `sed -i '1s/.*/…/'`. Sin las comillas vacías, macOS
  interpreta el patrón como nombre de archivo de backup y falla.

- **No pude capturar la terminal con una captura de pantalla del sistema.** El proceso desde el que
  trabajo no tiene el permiso de *Grabación de pantalla* de macOS: `screencapture` devuelve el fondo
  de escritorio sin ninguna ventana. En vez de dejar la evidencia 1 incompleta, hice dos cosas:
  (a) la salida real del `git push` rechazado quedó **transcripta literalmente** en `evidencias.md`,
  además de renderizada como imagen; y (b) agregué dos evidencias equivalentes tomadas del navegador
  —el editor web de GitHub negándose a commitear a `main`, y la regla de protección con sus casillas
  tildadas—. Las tres muestran la misma política desde ángulos distintos.

- **Playwright me hizo capturar páginas deslogueadas sin avisar.** Para detectar si había sesión
  iniciada chequeaba que existiera el `<meta name="user-login">` de GitHub. Existe **también cuando
  estás deslogueado**, con el atributo `content` vacío — así que el chequeo daba positivo siempre y
  las primeras capturas salieron con los botones *Sign in / Sign up*, sin el cuadro de merge (GitHub
  no se lo muestra a un visitante anónimo). Lo arreglé exigiendo que el `content` **no esté vacío**.
  La lección es más general que Playwright: *"el elemento existe"* y *"el elemento tiene el valor que
  espero"* no son la misma verificación.

- **El botón *Commit changes* de GitHub está deshabilitado hasta que edites algo.** Al automatizar la
  captura del editor web, el click al botón se caía por timeout. No era un selector mal escrito: el
  botón nace deshabilitado y recién se activa cuando el archivo cambió. Se resolvió escribiendo algo
  en el editor antes de intentar el click.

- **El conflicto lo resolví desde la consola, no desde el editor web.** Las capturas 2 y 3 se
  tomaron de la web (que es donde el conflicto se ve mejor), pero la resolución la hice localmente
  con `git switch feature/titulo-b && git merge origin/main`, editando el archivo y commiteando —
  el camino que la propia guía documenta en su bloque *"Lo mismo por consola"*. Es determinista y
  deja el commit de resolución con un mensaje explicando la decisión, que es lo que se lee después
  en el historial.

- **El tag `v1.0.0` está movido, y lo declaro.** Siguiendo el orden de la guía, la release se publicó
  antes de agregar `decisiones.md` y `evidencias.md` (que son justamente los que documentan esa
  release). Como el reglamento dice que el tag es "el punto exacto que se mira de cada TP", moví el
  tag al commit final del TP con `git tag -f v1.0.0 && git push -f origin v1.0.0`, que es el
  procedimiento que el propio reglamento (§3) contempla.

### Declaración de uso de IA

Usé **Claude Code (Claude Opus)** como asistente durante todo el TP1. Concretamente:

| Qué fue asistido | Cómo lo verifiqué |
|---|---|
| Ejecución de los comandos de `git` y `gh` (crear el repo, ramas, PRs, merges, tag) | Cada comando lo leí antes de que corriera y comprobé su efecto en la web de GitHub: el repo existe y es público, los PRs figuran mergeados con su diff, la rama quedó borrada, el tag aparece en *Releases* |
| Configuración de la protección de `main` por API | La leí de vuelta con `gh api "repos/{owner}/{repo}/branches/main/protection"` y comparé campo por campo contra lo que muestra *Settings → Branches* en la web. Y sobre todo: **la probé** — el push directo tiene que fallar, y falla (evidencia 1) |
| Redacción inicial de `decisiones.md`, `evidencias.md` y del informe en PDF | Los revisé y corregí para que digan lo que efectivamente pasó en mi repo. Los problemas listados arriba son los que me pasaron a mí, no ejemplos genéricos |
| Las capturas de evidencia del navegador (1.b, 1.c, 2, 3 y 4) | Se tomaron automatizando Chrome con **Playwright** contra este mismo repositorio y con mi sesión de GitHub. Verifiqué **cada imagen a ojo** antes de aceptarla — y de hecho descarté las dos primeras tandas: una salió deslogueada y otra con un tooltip tapando la interfaz. Las URLs de las capturas son públicas: cualquiera puede abrir el PR #3 o la release y contrastar |
| El `.gitignore` y la estructura de `CLAUDE.md` | Contrasté el `.gitignore` contra el propuesto en la guía (§4.3) y contra las referencias de <https://github.com/github/gitignore> para Python y Node |

Lo que **no** delegué: la decisión de qué versión conservar al resolver el conflicto, la estrategia
de merge, y el criterio de qué va commiteado y qué no.

La verificación real de todo esto es la del enunciado: si no lo puedo explicar en la defensa, no
cuenta — y por eso llevo además un `aprendizajes.md` local donde anoto qué hace cada comando y qué
me confundió.

---

## TP2 — Contenedores: la app del semestre

### Qué app elegí y por qué

**Un sistema de inventario de productos**, escrito por mí para esta materia: FastAPI (Python 3.12) +
React/Vite + PostgreSQL 16. La escribí en vez de adoptar un proyecto de GitHub porque el criterio 5
de `elegir-app.md` —*entenderla lo suficiente para modificarla en vivo*— se cumple solo cuando el
código es propio, y en la mesa del Integrador hay que hacer un cambio delante del profesor.

Contra los cinco criterios de la guía:

| Criterio | Cómo lo cumple |
|---|---|
| **1. Que corra hoy** | `cp .env.example .env && docker compose up -d --build` levanta los tres servicios. No necesita Python, Node ni PostgreSQL instalados |
| **2. Conocer los comandos de build** | `pip install -r requirements.txt` + `uvicorn app.main:app` en el back; `npm ci` + `npm run build` en el front. Son literalmente las líneas de los Dockerfiles |
| **3. Dónde se configura la base** | En **una sola** variable de entorno: `DATABASE_URL`, leída en `app/config.py`. No está hardcodeada en ningún lado — es lo que va a permitir que la misma imagen apunte a QA y a producción en el TP6 |
| **4. Lógica para testear** | **7 reglas de negocio**, listadas abajo. El TP5 pide 8 tests de backend y 4 de frontend: las reglas dan casos válidos, inválidos y de borde de sobra |
| **5. Entenderla para modificarla** | Es código propio, en capas explícitas: los `services/` no importan FastAPI, así que una regla se lee y se cambia sin tocar HTTP |

**Tamaño**: cuatro pantallas y tres entidades. `elegir-app.md` avisa que más grande no suma nota —
sólo builds más lentos y más puntos de falla.

**Las 7 reglas de negocio** (el corazón de la elección, porque son lo que se va a testear):

| # | Regla | Por qué existe |
|---|---|---|
| 1 | Una salida no puede superar el stock disponible | El stock representa unidades físicas: nunca puede quedar negativo |
| 2 | El SKU es único | Dos productos con el mismo SKU hacen imposible saber cuál se movió |
| 3 | No se puede eliminar una categoría con productos asociados | Evita productos huérfanos; borrar en cascada destruiría datos sin avisar |
| 4 | Precio y stock no negativos; cantidad de movimiento > 0 | Validación de dominio, en el borde de entrada |
| 5 | Descuento por cantidad a partir de un umbral | Cálculo con casos de borde — el umbral es **inclusive** |
| 6 | `stock <= stock_minimo` marca "bajo stock" | Es una **propiedad derivada**, no una columna: no puede desincronizarse del stock real |
| 7 | Un producto inactivo no admite movimientos | Si a un producto dado de baja igual se le pueden cargar movimientos, la baja es decorativa |

> 💡 Un caso que salió de probar la regla 5 y que vale como ejemplo de por qué los bordes importan:
> con el umbral en 10 y 10 % de descuento, **llevar 9 unidades cuesta lo mismo que llevar 10**
> (9 × 1800 = 16.200 y 10 × 1800 × 0,9 = 16.200). No es un bug —es lo que la regla dice— pero es
> exactamente el tipo de cosa que un test de borde expone y una lectura del código no.

### Arquitectura: MVC en FastAPI

| Capa | Dónde vive | Qué sabe |
|---|---|---|
| **Model** | `app/models/` (SQLAlchemy) + `app/schemas/` (Pydantic) | Las entidades y el contrato de la API |
| **Controller** | `app/routers/` + `app/services/` | Los routers traducen HTTP; los **services tienen las reglas** |
| **View** | `frontend/src/` (React) | Presentación; las reglas de la vista viven aisladas en `lib/reglas.js` |

La decisión que más importa: **los `services/` no importan FastAPI**. Lanzan excepciones propias
(`ReglaDeNegocioError`) y los routers las traducen a códigos HTTP. Gracias a eso las reglas se
testean llamando a una función, sin levantar un servidor — que es justo lo que el TP5 va a necesitar.
Lo mismo del lado del front: `lib/reglas.js` son funciones puras, sin React ni `fetch` adentro.

### Decisiones de contenerización

| Decisión | Por qué |
|---|---|
| **Backend: `python:3.12` para build, `python:3.12-slim` para runtime** | La etapa de build trae compilador y herramientas para instalar dependencias; la final sólo necesita ejecutar. Medido: **1,62 GB contra 326 MB** — 5 veces más chica, y sin compilador adentro (menos superficie de ataque) |
| **Las dependencias en un virtualenv (`/opt/venv`) que se copia entre etapas** | Es lo único que tiene que viajar. Ni pip, ni su cache, ni los wheels intermedios llegan a la imagen final |
| **Frontend: `node:22-alpine` para build, `nginx:alpine` para servir** | Una SPA compilada son archivos estáticos: **Node no tiene nada que hacer en producción**. 229 MB contra 93 MB |
| **El archivo de dependencias se copia ANTES que el código** | Cuando una capa cambia, Docker invalida esa capa y todas las siguientes. Con este orden, cambiar una línea de código no re-descarga las dependencias |
| **`npm ci` y no `npm install`** | `ci` respeta el lockfile exacto: el build es reproducible. `install` puede resolver versiones distintas según cuándo se corra |
| **Usuario sin privilegios en el backend** | El contenedor no corre como root. Si alguien logra ejecutar algo dentro, no lo hace con todos los permisos |
| **Dos `.dockerignore`, uno por carpeta de build** | Docker los busca en el **contexto** que se le pasa (`./backend`, `./frontend`), no en la raíz del repo. Por eso son dos archivos con contenidos distintos |

### Qué persiste y qué no

Los contenedores son **efímeros por diseño**: la capa de escritura muere con el contenedor. Eso es
una ventaja para la app (contenedores descartables ⇒ deploys y rollbacks triviales) y una catástrofe
para los datos. Por eso el estado se separa explícitamente:

- **Persiste**: el directorio de datos de PostgreSQL, montado en el volumen **nombrado**
  `db_data:/var/lib/postgresql/data`. Sobrevive a `docker compose down`, a que el contenedor se
  destruya y se recree, y a un cambio de imagen.
- **No persiste**: absolutamente todo lo demás. El backend y el frontend no escriben nada.

Usé **volumen nombrado y no bind mount** (`./datos:/var/lib/...`): en Mac hay una máquina virtual en
el medio, así que un bind mount del directorio de datos de PostgreSQL es notablemente más lento y da
problemas de permisos.

`down` apaga; `down -v` además **olvida**. La evidencia 7 del TP2 muestra las dos cosas.

### `depends_on` no alcanza: por qué el healthcheck

`depends_on` garantiza el orden de **arranque**, no de **disponibilidad**. Que el contenedor de
PostgreSQL haya arrancado no significa que acepte conexiones — hay varios segundos entre una cosa y
la otra, y en ese hueco el backend se conecta, falla y se muere. Por eso el servicio `db` declara un
`healthcheck` con `pg_isready` y el backend espera con `condition: service_healthy`. En los logs se
ve literal: `db Waiting → db Healthy → backend Starting`.

La distinción "arrancó" contra "está listo" reaparece en cada sistema distribuido, y es una de las
preguntas de defensa más previsibles de este práctico.

### Cómo se hablan los tres servicios

- **backend → db**: por el **nombre del servicio** (`Host=db`). Compose crea una red interna con DNS
  embebido, así que no importa en qué IP cayó el contenedor de la base: siempre es `db`.
- **frontend → backend**: el JavaScript de la SPA **corre en el browser**, que vive en mi máquina y
  no dentro de la red de compose — así que el front *no puede* pedirle nada a `http://backend:8000`.
  Elegí la solución (a) de la guía: la SPA llama a **rutas relativas** (`/api/...`) y quien las
  traduce es el servidor de Vite en desarrollo y **nginx** en el contenedor. Dos consecuencias
  buenas: la misma imagen sirve en cualquier entorno (no hay URL compilada adentro), y como para el
  browser todo sale del mismo origen, **no hay CORS que configurar**.
- El `proxy_pass` de nginx usa una **variable** (`set $backend_api http://backend:8000;`) en vez del
  nombre escrito directo. Con el nombre directo, nginx lo resuelve al arrancar y, si el backend
  todavía no existe, se niega a levantar con `host not found in upstream`.

### Los secretos

La contraseña de la base va en `${DB_PASSWORD}`, que sale de un **`.env` que no se commitea** (está
en `.gitignore`). Lo que sí se versiona es `.env.example`, que documenta qué variables hacen falta
sin traer ningún valor real. Por eso el arranque son **dos comandos y no uno**: `cp .env.example .env`
y después `docker compose up -d`. Ese paso manual no es un defecto de la entrega — es el precio de
que el secreto no viaje en el repositorio. En el TP4 esos secretos migran a los secrets de la
plataforma de CI.

### Problemas encontrados y cómo los resolví

- **La app de práctica es .NET y no tenía el SDK instalado.** La primera pasada de la guía se hace
  sobre el sample de la cátedra (.NET 8), y `brew install --cask dotnet-sdk` pide contraseña de
  administrador. Lo resolví con el script oficial `dot.net/v1/dotnet-install.sh --channel 8.0`, que
  instala en `~/.dotnet` **sin privilegios**. Dato para tener a mano: para *construir la imagen* no
  hacía falta —el SDK vive dentro del contenedor— pero sí para el paso de la guía que corre la app
  nativa antes de contenerizarla, que es el que te enseña cómo se ve "funcionando" antes de meter
  Docker en el medio.

- **`npm ci` falló en el build: no había `package-lock.json`.** Escribí el `package.json` a mano y
  fui directo al `docker build`, sin haber corrido nunca `npm install`. `npm ci` **exige** el
  lockfile — es justamente lo que lo hace reproducible. Se resolvió con un `npm install` local que lo
  generó, y el lockfile quedó commiteado, que es donde tiene que estar.

- **`docker images mcr.microsoft.com/dotnet/sdk:8.0` no mostraba nada.** Docker 29 guarda las
  imágenes base de las etapas de build en el **cache de construcción**, no en el store de imágenes,
  así que el comando de comparación de la guía devolvía la tabla vacía. No estaba roto: hay que
  bajarlas explícitamente con `docker pull` para poder compararlas. Es un detalle de versión, y vale
  la pena saberlo porque el mensaje no sugiere nada.

- **Los packages de ghcr nacen privados.** Después del `push`, `gh api /user/packages` los mostraba
  como `private` — y mientras lo estén, nadie puede hacer `docker pull`: ni la cátedra, ni otra
  máquina, ni un pipeline. Hay que cambiar la visibilidad a **Public** desde la página del package,
  y hacerlo **para las dos** imágenes.

- **El token de `gh` no tenía permiso para publicar imágenes.** El scope `write:packages` no venía en
  el token del TP1. Se agrega con `gh auth refresh -h github.com -s write:packages`, que abre un
  device flow en el navegador. Aviso de la guía que conviene tener presente: el `docker login` da
  `Succeeded` con cualquier token válido y **recién falla el `push`** con `denied` — el login
  exitoso no garantiza el permiso. En mi caso el `refresh` sí tomó el scope y el push funcionó, pero
  la comprobación real es empujar algo.

- **La arquitectura de las imágenes.** Estas imágenes se construyeron en una Mac con chip ARM, así
  que sirven para máquinas ARM. Alguien con Intel/AMD recibiría
  `no matching manifest for linux/amd64` — y los runners de CI del TP7 son Intel. Para este práctico
  alcanza con saberlo y declararlo; en el **TP7** se resuelve con `docker buildx`, que construye para
  las dos arquitecturas a la vez.

### Declaración de uso de IA — TP2

Mismo esquema que en el TP1: usé **Claude Code (Claude Opus)** y lo verifiqué así.

| Qué fue asistido | Cómo lo verifiqué |
|---|---|
| El código de la app (modelos, schemas, services, routers, componentes de React) | **Probé las 7 reglas contra la API levantada**, una por una, comprobando el código HTTP y el mensaje de error de cada una: SKU duplicado → 400, borrar categoría con productos → 400, salida mayor al stock → 400, cantidad cero → 422, producto inactivo → 400, y el descuento en el borde exacto (9 sin descuento, 10 con descuento) |
| Los Dockerfiles, el compose y el `nginx.conf` | Los leí línea por línea y **los probé**: el sistema levanta con un comando, el front habla con el back por el proxy de nginx, y la prueba de persistencia se comporta como esperaba (`down` conserva, `down -v` borra). Los tamaños de imagen los medí, no los estimé |
| La primera pasada sobre el sample de la cátedra | La hice completa antes de tocar mi app, que es lo que el enunciado pide. Ahí vi el 502 del front sin red compartida y la diferencia SDK/runtime con números reales — cuando después apareció lo mismo en mi app, ya sabía qué era |
| Redacción de esta sección y del informe | Los revisé y corregí para que digan lo que efectivamente pasó. Los problemas listados son los que me pasaron a mí |

Lo que **no** delegué: la elección de la app y su dominio, las 7 reglas de negocio, la decisión de
llamar a la API por ruta relativa en vez de URL absoluta, y qué persiste y qué no.
