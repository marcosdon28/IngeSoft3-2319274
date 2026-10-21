# Decisiones

Bitácora de decisiones técnicas del semestre. Se acumula: cada TP agrega su sección abajo, sin
reescribir lo anterior.

Repositorio: <https://github.com/marcosdon28/IngeSoft3-2319274>

## Enlaces del TP7

| Qué | Enlace |
|---|---|
| **Packages** públicos, etiquetados `sha-<commit>` (uno por merge; nunca `latest`) | <https://github.com/marcosdon28/IngeSoft3-2319274/pkgs/container/inventario-backend> · <https://github.com/marcosdon28/IngeSoft3-2319274/pkgs/container/inventario-frontend> |
| **Corrida con integración VERDE y e2e ROJA** (la promoción frenada): commit que rompió la app #38 | <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39644611792> — artefactos `playwright-report-integracion` (verde) y `playwright-report-e2e` (rojo) |
| **Cadena completa verde** posterior, hasta PROD (el arreglo, #39) | <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39646124064> |
| QA (ejecuta la imagen del último merge) | front <https://inventario-front-qa.onrender.com> · api <https://inventario-api-qa.onrender.com> |
| PROD (ejecuta la imagen aprobada) | front <https://inventario-front-prod.onrender.com> · api <https://inventario-api-prod-7xrj.onrender.com> |

## Enlaces del TP6

Lo que no se encuentra navegando el repositorio, en un solo lugar:

| Qué | Enlace |
|---|---|
| **Package backend**, público, etiquetado con el commit de un merge | <https://github.com/marcosdon28/IngeSoft3-2319274/pkgs/container/inventario-backend> — `docker pull --platform linux/amd64 ghcr.io/marcosdon28/inventario-backend:sha-8652e2daf3c31a7b112af0c98a1c4dc04b2db2fe` |
| **Package frontend**, ídem | <https://github.com/marcosdon28/IngeSoft3-2319274/pkgs/container/inventario-frontend> — `docker pull --platform linux/amd64 ghcr.io/marcosdon28/inventario-frontend:sha-8652e2daf3c31a7b112af0c98a1c4dc04b2db2fe` |
| **Cadena, eslabón 2**: la corrida de un PR con los tests en verde donde «Entrar al registry» sale **salteado** (pasó todo y no publicó: sólo `main` publica) | <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39626398611/job/119312661785> |
| **Cadena, eslabón 3**: la lista de pasos de una corrida de `main`, donde «Construir y publicar la imagen» es el **último** paso, después de los tests | <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39633286706/job/119336878808> |
| **QA** | front <https://inventario-front-qa.onrender.com> · api <https://inventario-api-qa.onrender.com> |
| **PROD** | front <https://inventario-front-prod.onrender.com> · api <https://inventario-api-prod-7xrj.onrender.com> |
| Environments y su historial | <https://github.com/marcosdon28/IngeSoft3-2319274/deployments> |

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

- **La arquitectura de las imágenes.** Se construyeron en una Mac con chip ARM, y lo verifiqué en
  vez de suponerlo: `docker manifest inspect` devuelve una sola plataforma real, `linux/arm64` (el
  `unknown/unknown` que aparece al lado es el manifiesto de atestación que agrega BuildKit, no una
  arquitectura). Alguien con Intel/AMD recibiría `no matching manifest for linux/amd64` — y **los
  runners de GitHub Actions son Intel**, así que esto reaparece en el TP7. Ahí se resuelve con
  `docker buildx`, que construye para las dos arquitecturas a la vez. Para este práctico alcanza con
  saberlo y declararlo.

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

---

## TP3 — Planificación y trazabilidad

### La duración del sprint: 1 semana

Elegí **una semana**, alineada al ciclo real de entrega de la materia: la cátedra publica un TP por
semana y la defensa P1 cae en la clase 5. Si el sprint durara dos semanas, el tablero mostraría un
ritmo que no es el que efectivamente tengo — planificaría contra un calendario y trabajaría contra
otro.

El argumento general, más allá de esta materia: **el sprint debería durar lo que dura el ciclo de
feedback**. Sprints largos retrasan el momento en que uno se entera de que estimó mal; sprints muy
cortos gastan más tiempo en la ceremonia que en el trabajo. Acá el feedback llega semanalmente —cada
clase—, así que una semana es lo que corresponde.

Sprint 1: **26/08/2026 – 01/09/2026**.

### El límite de trabajo en progreso: 2

Apliqué la regla de arranque del enunciado: **cantidad de personas + 1**. Trabajando solo, 2.

El «más uno» no es holgura arbitraria: es la **válvula** para cuando algo queda esperando por fuera
de mí —una revisión, una respuesta, un pipeline corriendo— y necesito avanzar en otra cosa sin dejar
la primera a medias. Sin esa unidad extra, el límite obliga a elegir entre bloquearse o hacer trampa.

Por qué un límite en primer lugar: el trabajo empezado y no terminado no vale nada. Cuatro cosas al
60 % entregan cero; dos al 100 % entregan dos. El límite hace **visible** ese costo, que si no queda
invisible hasta que la fecha llega.

- **Qué me haría subirlo**: sumar gente al equipo (la regla escala con personas), o descubrir que me
  bloqueo seguido esperando algo externo que no controlo.
- **La señal de que quedó demasiado alto**: **si nunca lo alcanzo**. Un límite que nunca frena nada no
  está limitando: es decorativo. Y si lo subiera a diez, con una sola persona, dejaría de existir
  como límite — sería el mismo tablero sin límite, con un número al lado.

### Diagnóstico de la historia mal escrita

El issue [#15](https://github.com/marcosdon28/IngeSoft3-2319274/issues/15) —creado a propósito para
diagnosticarlo, y cerrado— dice:

> *Como desarrollador quiero crear la tabla usuarios para guardar los datos.*

**Por qué está mal escrita**: tiene la **forma** de historia de usuario pero es una **tarea técnica
disfrazada**. Una historia describe **valor para alguien**, y acá el «para guardar los datos» no es
un beneficio: es la definición de lo que hace una tabla. El «como desarrollador» tampoco ayuda —el
desarrollador es quien la implementa, no quien recibe el valor—. Y sobre todo: **no tiene criterios
de aceptación verificables**. ¿Cuándo está terminada? ¿Con qué columnas? ¿Qué se puede hacer una vez
que existe que antes no se podía? Nada de eso se puede comprobar. Es también una historia
**horizontal**: entrega una capa técnica, no una rebanada de funcionalidad que alguien pueda usar.

**Cómo la reescribiría**: partiendo de quién se beneficia y de qué puede hacer después.

> *Como encargado de depósito quiero registrarme con usuario y contraseña para que cada movimiento de
> stock quede asociado a quien lo hizo.*
>
> **Criterios de aceptación**
> - [ ] Un usuario nuevo se registra con email y contraseña y queda habilitado para operar
> - [ ] El email es único: registrarse con uno ya usado devuelve un error explicando por qué
> - [ ] Cada movimiento registrado guarda qué usuario lo hizo, y se ve en el historial
> - [ ] Un usuario sin sesión iniciada no puede registrar movimientos

La tabla `usuarios` **sigue haciendo falta** — pero pasa a ser una **tarea** de esa historia, que es
su lugar. La diferencia no es de redacción: es de **nivel**. La historia dice qué valor se entrega;
la tarea, qué hay que construir para entregarlo.

### Otras decisiones del práctico

| Decisión | Por qué |
|---|---|
| **El bug va al costado, no colgando de la historia** | La jerarquía cuenta **lo que se planificó construir**: la épica es el objetivo, las historias el valor, las tareas los pasos. Un bug es un defecto de algo **ya construido** — no era parte del plan. Y colgarlo de la historia que lo originó tiene un efecto feo: esa historia ya está cerrada, y su barra de progreso pasaría a mentir. *(Matiz que sé que existe: hay equipos que sí los cuelgan, no para planificar sino para **medir** cuántos defectos se les escapan por sprint; y en Azure Boards un Bug puede ser hijo de una Feature. O sea que «al costado» es una convención de trabajo, no una regla de la herramienta.)* |
| **El bug es real, no el del video** | El enunciado permite usar el del video, pero dice que uno propio es mejor. El nuestro es reproducible en vivo y está diagnosticado hasta la línea de código: `frontend/src/App.jsx`, donde `recargar()` corre una sola vez al montar y el `catch` no reintenta. Un bug prestado no se puede reproducir delante de nadie |
| **Sub-issues y no task-lists** | Las task-lists (`- [ ] #12` en el cuerpo) se ven parecidas pero **no crean la relación padre-hijo navegable**: no se puede subir de la tarea a su historia y de ahí a la épica. El enunciado pide navegable, así que van sub-issues |
| **La épica sin criterios de aceptación** | No se verifica por sí misma: se da por cerrada cuando sus historias lo están. Los criterios van donde algo se puede comprobar, que es la historia |
| **`Closes #12` en la descripción del PR, no en el mensaje del commit** | Por mensaje de commit el issue **igual se cierra**, pero **no queda enlazado al PR** — y ese enlace es justo lo que se mira al corregir y lo que permite navegar de la tarea al código |
| **El número que cierra es el de la TAREA, no el de la historia** | Un PR implementa una tarea concreta. Si cerrara la historia #11, la estaría dando por terminada con la mitad del trabajo sin hacer: la tarea #13 sigue abierta. La trazabilidad quedaría mintiendo |
| **Los items se agregaron al Project por comando** | `gh project create` no configura el *auto-add* (por eso el proyecto nace con 6 workflows y no con 7). En vez de depender de esa automatización, los agregué explícitamente con `gh project item-add`: queda reproducible en un comando y no depende de que un workflow esté encendido |

### Problemas encontrados y cómo los resolví

- **`gh` no puede crear campos de tipo *Iteration*, pero la API GraphQL sí.** El CLI sólo acepta
  `TEXT`, `NUMBER`, `DATE` y `SINGLE_SELECT` en `gh project field-create`, así que asumí que el campo
  Sprint había que crearlo a mano. Probé igual la mutación `createProjectV2Field` con
  `dataType: ITERATION` y **funcionó**. Lección: que el CLI no exponga algo no significa que la API no
  lo soporte — vale la pena mirar el esquema antes de resignarse a la interfaz web.

- **…pero el campo nace sin configurar, y eso sí es sólo web.** La mutación crea el campo con
  `duration: 0` y **cero iteraciones**: no existe mutación pública para definir la duración ni generar
  las iteraciones. Esa parte —y con ella la asignación del sprint, la vista de tablero y el límite de
  trabajo en progreso— se hace desde la interfaz.

- **La interfaz de Projects v2 no se deja automatizar.** Intenté configurar la iteración con
  Playwright y no fue viable: es una aplicación React propia donde los controles no exponen roles
  accesibles estándar (el botón *New view* no es un `button` con nombre accesible; el selector de
  fechas usa `div`s con `aria-label` dinámicos del tipo `"Martes, September 1 (Inside selected
  range)"`, que cambian según el estado de la selección). Después de varios intentos frené y lo hice
  a mano: automatizar algo que tarda treinta segundos por interfaz no se justifica, y forzar
  selectores frágiles hubiera dejado un procedimiento que se rompe con el próximo rediseño.

- **El scope `project` no venía en el token.** `gh project list` fallaba con
  `your authentication token is missing required scopes [read:project]`. Se resuelve con
  `gh auth refresh -h github.com -s project`, que abre un device flow — el mismo mecanismo que hizo
  falta en el TP2 para `write:packages`.

- **Los Projects de usuario nacen privados.** Y el entregable de este TP **es la URL**: si se entrega
  privada, quien la abre ve un 404 — ni siquiera «no tenés permiso», sino «no existe». Se cambia con
  `gh project edit 2 --owner "@me" --visibility PUBLIC`, que además es **idempotente**: pedirle
  `PUBLIC` a un proyecto que ya lo es no da error. El control que hice antes de dar por cerrado el
  práctico fue abrir la URL en una ventana de incógnito.

### Declaración de uso de IA — TP3

| Qué fue asistido | Cómo lo verifiqué |
|---|---|
| Creación de labels, issues, jerarquía y Project por CLI | Verifiqué la jerarquía **consultándola de vuelta por GraphQL** (`subIssues`), no mirando la pantalla: épica → historia → dos tareas, con el bug fuera del árbol |
| La redacción de la historia y sus criterios de aceptación | Los revisé uno por uno preguntándome **cómo se comprueba cada uno**. El que no pasaba esa prueba, no entraba: por eso en el issue hay una tabla que dice, para cada criterio, qué hay que mirar para saber si está cumplido |
| El diagnóstico de la historia mal escrita | Es mío. Creé el issue a propósito, lo leí, y la reescritura sale de identificar qué faltaba: el beneficiario real, el valor, y criterios verificables |
| El PR de trazabilidad | Verifiqué que **el PR hace lo que el issue dice** (la tarea era escribir el workflow, y el PR crea exactamente ese archivo), y después comprobé por API que `#12` quedó cerrada, enlazada al PR #16, y que `#11`, `#13` y `#10` siguen **abiertas** — que es el estado correcto |
| El bug | Lo encontré leyendo mi propio código y lo reproduje: `docker compose down -v && up -d` y abrir la app enseguida. El issue cita la línea exacta y explica por qué pasa |

Lo que **no** delegué: la duración del sprint, el número del límite de trabajo en progreso, el
diagnóstico de la historia mal escrita, y la decisión de usar un bug propio en vez del de la guía.

---

## TP4 — CI: Pipelines as Code

### La estructura del pipeline: por qué esos jobs y por qué en paralelo

Dos jobs, `build-backend` y `build-frontend`, uno por cada imagen que tiene la app.

**Por qué separados**: son **artefactos independientes**. Ninguno necesita el resultado del otro, no
comparten código ni dependencias, y si uno falla quiero saber cuál sin leer un log mezclado. Un solo
job que construyera las dos imágenes me daría un único check en rojo sin decir cuál se rompió.

**Por qué en paralelo**: es el default de GitHub Actions —los jobs corren simultáneamente salvo que
se declare `needs:`— y acá no hay ninguna dependencia que justifique serializarlos. Medido sobre la
primera corrida:

| | Tiempo |
|---|---|
| `build-backend` | 1 m 53 s |
| `build-frontend` | 47 s |
| **Suma (si fueran secuenciales)** | 2 m 40 s |
| **Reloj real (en paralelo)** | **1 m 53 s** |

Los dos arrancaron en el mismo instante (`12:45:20Z`), así que el tiempo total es el del **más
lento**, no la suma. Y el ahorro crece con cada job que se sume: en el TP5 entran los tests.

**Lo que los jobs NO comparten**: filesystem. Cada uno corre en un runner limpio y distinto — son
dos máquinas. Si el TP7 necesitara que un job use algo que produjo otro, tendría que viajar como
artefacto o declararse `needs:` para el orden. Hoy no hace falta.

### Por qué el pipeline construye con mi Dockerfile en vez de compilar por su cuenta

Porque si el pipeline compilara aparte —con `pip install` y `npm run build` escritos en el YAML—
habría **dos definiciones de build**: la del Dockerfile y la del workflow. Tarde o temprano divergen,
y el día que pase estaría **verificando una compilación distinta de la que después se despliega**. El
pipeline daría verde sobre algo que no es lo que llega a producción.

Usando el Dockerfile del TP2 hay **una sola** definición: la misma que corre en mi máquina, la que
verifica el pipeline y la que se va a publicar en el TP7.

Un efecto lateral que se nota al leer el YAML: **no hay una sola línea de Python ni de Node ahí
adentro**. El workflow no sabe cómo se construye mi app — eso lo sabe el Dockerfile. Por eso este
mismo archivo le serviría a cualquier compañero, sea cual sea su stack.

### Qué cachea el pipeline, y qué pasa si el cache desaparece

Se cachean las **capas de la imagen**, en el cache de GitHub Actions (`type=gha`).

**Qué se reutiliza y qué no** — medido en la segunda corrida del backend, 7 capas `CACHED`:

| Capa | ¿Se reutiliza? | Por qué |
|---|---|---|
| La imagen base (`python:3.12`, `python:3.12-slim`) | ✅ sí | No cambia nunca |
| `COPY requirements.txt` + `RUN pip install` | ✅ sí | Sólo se rehace si cambia `requirements.txt` |
| `COPY app ./app` | ❌ no, si toqué código | Es lo que cambia en casi todos los PRs |
| Las capas posteriores a una que cambió | ❌ no | Docker invalida esa capa **y todas las siguientes** |

Ese orden no es casual: es la razón por la que el Dockerfile del TP2 copia las dependencias **antes**
que el código. Al revés, cada cambio de una línea reinstalaría todo.

**El resultado, medido**: `build-backend` pasó de **1 m 53 s a 21 s** entre la primera y la segunda
corrida. Cinco veces más rápido.

**Si el cache desaparece, no pasa nada grave: el pipeline funciona igual, sólo más lento.** El cache
es una **optimización**, no una dependencia — vuelve a construir todo desde cero y a repoblarlo. Es
importante que sea así: un pipeline que *necesita* el cache para funcionar está roto, porque el cache
se desaloja solo (GitHub lo purga por antigüedad y por límite de tamaño).

**El `scope` no es opcional cuando hay dos jobs.** Sin él los dos usarían el mismo estante por
default y **se pisarían**: el último en terminar deja su cache y borra el del otro. El síntoma es
desconcertante porque parece azar — un job muestra `CACHED` y el otro no, y cuál cambia en cada
corrida. Con `scope=backend` y `scope=frontend`, cada uno reutiliza siempre lo suyo.

### El gate: qué exige hoy mi `main`

Dos condiciones, y hacen falta las dos:

1. **Que el cambio entre por Pull Request** — del TP1, con `enforce_admins` para que me alcance
   también a mí.
2. **Que los dos checks estén en verde** — `build-backend` y `build-frontend` como
   *required status checks*.

> La puerta sin verificación no alcanza, y la verificación sin puerta tampoco.

**`strict: true`** agrega una tercera exigencia: que la rama esté **actualizada con `main`** antes de
mergear. Sin eso, un PR podría entrar en verde habiendo sido verificado contra un `main` que ya no
existe — y romper `main` sin que ningún check lo haya visto venir. Lo demostré con dos PRs abiertos a
la vez: al mergear uno, el otro quedó `BEHIND` con sus **dos checks en verde** y el botón de merge
igualmente deshabilitado, pidiendo *Update branch*.

Un detalle de vocabulario que confunde y conviene tener claro: al romper el build a propósito, la API
devolvía `mergeable: MERGEABLE` y `mergeStateStatus: BLOCKED`. **No es contradictorio**:
`mergeable` habla de **conflictos de contenido** (no había ninguno) y `mergeStateStatus` habla de
**política** (el gate). Son dos preguntas distintas.

### La demostración del gate

Secuencia completa, en el PR #20:

1. **Rojo**: un `import` a un archivo inexistente en `frontend/src/App.jsx` → `build-frontend`
   falla a los 30 s, `build-backend` sigue en verde.
2. **Bloqueado**: los dos checks marcados *Required*, botón *Squash and merge* deshabilitado.
   `gh pr merge` lo confirma desde la consola:
   `the base branch policy prohibits the merge`.
3. **Fix**: un commit que saca el import. El pipeline **re-corre solo**, sin tocar nada.
4. **Verde** → `mergeStateStatus: CLEAN` → merge.

**Por qué rompí el frontend y no el backend.** Es una diferencia de stack que vale la pena entender:
el frontend **se empaqueta** —Vite resuelve los imports al hacer el bundle—, así que un import roto
lo tumba durante `npm run build`. El backend es **Python: no compila ni se empaqueta**, y su
Dockerfile **nunca ejecuta mi código** — sólo instala dependencias. Escribir `import estonoexiste` en
un `.py` daría **verde igual**. Para romper el backend habría que romper la **dependencia**: un
paquete inexistente en `requirements.txt`. Desde el TP5, con los tests adentro del pipeline, el
código del backend sí va a poder romperlo.

### Problemas encontrados y cómo los resolví

- **Estaba usando versiones viejas de las actions.** Empecé con `actions/checkout@v4`,
  `docker/setup-buildx-action@v3` y `docker/build-push-action@v6` — dos o tres majors por detrás de
  las que usa la guía. Funcionaban, así que el pipeline en verde no me lo iba a avisar nunca. Lo
  verifiqué consultando las releases de cada repositorio y las subí a `v6`, `v4` y `v7` en un PR
  aparte, que **pasó por su propio gate**. Las tres van con major explícito y no con `@main`: sin
  versión fijada, el pipeline cambiaría solo el día que sus autores publiquen algo.

- **Buscar `CACHED` en los logs por la API no funciona.** `gh api .../actions/jobs/<id>/logs`
  devuelve una redirección a un zip, así que mi `grep` daba cero y parecía que el cache no estaba
  actuando — cuando los tiempos decían lo contrario. El comando correcto es
  `gh run view <run> --log`, que sí devuelve texto. Buena lección sobre confiar en una medición
  antes de entender qué devuelve el comando.

- **La primera corrida es más lenta que una sin cache, y está bien.** Además de construir tiene que
  **exportar** las capas: el paso de export tardó 66,6 s. El cache se paga una vez y se cobra en
  todas las corridas siguientes.

- **Un detalle del contexto en los Pull Requests.** En un PR, `GITHUB_REF_NAME` no vale el nombre de
  la rama sino `<numero>/merge`, porque GitHub construye una mezcla de la rama con `main` y verifica
  **eso**. Para loguear la rama real hay que usar `github.head_ref`. No es cosmético: aclara que lo
  que el pipeline verifica no es tu rama, es **el resultado propuesto del merge**.

### Declaración de uso de IA — TP4

| Qué fue asistido | Cómo lo verifiqué |
|---|---|
| El `ci.yml` | Lo leí línea por línea antes de commitearlo, y sobre todo **lo vi funcionar**: los dos jobs arrancando en el mismo instante, el cache reutilizando 7 capas, y el gate frenando un merge de verdad |
| La configuración del gate por API | El `PUT` **reescribe la protección entera**, así que re-declaré lo del TP1 en el mismo JSON y después leí la protección de vuelta para confirmar que seguían los `approvals: 0` y `enforce_admins: true` |
| Las mediciones de tiempo y cache | Salen de `gh api .../jobs` y `gh run view --log`, no de estimaciones |
| Redacción de esta sección y del informe | Revisados contra lo que efectivamente pasó |

**Un error que cometí y corregí, porque viene al caso.** Al armar la evidencia del cache, la primera
versión de la imagen tenía líneas de log de la primera corrida que **no había leído**: estaban
escritas a mano para ilustrar. Lo detecté al releerla, la descarté entera y la rehíce extrayendo cada
línea de `gh run view --log` de las dos corridas reales. Una evidencia inventada es peor que no tener
evidencia: la segunda se nota, la primera no. Lo dejo declarado porque es exactamente el tipo de cosa
que el reglamento pide verificar de lo que produce la IA.

Lo que **no** delegué: la estructura del pipeline, la decisión de construir con el Dockerfile en vez
de compilar aparte, qué romper para demostrar el gate, y la interpretación de las mediciones.

---

## TP5 — Testing en el pipeline: unit tests, coverage y el umbral que frena un merge

> 📎 Desde este práctico no hay `evidencias.md` ni capturas: cada afirmación lleva al lado la URL de
> la corrida o del Pull Request que la prueba.
>
> | Lo que prueba | Enlace |
> |---|---|
> | La suite, la cobertura y el umbral (PR mergeado) | <https://github.com/marcosdon28/IngeSoft3-2319274/pull/24> |
> | Resumen de cobertura en el Summary + reportes descargables (`coverage-backend`, `coverage-frontend`) | <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39624071037> |
> | La corrida **roja por umbral**, con el número en el log | <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39624730420> |
> | La secuencia rojo → tests → verde → merge | <https://github.com/marcosdon28/IngeSoft3-2319274/pull/25> |
> | El freno vigente, **abierto y en rojo** | <https://github.com/marcosdon28/IngeSoft3-2319274/pull/26> |

### Qué lógica elegí testear y por qué ésa

Las **7 reglas de negocio** del TP2, porque son donde un bug duele: stock negativo (regla 1), dos
productos con el mismo SKU (2), una categoría borrada con productos adentro (3), un descuento mal
calculado en un remito (5). Un bug en un componente de React se ve en la pantalla y se arregla; un
bug en el cálculo del descuento sale en una venta y nadie lo nota hasta que cierran la caja.

| Lado | Qué se prueba | Tests | Dónde |
|---|---|---|---|
| Backend | Regla 5, `calcular_descuento` / `calcular_total` (función pura) | 7 | `tests/test_descuento.py` |
| Backend | Regla 6, `Producto.bajo_stock` (propiedad derivada) | 4 | `tests/test_bajo_stock.py` |
| Backend | Regla 4, validación de borde con Pydantic (**casos de error**) | 4 | `tests/test_schemas.py` |
| Backend | Reglas 1 y 7, `movimiento_service.registrar` (**con mock**) | 5 | `tests/test_movimiento_service.py` |
| Backend | Regla 2, `producto_service` + filtro de bajo stock + baja | 6 | `tests/test_producto_service.py` |
| Backend | Regla 3, `categoria_service` + nombre único | 5 | `tests/test_categoria_service.py` |
| Frontend | Reglas 1, 4, 5, 6 y 7 en la vista, `lib/reglas.js` | 21 | `src/lib/reglas.test.js` |
| Frontend | El cliente de la API, `api.js` (**con mock**, casos de error) | 6 | `src/api.test.js` |

**31 tests de backend sobre 7 reglas y 27 de frontend**, todos con la forma AAA (Arrange / Act /
Assert) y con nombres que dicen el comportamiento, no el método: `test_una_salida_mayor_al_stock_
es_rechazada_y_no_toca_la_base` es el diagnóstico cuando falle a las 3 AM. Los parametrizados
cuentan como un método cada uno (`@pytest.mark.parametrize` / `it.each`); el mínimo de ocho se
cumple con métodos, no con datos.

**El criterio para saber si un test vale** —si invierto la regla, algo se pone rojo— lo probé sobre
los bordes a propósito: hay un test con **exactamente** el umbral (10 unidades → descuento; 6 con
mínimo 6 → bajo stock; sacar 10 de 10 → válido). Si alguien cambia `>=` por `>` en
`calcular_descuento`, cae `test_descuento_por_cantidad_aplica_desde_el_umbral_inclusive[10-10.0]`;
si cambia `<=` por `<` en `bajo_stock`, cae `[6-6-True]`. Un test sólo con 1 y 100 unidades dejaría
pasar ese cambio.

### Las tres técnicas, de los dos lados

| Técnica | Backend (pytest) | Frontend (vitest) |
|---|---|---|
| **Parametrizado** | `@pytest.mark.parametrize` en descuento, bajo stock | `it.each` en `calcularTotal`, `estaBajoStock`, cantidades inválidas |
| **Caso de error** | `MovimientoCrear(cantidad=0)` → `ValidationError` señalando `cantidad`; `ReglaDeNegocioError` con el mensaje que dice *cuánto hay y cuánto se pidió* | `motivoMovimientoInvalido` devuelve el motivo exacto; un `400` de la API se convierte en `Error` con el `detail` del backend |
| **Mock** | `Mock(spec=Session)` de SQLAlchemy | `vi.fn()` como reemplazo del `fetch` |

**El mock del backend.** La dependencia externa de los services es la base de datos, y **ya entraba
desde afuera**: desde el TP2 cada service recibe `db: Session` por parámetro (lo inyecta FastAPI con
`Depends(get_db)`). No hizo falta el refactor del «paso cero» de la guía. El doble es
`unittest.mock.Mock(spec=Session)`: `spec` hace que sólo acepte los métodos que la `Session` real
tiene, así un typo en el service rompe el test en vez de pasar en silencio. En cada test el doble
actúa de las dos formas que distingue la guía:

- como **stub**, cuando `db.get.return_value = producto` le dice qué contestar;
- como **mock**, cuando el assert mira **la interacción**: `db.add.assert_called_once()` y
  `db.commit.assert_called_once()` en el movimiento válido —el equivalente del
  `Verify(…, Times.Once)` de Moq—, y `db.add.assert_not_called()` cuando una regla frenó. Si mañana
  alguien duplica el `add` o commitea antes de validar, el test se pone rojo sin tocar PostgreSQL.

**El mock del frontend, y el refactor que lo hizo posible.** `api.js` tenía el mismo problema del
`new NotificadorEmail()` de la guía con otra cara: `pedir()` llamaba a `fetch` global adentro, así
que no había por dónde meter un impostor sin levantar la API. El cambio: `crearApi(fetchImpl)`
recibe la función que hace el pedido, y `export const api = crearApi()` le pasa el `fetch` real del
navegador —así ninguna pantalla cambió—. El test le pasa `vi.fn().mockResolvedValue(…)`. El que
vale como mock es `listar sólo bajo stock le pide a la API la ruta con el filtro`: no mira lo que
devolvió, mira que se haya llamado **una vez** y con `/api/productos?bajo_stock=true`. Lo que esto
**no** prueba: que el backend siga contestando esa ruta — eso es end-to-end, y es el TP7.

### El umbral: el número, la métrica y por qué

| Lado | Medido hoy (línea) | Medido hoy (**rama**) | Umbral | Sobre qué métrica |
|---|---|---|---|---|
| Backend | 92,1 % | 82,4 % | **85 %** | la combinada de coverage.py (sentencias + ramas), que hoy da 90,7 % |
| Frontend | 100 % | 97,2 % | **90 % líneas y 85 % ramas** | las dos, por separado (`thresholds`) |

**Por qué 85 en el backend.** La lógica mide 90,7 y quiero que el umbral me frene si baja, no que
sea inalcanzable: cinco puntos de margen absorben un método chico sin tests, no una clase entera.
`--cov-fail-under` de coverage.py evalúa **una sola métrica combinada** (sentencias ejecutadas más
ramas recorridas, sobre el total de las dos) — no línea sola, que es la menos honesta—, así que
el umbral mira las ramas aunque el número sea uno. Para subirlo a 95 tendría que testear
`actualizar` con cada campo del PATCH y `listar` de movimientos (que arma un dict) — código sin
reglas: no lo vale.

**Por qué 90/85 en el frontend.** Está en 100/97 porque la lógica de la vista es chica y pura. Lo
puse diez puntos abajo de líneas y doce de ramas a propósito: un umbral al 100 se apaga el primer
día que alguien agregue una función —la regla «lo que tocás, lo dejás limpio» funciona si el
número es defendible, no si es un trofeo—. Y va sobre **las dos métricas** porque en vitest 2 una
función que ningún test llama baja las líneas pero casi no mueve las ramas: con un umbral sólo de
ramas, la demostración de §3.5 no se habría puesto roja.

### Qué dejé afuera de la cuenta, y por qué cada cosa

**Backend** (`backend/.coveragerc`, `omit`):

| Archivo | Por qué queda afuera |
|---|---|
| `app/main.py` | El arranque: crea la app, incluye los routers, crea el schema. Si está mal, la app no levanta y me entero sin test |
| `app/database.py` | Infraestructura: el engine y la fábrica de sesiones. No hay reglas |
| `app/config.py` | Lectura del entorno (`os.getenv`). Testearlo es testear `os` |
| `app/routers/*` | Pegamento HTTP: traducen `ReglaDeNegocioError` → 400 y `NoEncontradoError` → 404. No hay reglas de negocio ahí — a propósito, desde el TP2 — y se verifican end-to-end en el TP7 |

**Lo que NO excluí, aunque la guía lo sugiere como «clases de datos»**: `app/models/` y
`app/schemas/`. En esta app tienen reglas: `Producto.bajo_stock` es la regla 6 y los `Field(gt=0)` /
`Field(ge=0)` son la regla 4. Excluirlos sería esconder lógica, que es la trampa que el §2.4 no
acepta. (Y la trampa inversa no aplica: los routers no tienen ninguna regla adentro, así que
sacarlos **sí** cambia el número, y mucho: midiendo todo, 67 %; midiendo lo que tiene reglas,
90,7 %. Esa diferencia es exactamente el caso del §2.4: los routers y el arranque no tienen tests
ni deberían tenerlos, y arrastran el número al piso. Lo que distingue «medir lo que importa» de
«esconder lo que no testeé» es esta lista: lo excluido no tiene reglas.)

**Frontend** (`vite.config.js`, `include: ['src/lib/**', 'src/api.js']`): entra la lógica pura y el
cliente de la API. Quedan afuera los componentes de React (`pages/*.jsx`, `App.jsx`), que son
pegamento de UI y se verifican con un navegador real en el TP7, y `main.jsx`, el arranque. Es
`include` y no `exclude` por cómo mide vitest: con `include`, todo archivo de esa carpeta entra
aunque nadie lo pruebe, así una función nueva sin tests **baja** el número en vez de desaparecer.

### Por qué coverage alto no garantiza calidad — con mi ejemplo

Este test deja `calcular_total` al 100 % y no verifica nada:

```python
def test_cobertura_sin_verdad():
    calcular_total(1800, 10, 10)   # se ejecutó entera… y no hay ningún assert
```

Y uno un poco más tramposo, que **sí** tiene assert y tampoco verifica la regla:

```python
def test_descuento_devuelve_un_numero():
    assert isinstance(calcular_descuento(10), float)   # 0.0 también es float: pasa con la regla rota
```

Coverage mide **ejecución, no verificación**: dice qué código ningún test recorrió (eso es
información confiable), no que el código recorrido haga lo que debe. Lo que custodia que el
descuento sea 10 y no 15 son los asserts del test parametrizado, y lo que custodia que el umbral sea
inclusivo es el dato `(10, 10.0)` de esa tabla. Si el día de mañana alguien pregunta «¿el 90 % de tu
código está verificado?», la respuesta honesta es: el 90 % se **ejecuta** bajo tests; cuánto se
**verifica** lo contestaría un mutante (cambiar `>=` por `>` y ver qué se pone rojo), y eso lo hice
a mano sobre los dos bordes.

### El ejercicio de la rama sin cubrir

Abrí el reporte HTML del backend (`htmlcov/`, artefacto `coverage-backend`) y elegí una rama
**parcial** (naranja), no una función sin tests:

1. **Qué línea es**: `backend/app/services/producto_service.py`, línea 73,
   `if datos.precio is not None:` dentro de `actualizar`. El reporte marca `73->75`: sólo se
   recorrió el camino **falso** (ningún test manda `precio` en el PATCH). Lo mismo pasa en la 79
   con `stock_minimo`.
2. **Qué entrada la recorrería**: `ProductoActualizar(precio=1950)` sobre un producto existente.
3. **Qué decidí**: **no agregarlo**. El camino verdadero es una asignación (`producto.precio =
   datos.precio`) sin ninguna regla; testearlo sería testear que una propiedad guarda un valor. Lo
   que sí importa de `actualizar` —que un PATCH parcial no pise los campos que no vinieron— ya está
   probado en `test_dar_de_baja_un_producto_lo_deja_inactivo_sin_tocar_lo_demas`. Las ramas
   parciales que quedan son el motivo de que el backend mida 82,4 % de rama y no más, y prefiero
   ese número honesto a dos tests que no custodian nada.

Del lado del front el reporte marca la línea 19 de `reglas.js`, `Number(precio) || 0`: el `|| 0` sólo
se recorre si el precio no es numérico, y el precio siempre llega de la API como número. Tampoco lo
agregué, por la misma razón.

### Las herramientas de mi stack (la tabla «Tu stack, de un vistazo»)

| Lo que hay que lograr | Backend (Python / FastAPI) | Frontend (JS / Vite) |
|---|---|---|
| Dónde viven los tests | `backend/tests/` | al lado del código, `*.test.js` |
| Un test parametrizado | `@pytest.mark.parametrize` | `it.each` |
| La dependencia entra desde afuera | parámetro `db` del service (ya estaba) | parámetro `fetchImpl` de `crearApi` (refactor de este TP) |
| Fabricar el doble | `unittest.mock.Mock(spec=Session)` | `vi.fn()` |
| Medir la cobertura | `pytest --cov --cov-branch` (coverage.py vía pytest-cov) | `vitest run --coverage` (provider v8) |
| **Un umbral que ROMPE el build** | `--cov-fail-under=85` | `coverage.thresholds: { lines: 90, branches: 85 }` |
| **Qué ENTRA en la cuenta** | `omit` en `.coveragerc` | `include` en `vite.config.js` |
| Reporte legible | `--cov-report=html` + `xml` para el Summary | reporter `html` + `json-summary` para el Summary |
| Que las herramientas entren a la etapa de tests | la etapa `test` instala `requirements-dev.txt` (pytest, pytest-cov) sobre el venv de `build` | `npm ci` sin `--omit=dev`: la etapa `test` hereda las devDependencies de `build` |

Las dos etapas de tests viven **en los Dockerfiles** (`FROM build AS test`), entre `build` y la
imagen final, y el pipeline sólo las construye y las corre: sigue sin saber cómo se testea mi app,
igual que en el TP4 no sabía cómo se compila. Una receta, no dos. Las imágenes finales no se llevan
ni pytest ni vitest: el backend copia sólo el venv y `app/`, el front sólo el `dist/`.

### El gate: qué cambió respecto del TP4

Nada en la protección de `main`: `build-backend` y `build-frontend` siguen siendo los dos required
checks (verificado con `gh api …/branches/main/protection`). Lo que cambió es **qué puede ponerlos
en rojo**. Hasta el TP4, sólo que la imagen no se construyera; el backend, en Python, ni siquiera
podía fallar por el código. Desde este PR, un `docker run` de la etapa de tests devuelve el código de
salida de pytest / vitest, y ésos fallan por un test en rojo **o por cobertura bajo el umbral**: la
calidad entra en el mismo check que ya frenaba merges. Tres guardianes: el PR obligatorio (TP1), el
build (TP4) y el umbral (TP5). Lo que **ninguno** de los automáticos ve: que la regla esté bien
entendida —si leí mal el requisito, el test lo congela mal y queda verde para siempre—.

### La demostración: el umbral frenando un merge

Son **dos Pull Requests**, a propósito: el primero cuenta la historia completa y el segundo la prueba
en vivo.

**PR #25 — la secuencia rojo → tests → verde → merge**
(<https://github.com/marcosdon28/IngeSoft3-2319274/pull/25>):

1. **Código nuevo sin tests, que compila perfecto**: `prioridadDeReposicion` y `ordenarPorPrioridad`
   en `frontend/src/lib/reglas.js` (y el tablero las usa para ordenar los productos por reponer).
   `npm run build` en verde, **27 tests en verde**.
2. **Rojo por cobertura, no por compilación**:
   <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39624730420>. `build-backend`
   verde; `build-frontend` **rojo** con el motivo en el log, con todas las letras:
   ```
   Tests  27 passed (27)
   All files   |   86.06 |    97.22 |   58.82 |   86.06 |
   ERROR: Coverage for lines (86.06%) does not meet global threshold (90%)
   ```
   Frenó por **líneas**: 86,06 % contra 90. Las ramas quedaron en 97,22 %, iguales que antes,
   porque en **vitest 2.1.9** una función que ningún test llama no suma ramas sin cubrir — es
   justo lo que la guía describe para vitest 3, y la razón por la que el umbral va sobre las dos
   métricas: con uno sólo de ramas, esto no se habría puesto rojo. El PR quedó `mergeStateStatus:
   BLOCKED` con `mergeable: MERGEABLE` (sin conflictos: la política es lo que bloquea), y
   `gh pr merge` lo rechazó: *the base branch policy prohibits the merge*.
3. **Los tests que faltaban**: `frontend/src/lib/prioridad.test.js`, **diez**, y no los inventé yo:
   uno por cada camino que el código declara — sin producto, sin stock, por encima del mínimo,
   urgente, pronto (dos entradas distintas), puede esperar, el borde de «exactamente la mitad del
   mínimo», el ordenamiento con desempate por nombre y que no mute la lista.
4. **Verde y merge**: <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39625075951>
   (100 % líneas, 98,18 % ramas) → squash a `main`.

Una honestidad que vale la pena dejar escrita: la primera versión de la función quedó **0,74 puntos
arriba** del umbral (90,74 %) y el gate no se habría puesto rojo. La guía lo avisa —«hacé la cuenta
con tu reporte antes de subir»—: con 54 líneas medidas, 10 nuevas sin tests no alcanzan. El
ordenamiento (`ordenarPorPrioridad`), que de todas formas el tablero necesitaba, llevó el número a
86,06 %. Lo corregí antes de que corriera el pipeline (un `--amend`), así que el PR muestra una sola
corrida roja.

**PR #26 — el freno vigente, abierto y en rojo hasta la defensa**
(<https://github.com/marcosdon28/IngeSoft3-2319274/pull/26>): `sugerir_reposicion` en
`backend/app/services/producto_service.py`, sin tests. Corrida:
<https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39625414893> — `build-frontend` verde,
`build-backend` rojo con `FAIL Required test coverage of 85% not reached. Total coverage: 82.38%`
y los **31 tests en verde**. Este PR **no se arregla ni se mergea**: cualquiera que lo abra ve los
checks obligatorios, cuál está en rojo y por qué, sin depender de una captura mía. Acá frenó el
**otro** lado y la otra métrica: el backend, por la combinada de coverage.py (82,4 contra 85).

**Qué clase de error deja pasar igual este freno.** Un test que ejecuta la función nueva sin
afirmar nada (`prioridadDeReposicion(producto)` suelto) hubiera dejado el PR #25 en verde con el
mismo código: el gate mide ejecución. Y ninguno de los tres guardianes puede saber si «menos de la
mitad del mínimo» era lo que el negocio quería, o si tenía que ser «menos de un tercio».

### Problemas encontrados y cómo los resolví

- **`tests/` estaba en `backend/.dockerignore` desde el TP2.** Era correcto para la imagen final,
  pero la etapa `test` hace `COPY tests ./tests` y con esa línea el contexto no los incluye: la
  guía lo avisa textual («si ahí excluiste la carpeta de tests, no entra por más que la pidas»). Lo
  saqué; la imagen final sigue sin llevarlos porque su `COPY` es sólo de `app/`.

- **`--cov-fail-under` no mira «líneas» ni «ramas»: mira la métrica combinada.** Con
  `--cov-branch`, coverage.py informa línea y rama por separado en el XML, pero el umbral se evalúa
  sobre el porcentaje combinado (la columna `Cover`). Lo verifiqué pidiendo 99: `FAIL Required test
  coverage of 99% not reached. Total coverage: 90.68%`. Por eso el umbral del backend es **un**
  número y está declarado como «combinada», y el Summary muestra las dos métricas al lado.

- **El major de `@vitest/coverage-v8` tiene que ser el de vitest.** El proyecto tiene vitest 2.1.x,
  así que fue `@vitest/coverage-v8@2`, no la última a secas (que es la 4). Con majors distintos
  vitest arranca y falla de forma críptica. Lo comprobé con `npm ls vitest @vitest/coverage-v8`.

- **`defineConfig` de `vite` no conoce la clave `test`.** Para que `vite.config.js` acepte la
  configuración de cobertura el import pasa a `vitest/config`, que extiende al de Vite: Vite sigue
  leyendo el mismo archivo.

- **La Mac tiene Python 3.9 y la app corre con 3.12.** No instalé nada local: la suite se corrió
  **sólo adentro del contenedor** (`docker build --target test` + `docker run`), que es exactamente
  lo que corre el pipeline. Una sola receta de tests, como una sola receta de build.

- **Un assert que depende del texto de Pydantic.** `test_un_movimiento_con_cantidad_cero_es_
  rechazado` comprueba que el mensaje contenga `greater than 0`: ese texto lo escribe Pydantic, no
  yo. Lo dejé porque el mensaje **es** comportamiento (le llega al usuario), pero queda anotado que
  un cambio de versión de Pydantic puede romperlo sin que la regla haya cambiado.

### Declaración de uso de IA — TP5

Usé **Claude Code (Claude Fable 5.1)** como en los prácticos anteriores.

| Qué fue asistido | Cómo lo verifiqué |
|---|---|
| La escritura de los tests (backend y frontend) | Leí cada test preguntándome **qué verifica cada assert y qué caso no cubre**: por eso cada archivo prueba una regla, cada test un comportamiento, y los bordes están escritos con el valor exacto del umbral. Los corrí en el contenedor antes de subirlos (31 + 27 en verde) y **los invertí a mano** (`>=` → `>` en el descuento, `<=` → `<` en bajo stock) para ver que el test del borde se pusiera rojo |
| El refactor de `api.js` (`crearApi`) | La app levantada en compose sigue funcionando igual: ninguna pantalla cambió, porque `api` exporta el mismo objeto con el `fetch` real |
| Las etapas `test` de los Dockerfiles y los pasos del `ci.yml` | Los dos frenos **probados** localmente antes de abrir el PR (umbral 99 en el back, ramas 100 en el front: rojo en los dos), y después en el pipeline con la demostración de §3.5. Verifiqué que la imagen final del front siga siendo nginx (`docker inspect` → `nginx -g daemon off`) |
| La elección de qué excluir de la cobertura | Es mía: medí con y sin los routers, y decidí no excluir models ni schemas porque tienen reglas |
| Redacción de esta sección | Revisada contra lo que efectivamente pasó; los problemas listados son los que me pasaron |

Lo que **no** delegué: qué reglas testear, los números del umbral y sobre qué métrica, qué queda
afuera de la cuenta, y la decisión de no agregar el test de la rama sin cubrir.

---

## TP6 — CD: environments, aprobaciones y deployment patterns

### El artefacto: el pipeline entrega lo que verificó (§3.0)

Hasta el TP5 el pipeline **verificaba**: construía, testeaba, medía. Y lo que construía moría con el
runner. Desde el PR [#28](https://github.com/marcosdon28/IngeSoft3-2319274/pull/28) cada job termina
**publicando** su imagen en ghcr, etiquetada con el commit que la produjo:
`ghcr.io/marcosdon28/inventario-backend:sha-<40 caracteres>` y lo mismo para `-frontend`.

**Por qué sólo con la verificación en verde, y qué dejaría de significar el registry si no.** Si se
publicara igual con los tests en rojo, «está en el registry» pasaría a significar «alguien lo
construyó alguna vez», y el deploy del TP7 tendría que volver a preguntarse si lo que baja está
sano. La garantía no es un control nuevo: son **tres eslabones que ya existen**, encadenados:

1. **Nada entra a `main` sin los dos checks en verde** — el gate del TP4 más el umbral del TP5.
2. **Sólo lo que entra a `main` se publica** — `push: ${{ github.event_name == 'push' &&
   github.ref == 'refs/heads/main' }}`. Las dos condiciones y no una: hoy el workflow sólo escucha
   `main` y los PRs, pero el día que alguien agregue otra rama al disparador, un push ahí publicaría
   sin pasar por ningún guardián. La condición vive en el paso que publica, no en el disparador.
3. **Publicar es el ÚLTIMO paso del mismo job que corrió los tests.** No hay ningún `if: tests
   pasaron`: los pasos corren en orden y se cortan al primer error. Si el `docker run` de los tests
   falla, el job muere ahí y el paso de publicar nunca llega a correr. La condición está en el
   orden.

Y lo que la cadena **no** garantiza, dicho con todas las letras: que nadie suba una imagen a mano.
Yo puedo hacer `docker push` desde mi notebook, y nadie me lo impide (lo hice en el TP2). La cadena
garantiza lo que **el pipeline** publica, no lo que físicamente puede entrar. Lo que sí identifica
una imagen más allá de la etiqueta es su **digest** (`sha256:…`), que depende del contenido: una
etiqueta se puede mover; un digest, no.

**Decisiones de este paso:**

| Decisión | Por qué |
|---|---|
| **Reutilizar los packages del TP2** (`inventario-backend` / `inventario-frontend`) en vez de `<repo>-backend` | Ya eran públicos y ya estaban enlazados al repositorio por el `LABEL org.opencontainers.image.source`. `${{ github.repository }}` no servía de todas formas: `IngeSoft3-2319274` tiene mayúsculas y el registry las rechaza (`repository name must be lowercase`), así que el nombre va escrito a mano |
| **`permissions` adentro de cada job**, no arriba del workflow | A nivel del workflow **reemplaza** el default para todos los jobs: le daría `packages: write` a jobs que no publican nada (los de deploy). Por job, sólo el que publica lo tiene: mínimo privilegio. Y `contents: read` no es de más: lo que no se lista queda sin permiso, y sin eso el checkout no puede leer el código |
| **Sin secrets nuevos** para el registry | `GITHUB_TOKEN` es el token de la corrida: vive lo que dura el job, nunca se guarda ni se imprime. Es el caso ideal del TP4 §2.6 |
| **Una sola etiqueta, `sha-<commit>`**; nunca `latest` | `latest` no dice qué hay detrás y se mueve de una imagen a otra. Con el commit en la etiqueta, la pregunta «¿lo que corre es lo que se verificó?» tiene respuesta |

### Problemas encontrados y cómo los resolví

- **La primera corrida de `main` falló al publicar: `denied: permission_denied: write_package`**
  (<https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39626576738>). El `docker login`
  con el `GITHUB_TOKEN` dio *Succeeded* — como avisa la guía del TP2, el login exitoso no garantiza
  el permiso — y recién falló el `push`. Causa: los dos packages los creé **a mano** en el TP2 con mi
  token personal, así que son packages **de mi usuario**, no del repositorio: el token de una corrida
  sólo puede escribir en packages que el repositorio tiene autorizados. Si el pipeline hubiera
  creado packages nuevos, habrían nacido enlazados al repo con permiso de escritura (y privados: con
  el paso extra de hacerlos públicos). La corrección fue del lado del package, no del YAML: en
  *Package settings → Manage Actions access*, agregar el repositorio `IngeSoft3-2319274` con rol
  **Write**, para los dos. Lo que se aprende: «el repo puede leer el package» (que es lo que el
  `LABEL` del Dockerfile consigue) y «el repo puede escribir en el package» son dos permisos
  distintos.

### Los dos entornos: Neon + Render, armados por API

| Decisión | Por qué |
|---|---|
| **Neon** para las bases, y no el Postgres de Render | El Postgres gratuito de Render **expira a los 30 días** (con 14 de gracia): no cubre ni un TP. El de Neon es permanente, con límites de uso (0,5 GB, cómputo mensual, se duerme a los ~5 min idle y despierta solo). Elegir infraestructura es leer letra chica |
| **Un proyecto de Neon (`inventario`) con dos databases**, `app_qa` y `app_prod`, mismo servidor | Entornos separados a nivel de base, que es lo que la consigna pide; dos proyectos serían el doble de cómputo gratuito consumido para el mismo aislamiento |
| **`DATABASE_URL` = la URI de Neon con el prefijo `postgresql+psycopg://`** y `sslmode=require` | Es la única variable que la app lee para la base (decisión del TP2, en `app/config.py`): la misma imagen apunta a QA o a PROD cambiando sólo esa variable. psycopg 3 entiende `sslmode` y `channel_binding` tal como vienen en la URI |
| **El esquema lo crea la app al arrancar** (`Base.metadata.create_all` en `main.py`, del TP2) | Las dos bases nacen vacías; con el primer arranque de cada api de Render aparecen las tres tablas. Verificado con `information_schema.tables` en las dos |
| **Render: 4 web services Docker, plan free, región Oregon, Auto-Deploy OFF**, creados **por la API** (`POST /v1/services`) y no clickeando | Mismo resultado que el panel, pero reproducible: los ids, las URLs y las variables quedaron en un archivo local. Auto-Deploy apagado es la decisión conceptual del TP: si Render se desplegara solo en cada push, el deploy no pasaría ni por el CI ni por la aprobación — lo dispara **mi pipeline** |
| **Nombres**: `inventario-api-qa`, `inventario-front-qa`, `inventario-api-prod`, `inventario-front-prod` | Identificables en el panel y en los logs. `inventario-api-prod` ya estaba tomado en `onrender.com`, así que Render le agregó un sufijo: la URL real es `https://inventario-api-prod-7xrj.onrender.com` — y esa es la que llevan el smoke y el `BACKEND_URL` del front de PROD, copiada de lo que devolvió la API, no escrita de memoria |
| Variables del front: `BACKEND_URL` = la api de **su** entorno, **sin barra final**, y `DNS_RESOLVER=8.8.8.8` | Con barra, nginx manda todo a `/` y cada llamada da 404. El DNS de Docker (`127.0.0.11`) no existe en Render: hace falta uno público para que nginx resuelva `onrender.com` |
| Environments de GitHub creados **antes** de que un job los nombre, por API (`PUT …/environments/qa` y `…/production` con `reviewers` = yo y `prevent_self_review: false`) | Si un job referencia un environment inexistente, GitHub lo crea sin reglas ni secrets. `qa` sin reglas **a propósito** (es automático); `production` con required reviewer: el gate humano. *Prevent self-review* apagado es lo que me deja aprobar mis propios deploys — a diferencia de los PRs, acá GitHub lo permite |

**Cómo comprobé que cada entorno usa su propia base** (el error más silencioso del TP: PROD apuntando
a `app_qa`, que no pone nada en rojo). Inserté una categoría `SOY PROD` **sólo en `app_prod`** con
`psql` (desde un contenedor `postgres:16-alpine`, con la URI de Neon), y después:
`GET https://inventario-api-prod-7xrj.onrender.com/api/categorias` → `[{"id":1,"nombre":"SOY PROD",…}]`;
`GET https://inventario-api-qa.onrender.com/api/categorias` → `[]`; y `select count(*) from
categorias` en `app_qa` → `0`. Cada api habla con su base.

### El deploy lo dispara el pipeline — por la API de Render, no por el deploy hook

La guía usa el **Deploy Hook** de cada servicio (una URL secreta con `?key=…`, a la que se le pega
`&ref=<commit>`). Yo disparo el deploy con la **API de Render**
(`POST /v1/services/{id}/deploys` con `{"commitId": "<sha>"}`), desde
[`scripts/render-deploy.sh`](scripts/render-deploy.sh). Es la alternativa que la propia guía del
TP8 nombra como «la profesional», y la elegí por tres motivos, uno práctico y dos de fondo:

1. **Práctico**: los cuatro servicios los creé por la API, y la API **no expone el deploy hook**
   (ni en `GET /services/{id}` ni en ningún otro campo: sólo existe en el panel). Copiarlos a mano
   era el único paso artesanal de toda la cadena.
2. **El hook responde al instante y no dice nada más.** Render construye en background y, mientras
   construye —o si el build falla—, sigue sirviendo la versión anterior: el smoke puede dar verde
   contra la versión **vieja**. La guía lo reconoce como «limitación honesta» del hook. Con la API,
   el deploy tiene un **id**, y el script le pregunta su estado cada 15 s hasta que figure `live`
   (o falla si termina en `build_failed`, `update_failed`, `canceled`…). El smoke corre **después**,
   contra la versión nueva. Medido en el front de QA: `build_in_progress` → `update_in_progress`
   → `live` en 31 s con cache.
3. **El id del servicio queda a la vista.** `RENDER_SERVICE_API` y `RENDER_SERVICE_FRONT` son
   **variables** (no secrets) de cada environment: cualquiera puede leer en el YAML y en la corrida
   contra qué servicio se desplegó, y compararlo con el id del panel —que es la comprobación que la
   defensa pide sobre los hooks («¿el hook de PROD apunta al servicio de PROD?»), sin abrir nada
   secreto—. Con un hook, la URL entera es secreta y el id del servicio viaja adentro.

Lo que se mantiene igual que con el hook: **el commit va explícito** (`commitId` = `GITHUB_SHA`,
el equivalente exacto del `&ref=`), Auto-Deploy está apagado en los cuatro servicios, y en *Events*
de Render cada deploy dice que lo disparó la API —no un push ni un clic en el panel—.

**La contrapartida, y es una de alcance de secrets.** El hook de QA sólo puede desplegar QA; la
API key de Render puede desplegar **cualquier** servicio del workspace, y el plan gratuito no da
claves por servicio. La misma `RENDER_API_KEY` está cargada como secret en `qa` **y** en
`production`, y lo que separa un entorno del otro son las **variables** del environment (los ids)
más el YAML. En la práctica, un job de `qa` que quisiera desplegar PROD tendría que cambiar el YAML
—y eso pasa por un PR—, pero la credencial no se lo impediría. Es el precio de usar la API con una
clave de workspace, y lo declaro: el alcance de los secrets sigue siendo por environment (sin
aprobación, el job de `production` no lee ni la clave ni los ids), pero la clave de `qa` no es
«menos poderosa» que la de `production`, como sí lo sería un hook.

### La cadena, en corridas reales

| Qué | Enlace |
|---|---|
| Primer deploy a QA disparado por el pipeline (api y front `live` con `5aed07e`, smoke en la primera vuelta) | <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39633286706> |
| **Rechazo** del deploy a PROD, con motivo (el merge de #30 sólo agregaba el job; sin cambio de app no vale dos builds) | <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39633772783> |
| **Aprobación**: QA → *Waiting for review* → PROD `live` con `8652e2d` y el cambio visible en el subtítulo | <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39634412515> |
| Historial de deployments por environment | <https://github.com/marcosdon28/IngeSoft3-2319274/deployments> |

**Qué mira el aprobador antes de aprobar** (los criterios, no el trámite):

1. Que `deploy-qa` haya dejado **los dos** servicios `live` con el commit de la corrida, y el smoke
   verde — y en qué vuelta: una vuelta es normal; varias dicen que algo tardó y quiero saber qué.
2. **Qué cambia**: el título del PR mergeado y su diff. Un cambio de texto del front no es lo mismo
   que uno que toca `DATABASE_URL` o el esquema.
3. Que no haya **otra corrida** más nueva esperando: aprobar la vieja manda a PROD un commit
   anterior al que ya está (el `concurrency` no ordena la cola de aprobaciones).
4. El momento: no se despliega si no voy a poder mirar PROD los minutos siguientes.

Y por qué el rechazo fue ése: la corrida 39633772783 venía del merge de #30, que **sólo agrega el
job `deploy-prod` al workflow** — no hay un cambio de aplicación que justifique dos builds de PROD
en el plan gratuito, y el primer deploy aprobado convenía que llevara algo visible para comprobarlo
en la URL. Es un motivo específico de esa corrida, no un «viernes a la tarde».

### Continuous Delivery, no Continuous Deployment

Implementé **Continuous Delivery**: cada cambio verificado llega solo a QA y queda **listo** para
producción; el último paso lo autoriza una persona. No Continuous Deployment porque mi red de
seguridad hoy es unit tests + smoke: nadie verifica que la app **funcione** de punta a punta antes
de promover (eso es el TP7), y no tengo observabilidad de PROD (TP9) para enterarme rápido si un
deploy automático sale mal. Automatizar la promoción con esa red sería automatizar la propagación
de errores. Lo que me faltaría para la tercera: e2e como gate (TP7), monitoreo y alertas (TP9), y
un rollback automático disparado por esas alertas. ¿La querría? Para esta app sí: sin usuarios
reales el gate humano enseña más de lo que protege.

### Lo que se publica y lo que corre no son lo mismo (todavía)

Render **reconstruye** la app desde el repositorio en cada deploy: le paso el commit, y construye
mis Dockerfiles de nuevo. La imagen que el pipeline publicó en ghcr queda ahí, etiquetada, pero
**no es la que corre** en QA ni en PROD. Lo que pierdo: la garantía de «se promueve lo mismo que se
verificó» vale para el **commit**, no para los **bits**. Entre el build del pipeline y el de Render
puede cambiar una imagen base (`python:3.12-slim`, `nginx:alpine`, `node:22-alpine` no están
fijadas por digest) o resolverse distinto algo que no esté en el lockfile; y el build de Render ni
siquiera corre mis tests. Es el hueco que el TP7 cierra haciendo que Render **ejecute** la imagen
de ghcr. Mientras tanto, `/health` devuelve el commit horneado en la imagen, y el smoke lo compara.

### La letra chica del free tier, y cómo la maneja el pipeline

| Contrato | Consecuencia | Qué hace el pipeline / qué decidí |
|---|---|---|
| Render duerme un web service a los **15 min sin tráfico**; el primer pedido lo despierta con un cold start de hasta ~1 min | Un `curl` seco después de un rato da timeout o 503 | El smoke reintenta **30 veces cada 20 s** con `--max-time 10` en cada `curl` (sin tope, un servicio despertando acepta la conexión y no contesta: el job se colgaría hasta el límite del runner) |
| **750 horas de instancia por mes, del workspace**, compartidas por los 4 servicios | Un servicio despierto 24 h se come 720 él solo; si se acaban, Render **suspende todo**, PROD incluido | Presupuesto: los 4 duermen casi todo el día. Con ~2 h de uso diario entre QA y PROD son ~8 h × 4 = 32 h/día de **pico** teórico, pero sólo cuentan las horas despiertas: estimo < 150 h/mes. **No se pone nada que haga ping** para mantenerlos despiertos (el monitor del TP9 se pausa al terminar) |
| **500 minutos de build por mes** del workspace | Cada promoción completa construye 4 veces (api y front, QA y PROD); si se acaban, Render deja de construir y el deploy «sale bien» con la versión vieja | Medido hoy: builds de **31–46 s** con cache (api y front). Una promoción ≈ 3 min; el TP6 entero gastó ~12 builds ≈ 10 min. Y si Render no construyera, el smoke lo detecta: `/health` tiene que devolver **el commit de la corrida** |
| Neon suspende el cómputo a los **~5 min idle**; 0,5 GB y horas de cómputo mensuales limitadas | El primer pedido que toca la base tarda más (despierta solo, rápido) | El smoke pide `/api/productos`, que toca la base: si Neon no responde, el entorno no está vivo |
| Render le agrega un **sufijo** al nombre si ya está tomado en `onrender.com` | La URL de la api de PROD no es la que uno escribiría de memoria | Las URLs se copiaron de lo que devolvió la API al crear cada servicio, y el `BACKEND_URL` del front de PROD también |

### Qué prueba el smoke test, y qué no

Prueba **tres cosas**: que el proceso vive (`/health`), que **la base responde** (`/api/productos`:
un `/health` que no toca la base da verde con la connection string rota) y que el front se sirve.
Y, desde #32, una cuarta: que `/health` devuelva **el commit de la corrida**. Sin eso, el smoke no
distinguía la versión nueva de la anterior — y como Render sigue sirviendo la vieja mientras
construye, un build fallido daba verde. Lo que **sigue sin probar**: que la app *funcione* —que
crear un producto, registrar una salida y ver el descuento anden de punta a punta—. Que responda no
es que ande. Eso es la suite e2e del TP7.

### Deployment pattern para una producción real, y el rollback

**Para esta app con usuarios reales elegiría blue-green**, con feature flags para lo que sea
riesgoso de producto:

- **Por qué no rolling**: con una sola instancia por servicio no hay «tandas»; y el inventario
  tiene una base relacional con esquema: en rolling conviven dos versiones contra la misma base, y
  un cambio de columna rompe a la vieja mientras la nueva entra.
- **Por qué no canary (todavía)**: canary necesita **observabilidad** —tasa de errores y latencia
  por versión— para saber si «el canario sangra», y hoy no tengo nada de eso (llega en el TP9).
  Sin métricas, canary es ruleta.
- **Por qué blue-green**: dos entornos completos y un switch; el rollback es volver el switch, en
  segundos, y se puede probar el verde con tráfico sintético antes de cortar. Costo: 2× infra, que
  para cuatro contenedores chicos es asumible. Lo que **me falta hoy** para hacerlo: un router
  delante de los dos (Render no lo da en el plan gratuito), y la disciplina de esquema compatible
  hacia atrás (migraciones aditivas), porque la base es **una** sola para los dos colores.
- **Flags** para desacoplar deploy de release: por ejemplo, el cálculo de prioridad de reposición
  nuevo (#25) podría llegar apagado y prenderse para un depósito primero. Con una variable de
  entorno no alcanza (se lee al arrancar); haría falta un servicio de flags o una tabla de
  configuración que la app lea en caliente.

**Mi plan de rollback hoy, paso a paso:**

1. Decidir **a qué** volver: el último deploy bueno está en *Deployments → production* (y cuando
   hay release, es el commit de la release anterior: `git rev-list -n1 v6.0.0`).
2. Disparar el deploy de **ese commit** en los dos servicios de PROD con el mismo script que usa el
   pipeline (`RENDER_API_KEY=… ./scripts/render-deploy.sh <srv-api-prod> <sha>` y lo mismo con el
   front): es exactamente lo que hace `deploy-prod`, sin pasar por la aprobación porque **es una
   emergencia y la versión ya estuvo aprobada antes**.
3. Comprobar `/health` → `commit` igual al sha de vuelta, y la pantalla.
4. Abrir el PR que arregla, y volver a promover por la cadena normal.

**Cuánto tarda (medido, no estimado).** Lo hice de verdad el 21/10: después de la release
`v6.0.0` (PROD en `8652e2d`), mergeé y aprobé un cambio que se nota —`/health` pasó a informar el
commit (#32/#33)— y volví a `v6.0.0` disparando los dos deploys de PROD con
`scripts/render-deploy.sh … $(git rev-list -n1 v6.0.0)`, los dos a la vez:

| Servicio de PROD | Deploy | Inicio (Render) | `live` (Render) | Duración |
|---|---|---|---|---|
| api (`srv-dbce34bncjis7397mmgg`) | `dep-dbcet0hkjs5s73cg94lg` → `8652e2da` | 16:55:30 UTC | 16:56:09 UTC | **39 s** |
| front (`srv-dbce34qfngtc739ttam0`) | `dep-dbcet0nf3r2c73cqg980` → `8652e2da` | 16:55:30 UTC | 16:55:56 UTC | **26 s** |

**Rollback completo: 47 segundos** desde el comando hasta que los dos servicios figuraron `live`
(el cronómetro lo llevó el propio script). Comprobación desde afuera: `/health` de PROD volvió a
contestar `{"status":"ok"}` sin `commit`, que es lo que devolvía `v6.0.0`. Esas horas están en
*Deploys* de cada servicio de producción, en el panel de Render, y son lo que se mira en la
defensa. El número es chico porque Render tenía el build de ese commit en cache: un rollback a un
commit que nunca construyó tardaría lo que tarda un build (2–5 min). Y la métrica DORA que esto
ejercita es *failed deployment recovery time*.

Lo que el historial de *Deployments* de GitHub **no** registra: este rollback. Lo disparé yo con la
API, fuera de una corrida, así que GitHub sigue diciendo que en `production` está el último commit
aprobado. Es una limitación de hacerlo a mano: la forma de que quede registrado sería re-correr el
job `deploy-prod` de la corrida vieja (vuelve a pedir aprobación, y GitHub sólo deja re-correr
corridas de hasta 30 días).

**Lo que el rollback de código no deshace**: los datos. Si el deploy malo corrió una migración que
borró una columna o escribió filas con un formato nuevo, volver la imagen no las devuelve. Por eso
las migraciones tienen que ser **aditivas** (agregar, nunca borrar en el mismo deploy) y el
rollback de datos es otro plan: backup previo al deploy, o *point-in-time recovery* (Neon lo tiene
hasta 6 horas en el plan gratuito).

- **El smoke con commit puso en rojo la primera corrida que lo tenía — y tenía razón.**
  <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39635800039>: `deploy-qa` dejó
  los dos servicios `live` con el commit `3dfb44e`, y el smoke se quedó 30 vueltas leyendo
  `{"status":"ok","commit":"local"}`. El `--build-arg APP_COMMIT` lo recibe **la imagen que publica
  el pipeline en ghcr**; Render no la ejecuta: **reconstruye** mis Dockerfiles desde el repositorio,
  sin ese argumento, y el `ARG` cae a su default. Es la demostración más concreta que pude tener de
  lo que el §3.2 de la guía llama «mal a propósito»: lo que corre en QA es *otra construcción* del
  mismo commit, no mi imagen. Mientras el TP7 no cierre ese hueco, `/health` usa el
  `RENDER_GIT_COMMIT` que Render inyecta en sus builds (PR
  [#33](https://github.com/marcosdon28/IngeSoft3-2319274/pull/33)); el `APP_COMMIT` horneado sigue
  teniendo prioridad y va a ser el que mande cuando los servicios pasen a ejecutar la imagen. Y
  queda dicho: un smoke que sólo pregunta «¿respondés?» habría dado verde en esa corrida.

### El tag `v6.0.0` está movido, y lo declaro

Lo puse primero sobre `8652e2d` —el commit que estaba en PROD al cerrar la cadena— y lo moví al
commit que cierra esta sección de `decisiones.md`, **después de aprobar su deploy a producción**:
así el tag sigue apuntando a lo que corre en PROD **y** contiene la documentación del práctico. Es
el procedimiento del reglamento (§3): `git tag -f v6.0.0 <sha> && git push -f origin v6.0.0`.

### Declaración de uso de IA — TP6

Usé **Claude Code (Claude Fable 5.1)**, y con una particularidad de este práctico: la IA no sólo
escribió, también **operó** — creó el proyecto y las bases en Neon y los cuatro servicios en Render
por sus APIs, cargó los secrets y las variables de los environments, rechazó y aprobó deploys por la
API de GitHub, y disparó el rollback. El reglamento (§6) dice que la vara es la misma, y así lo
verifiqué:

| Qué fue asistido | Cómo lo verifiqué |
|---|---|
| Los cambios del `ci.yml` (publicación, `deploy-qa`, `deploy-prod`, los smokes) y `scripts/render-deploy.sh` | Los leí paso por paso y **los vi correr**: el PR con «Entrar al registry» salteado, la corrida de `main` con publicar como último paso, el deploy a QA con los dos `live`, el *Waiting for review*, el rechazo y la aprobación. Y el smoke con commit **se puso rojo** la primera vez por una causa real (Render reconstruye): no es un check decorativo |
| La creación de la infraestructura por API (Neon, Render, environments de GitHub) | Comprobé cada cosa desde afuera, no leyendo la respuesta de la API: las cuatro URLs contestan, `information_schema.tables` muestra las tres tablas en las dos bases, `SOY PROD` aparece sólo en PROD, *Auto-Deploy: no* en los cuatro servicios, y los secrets están en el environment que corresponde (`gh secret list --env …`) |
| La plantilla de nginx | Probada con y sin variables (`grep` del `default.conf` generado adentro del contenedor, `nginx -t`), con el compose local y, al final, con el front de QA pidiéndole `/api/categorias` a su api por nginx |
| Los motivos del rechazo y de las aprobaciones | Los escribí sobre lo que **esa** corrida mostraba (qué PR era, en qué vuelta pasó el smoke); no son frases genéricas |
| El rollback | Lo ejecuté y lo cronometré; las horas de la tabla son las de *Deploys* de Render, y el `/health` de PROD cambió de respuesta |
| Redacción de esta sección | Revisada contra lo que pasó; los problemas listados son los que me pasaron, en el orden en que me pasaron |

Lo que **no** delegué: Render + Neon como riel y por qué, usar la API en vez de los hooks y asumir
la contrapartida del alcance de la clave, qué mira el aprobador, el patrón de deployment para una
producción real, y el plan de rollback.

---

## TP7 — Contenedores en el pipeline + integración y e2e

### Build once, deploy many: el problema del TP6 que resuelve la imagen como unidad

En el TP6 lo pude ver con un ejemplo propio y no con el del escenario: el smoke con commit se puso
**rojo** en la corrida 39635800039 porque `/health` decía `"commit":"local"`. Render reconstruía
mis Dockerfiles en cada deploy, y ese build no era el del pipeline: no recibía el `--build-arg`, no
pasaba por los tests, y entre uno y otro podía cambiar una imagen base (`python:3.12-slim`,
`nginx:alpine`, `node:22-alpine` no están fijadas por digest). Lo que corría en QA era **otra
construcción** del mismo commit. Desde el PR [#35](https://github.com/marcosdon28/IngeSoft3-2319274/pull/35)
los cuatro servicios **ejecutan la imagen del registry**: la misma que construyó el job que corrió
los tests, bit a bit. La unidad de release pasó de «un commit que alguien construye» a «una imagen
inmutable que se promueve».

### Cómo pasaron los servicios a ejecutar la imagen

| Decisión | Por qué |
|---|---|
| **Cambiar la fuente de los cuatro servicios existentes** (`PATCH /v1/services/{id}` con `image.imagePath`), no crear servicios nuevos | Conserva las URLs, las variables de entorno, los ids (que son las variables de los environments) y el historial de deploys. Crear nuevos habría dado otras URLs y obligado a recargar `BACKEND_URL`, smokes y enlaces — y a borrar los viejos para no duplicar horas del workspace |
| **La imagen con la que quedaron configurados**: `sha-393bb89…` (el commit de cierre del TP6, verificado con `docker pull` sin sesión) | Render exige una imagen para cambiar la fuente; es sólo el **punto de partida**. Lo que corre lo nombra **cada deploy** del pipeline con su propio `sha-<commit>`: Render sólo exige que coincidan el registry y el nombre de la imagen. Esa configuración **no se actualiza** con cada merge, y por eso el botón *Manual Deploy* del panel sería peligroso: desplegaría la imagen de *Settings*, no la que corre |
| Primero **uno solo** (el front de QA), con un deploy a mano por `imageUrl`, y recién después los otros tres y el pipeline | Cambiar la fuente **no despliega nada**: el servicio sigue corriendo lo que tenía. El deploy a mano fue la prueba (`live` en ~30 s, con el digest `sha256:8930…` registrado en el deploy, y el front sirviendo contra su api); la entrega es lo que despliega la corrida |
| El deploy manda **`imageUrl`** (el equivalente del `imgURL` del hook) y **ya no manda commit** | Con una imagen no hay nada que construir. Dejar el `commitId` le haría creer a quien lea el YAML que Render todavía compila. El script acepta las dos cosas y lo dice en el log |
| **Una sola etiqueta por imagen, `sha-<40 caracteres>`; `latest` no existe** | `latest` no dice qué contenido hay detrás y se mueve. Un deploy que lo nombrara ejecutaría «lo último publicado», haya pasado las e2e o no. Con el commit en la etiqueta no hay forma de desplegar algo sin decir exactamente qué es. El registry compara la etiqueta letra por letra: el commit corto no sirve (`manifest unknown`) |

**Del tag de git a la imagen, en un paso**: `git rev-list -n1 v7.0.0` da el commit; esa etiqueta
`sha-<commit>` está en los dos packages. `v7.0.0` es el **nombre** de una versión que sé que anduvo
en PROD; `sha-<commit>` es **el binario** de ese nombre. Para promover uso siempre el segundo: el
tag de git se puede mover; una imagen etiquetada por commit no cambia de contenido.

**Cómo se comprueba, desde afuera, que un entorno EJECUTA mi imagen.** Tres lugares, de más a
menos público: (1) `/health` devuelve el commit **horneado en la imagen** (`ARG APP_COMMIT`, que
sólo pone el pipeline) y el smoke lo compara con el de la corrida; (2) la API de Render muestra, en
cada deploy, `image.ref = ghcr.io/…:sha-<commit>` y `image.sha = sha256:…` (el digest); (3) en el
panel, *Events* de cada servicio dice que el deploy lo disparó la API (mi usuario) y nombra la
imagen. Lo que el smoke **no** alcanza a probar: que la app funcione. Que responda y corra el
commit correcto no dice que crear un producto ande — eso es la e2e.

### Las dos suites: qué probé en cada una, y por qué no es lo mismo

Las dos viven en `frontend/e2e/` y usan la misma herramienta, **Playwright**: la de integración con
el fixture `request` (un cliente HTTP, sin navegador), la e2e con Chromium. Las dos corren
**contra QA desplegado** —la api y el front de QA, que ya ejecutan la imagen de esa corrida— y
ninguna usa dobles: ni `page.route`, ni base en memoria, ni `test.skip`.

**Integración (`e2e/api.spec.js`, job `integracion`)** — la api con su base de verdad detrás:

| # | Prueba | Por qué ésa |
|---|---|---|
| a | Alta de una categoría → `GET` la encuentra → `DELETE` 204 → ya no está | El `GET` que sigue al `POST` le pregunta **a Postgres**, no a un doble. Si el código mandara algo que la base rechaza, acá contesta 500 y un unitario con `Mock(spec=Session)` daría verde |
| b | Nombre vacío → `422` y la lista **no cambió** | El contrato del error, y que «rechazar» sea de verdad no crear |
| c | **La regla 1 contra la base** (la elegí yo): producto con stock 5, salida de 6 → `400` «Stock insuficiente» y el `GET` del producto sigue diciendo 5 | Es la regla central del dominio. El unitario del TP5 prueba la *lógica* con un producto armado a mano; ésta prueba que la regla frena **antes del `commit`** con una transacción real: si alguien moviera el `producto.stock -= cantidad` arriba del `if`, el unitario con mock también lo vería, pero sólo ésta vería que la base quedó mal |

**E2E (`e2e/inventario.spec.js`, job `e2e`)** — un navegador usando la app completa:

| # | Flujo | Por qué ése |
|---|---|---|
| 1 | **Creación**: escribir una categoría con nombre único, *Agregar*, verla en la tabla, *Eliminar <nombre>*, que desaparezca | El ciclo completo front → nginx → api → base → front, afirmando sobre el dato que el test creó |
| 2 | **Error/validación**: producto con stock 5, pedir una salida de 6 → el usuario **ve** el motivo exacto («Stock insuficiente: hay 5 y querés sacar 6.»), el botón queda deshabilitado, el historial no tiene la fila y la base tampoco | Lo que el usuario ve cuando se equivoca también es comportamiento |
| 3 | **El flujo de todos los días** (lo elegí yo): registrar una salida de 10 unidades, ver el «10 % de descuento» antes de confirmar y después en el historial (`9.000,00`), y el stock bajado en la base | Es lo que un encargado de depósito hace cada día: si mañana no anda, **me escriben por esto**. Y toca el borde de la regla 5 de punta a punta: el front calcula 10 %, la api lo recalcula y la tabla lo muestra |

**Lo que cada suite ve y las otras no.** El unitario con doble (TP5) verifica *mi lógica* con la
base reemplazada; la integración verifica que *mi api y Postgres se entiendan* (tipos, constraints,
transacciones); la e2e verifica que *el front use bien la api* (el nombre del campo, la ruta, el
texto del botón, lo que se muestra). Un cambio de una línea que **sólo** atrapa la integración: que
`producto_service.crear` dejara de hacer `.upper()` del SKU y la base tuviera un índice único
case-insensitive — el mock acepta cualquier cosa; Postgres no. Y **el par verde/rojo** es un
diagnóstico sin abrir el código: integración verde + e2e roja = la api y la base están sanas, el
que usa mal la api es el front; integración roja = la api o la base, y la e2e ni corre (su `needs`
no se cumple).

**Lo que NO puse en cada suite, y por qué (pirámide).** En integración no están las reglas de
borde del descuento (9 contra 10 unidades) ni los mensajes de validación de Pydantic: eso ya lo
custodian 38 unitarios en milisegundos, y repetirlos contra Neon sería pagar segundos por lo mismo.
En e2e no está «crear un producto desde el formulario» ni «dar de baja»: cada flujo de navegador
cuesta ~1 s contra QA y comparte el entorno con todas las corridas; tres flujos que cubren
crear/ver/borrar, el error y el uso diario alcanzan para la red de seguridad. La UI de productos
se verifica indirectamente (los productos de los flujos 2 y 3 se crean por API y aparecen en el
selector del formulario).

**Integración amplia, no estrecha.** La estrecha —levantar la api en el runner con un Postgres como
`services:` del job— llega antes (no necesita deploy) y aísla cada corrida; la amplia prueba la api
**ya desplegada**, con la imagen exacta de la corrida y la base real de QA, con un décimo de la
configuración. Elegí la amplia porque lo que quiero saber es si *esta imagen, en Render, contra
Neon* anda — no si el código anda en un Postgres de laboratorio. Lo que pierdo: aislamiento (QA es
uno solo) y velocidad (depende del cold start).

**Cold start y tests flaky.** `timeout: 60 s` por test, `expect.timeout: 15 s` por aserción,
`retries: 1`. El retry absorbe una demora suelta de la red; si un test pasa recién en el retry
aparece como **flaky** en el reporte con la corrida en verde, y eso se mira: un flaky aislado puede
ser el plan gratuito; el mismo test flaky dos corridas seguidas es el test. Un test que a veces
falla es peor que no tenerlo: entrena al equipo a ignorar el rojo. Y los dos jobs corren **después**
del smoke de `deploy-qa`, que ya despertó QA y esperó `live`: por eso un minuto por test alcanza.
Nada de `sleep`: cada `expect` espera a que la condición se cumpla, hasta su tope.

**QA es uno solo y lo comparten todas las corridas — y las dos suites.** Cada prueba fabrica sus
datos con `Date.now()` en el nombre y **borra lo que creó, comprobándolo** (`DELETE` 204 y después
un `GET` que ya no lo encuentra), en un `finally` para que un fallo a mitad de camino no deje basura.
Lo aprendí en la primera corrida local: la e2e de categorías falló por un selector ambiguo y dejó
una categoría `e2e …` en la base; la segunda corrida la encontró. Y el **límite conocido** de la
cadena: con dos merges seguidos, la corrida B redespliega QA mientras la integración o la e2e de A
lo usan — un rojo de A que no es de su código, o peor, un verde que probó la imagen de B. Lo
reconocería mirando en Render qué imagen corre QA y a qué hora corrió el `deploy-qa` de B; lo
resolvería rechazando la corrida A con el motivo y dejando que valga la B, que trae los dos
cambios. La regla práctica: **un merge por vez** mientras la cadena corre. Un equipo real lo
resuelve con un entorno por corrida; acá QA es uno.

**La misma imagen del front en QA y en PROD.** `ghcr.io/marcosdon28/inventario-frontend:sha-<commit>`
corre en los dos entornos, bit a bit. Lo único que los distingue son dos variables del servicio:
`BACKEND_URL` (la api de **su** entorno, sin barra final) y `DNS_RESOLVER`; nginx las lee al
arrancar desde la plantilla del TP6. Adentro de la imagen quedan el `dist/` de Vite —que llama a
`/api/...` con ruta relativa, sin ningún host— y la plantilla. Del lado del backend, lo mismo con
`DATABASE_URL`. Si alguna dirección estuviera horneada, la imagen de QA no serviría para PROD y
«se promueve lo mismo que se verificó» sería mentira.

### La cadena completa, en corridas reales

| Qué | Enlace |
|---|---|
| Primer deploy **por imagen** a QA y a PROD (api y front `live` con `sha-11410dd…`, digest registrado en el deploy) | <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39641520928> |
| **Primera cadena completa**: build → deploy-qa → integración (19 s) → e2e (49 s) → aprobación → deploy-prod | <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39643619818> |
| **La rotura controlada**: integración **verde**, e2e **roja**, `deploy-prod` sin arrancar | <https://github.com/marcosdon28/IngeSoft3-2319274/actions/runs/39644611792> · reportes de esa corrida: `playwright-report-integracion` (verde) y `playwright-report-e2e` (rojo), en *Artifacts* |
| El commit que rompió la app (sólo `Movimientos.jsx`, nada de `e2e/`) | <https://github.com/marcosdon28/IngeSoft3-2319274/pull/38> |
| El arreglo, y la **cadena completa verde** posterior hasta PROD | <https://github.com/marcosdon28/IngeSoft3-2319274/pull/39> |

### La e2e frenando una promoción: qué se rompió y cómo lo diagnostiqué con los dos reportes

**Qué cambié**: el texto del botón del formulario de movimientos, «Registrar» → «Guardar»
(PR #38, un solo archivo de la app: `frontend/src/pages/Movimientos.jsx`). Elegí eso y no el nombre
del campo que el front manda porque lo que la e2e tiene que atrapar es lo que **nadie más ve**: un
cambio de texto no rompe el build, no lo ve ningún unitario (los del front prueban `lib/reglas.js` y
`api.js`, no componentes) y el smoke le habla a la api, no al botón. Compiló, los 37 tests del front
pasaron, QA respondió y corría el commit.

**Qué hizo la cadena** (corrida 39644611792): `build` ✓ → `deploy-qa` ✓ (smoke verde, vuelta 1,
con el commit comprobado) → `integracion` ✓ **3 passed (7 s)** → `e2e` ✗ (`1 passed, 2 failed`,
con su retry cada uno, 3 min 20 s) → **`deploy-prod` salteado**: ni apareció como pendiente de
aprobación. El smoke en verde es parte del punto: el sistema respondía y aun así estaba roto.

**Cómo lo diagnostiqué, con los reportes y no con el código.** Bajé los dos artefactos de esa
corrida (`gh run download … -n playwright-report-e2e` y `-n playwright-report-integracion`). El
verde dice que la api y la base están sanas: alta, borrado, validación y la regla 1 pasaron contra
la api de QA. El rojo, en el test *«una salida mayor al stock muestra el motivo, deshabilita el
botón…»*, dice:

```
Error: expect(locator).toBeDisabled() failed
Locator: getByRole('button', { name: 'Registrar' })
Error: element(s) not found
```

y el *snapshot* de la página que viene en el reporte muestra el formulario con un botón «Guardar»
donde la prueba buscaba «Registrar». El flujo de todos los días falló por lo mismo, al intentar
hacer click. **El par verde/rojo leído contra la tabla del §2.5**: la integración le habló a la api
con el contrato correcto y la base guardó y borró sin chistar → la api está bien; el que no ofrece
lo que el usuario necesita es el **front**. Fila 1, sin abrir el código. Si hubiera roto la api, la
integración se habría puesto roja y la e2e ni habría corrido (su `needs`): fila 2.

**Qué NO pasó gracias al gate**: PROD no recibió un front en el que no se puede registrar un
movimiento (el botón seguía existiendo, pero cualquier automatización, atajo o documentación que
dijera «Registrar» quedaba rota — y en un caso real sería el campo mal nombrado, con la api
rechazando cada alta). Y **qué clase de bug el gate no ataja**: uno que no esté en los tres flujos
—dar de baja un producto, por ejemplo—, o uno de datos (un descuento mal calculado que la e2e no
afirme), o uno que sólo aparezca con carga. La e2e es la red final, no la única.

**Lo que la corrida roja me enseñó de mis propias pruebas.** Dejó **basura en QA**: dos categorías
y dos productos `e2e …`. El `finally` que limpia estaba, pero el `click` al botón que no existía
esperó hasta el tope del **test** (60 s), el test murió por timeout y el `finally` nunca corrió.
Los borré a mano por la API y agregué `actionTimeout: 15_000` a la configuración (en el mismo PR
del arreglo): ahora una acción falla a los 15 s y la limpieza llega a ejecutarse. Es exactamente el
tipo de cosa que sólo se ve rompiendo de verdad.

### Problemas encontrados y cómo los resolví

- **`$img:sha-$SHA` en zsh no es lo que parece.** Al pasar tres servicios a imagen con un `for` en
  la terminal, la API contestó 400 y el error no decía por qué: zsh interpreta `$img:s…` como un
  *modificador de historial* y el JSON salió roto. Con `${img}` entre llaves anduvo. El primer
  servicio (el front de QA) lo había hecho sin bucle, por eso ese sí funcionó.
- **La primera e2e local falló por un selector ambiguo**: `getByRole('cell', { name })` matcheaba
  dos celdas, la del nombre y la del botón «Eliminar <nombre>» (que también contiene el nombre).
  `exact: true` lo resuelve. Y dejó una categoría en la base local; de ahí el `finally` de limpieza.
- **La corrida roja dejó basura en QA** (arriba): el timeout del test mató el `finally`. Arreglado
  con `actionTimeout`.
- **Dos PRs quedaron `BEHIND` al mergear uno antes**: la protección de `main` tiene `strict: true`
  (TP4), así que `gh pr merge` los rechaza hasta hacer *Update branch*. `gh pr update-branch`, que
  re-dispara los checks, y después el merge. Es el gate del TP4 haciendo lo suyo.
- **Un reporte de Playwright se coló en un commit.** Al preparar la rama de la rotura desde un
  `main` anterior al `.gitignore` nuevo, `git add frontend` se llevó `playwright-report/index.html`
  y `test-results/.last-run.json`. Lo vi en el `--stat` antes de mergear y los saqué con
  `git rm --cached` + `--amend`. Lección: mirar el `--stat` de cada commit, no sólo el diff.

### Declaración de uso de IA — TP7

Usé **Claude Code (Claude Fable 5.1)**, que además de escribir **operó**: pasó los cuatro servicios
de Render a imagen por la API, hizo el deploy de prueba, mergeó, aprobó y bajó los reportes.

| Qué fue asistido | Cómo lo verifiqué |
|---|---|
| Las dos suites de Playwright | Cada prueba la leí preguntándome **qué verifica, contra qué entorno corre y qué pasa si falla**: por eso cada una afirma sobre su propio dato (nombre con la hora), limpia y comprueba la limpieza. Las corrí primero contra el compose local (6 en verde, base vacía al final) y después en QA. Y **las vi fallar por una rotura real** de la app, no del test |
| Los endpoints `DELETE` del backend (regla 8 y anulación) | Siete unitarios con mock que invierten cada rama (con movimientos → 400 y sin `delete`; sin movimientos → `delete` una vez; anular una entrada que dejaría stock negativo → regla 1), y la suite de integración los usa contra Postgres en cada corrida |
| El paso a imagen de los servicios y el `imageUrl` del script | Comprobado desde afuera: `runtime: image` y `repo: null` en la API, el deploy con `image.ref` y digest, y `/health` devolviendo el commit **horneado** (ya no el `RENDER_GIT_COMMIT` de un rebuild) |
| El diagnóstico de la corrida roja | Lo hice con los reportes descargados —el error, el snapshot del formulario con el botón «Guardar»— antes de mirar el diff; el diff sólo lo confirmó |
| Redacción de esta sección | Revisada contra lo que pasó, en el orden en que pasó |

Lo que **no** delegué: qué tres flujos y qué tres pruebas de integración (y por qué ésas), amplia
contra estrecha, qué romper para la evidencia, y la lectura del par verde/rojo.
