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
