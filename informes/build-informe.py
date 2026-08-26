#!/usr/bin/env python3
"""Genera informes/TP1-informe.html embebiendo las capturas de img/ en base64.

Después, para producir el PDF:
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \\
    --headless --disable-gpu --no-pdf-header-footer \\
    --print-to-pdf=informes/TP1-informe.pdf file://$PWD/informes/TP1-informe.html
"""
import base64, pathlib, datetime

REPO = pathlib.Path(__file__).resolve().parent.parent   # la raíz del repositorio
IMG  = REPO / 'img'

def b64(name):
    return 'data:image/png;base64,' + base64.b64encode((IMG / name).read_bytes()).decode()

def fig(src, cap):
    return '<figure><img src="' + src + '"/><figcaption>' + cap + '</figcaption></figure>'

FIG1  = fig(b64('01-push-directo-rechazado.png'),
    'Salida real del intento de push directo. GitHub responde <code>GH006: Protected branch update '
    'failed</code> y <code>! [remote rejected] main -&gt; main (protected branch hook declined)</code>; '
    'el comando sale con código 1. Después, <code>git reset --hard HEAD~1</code> deshace el commit '
    'local que ya no sirve.')
FIG1B = fig(b64('01b-web-editor-bloquea-main.png'),
    '«You can’t commit to <code>main</code> because it is a protected branch». La única opción '
    'habilitada es <em>Create a new branch for this commit and start a pull request</em>: la regla '
    'no grita, desvía.')
FIG1C = fig(b64('01c-proteccion-de-rama.png'),
    'Settings → Branches → regla sobre <code>main</code>. «Require a pull request before merging» '
    'tildado, «Require approvals» sin tildar (cero aprobaciones, deliberado), y «Do not allow '
    'bypassing the above settings» tildado.')
FIG2  = fig(b64('02-conflicto-en-el-pr.png'),
    'El PR de la rama B después de mergear la A: cartel «Merge conflicts», el aviso «This branch has '
    'conflicts that must be resolved» con <code>README.md</code> señalado, y el botón <em>Squash and '
    'merge</em> deshabilitado.')
FIG3  = fig(b64('03-marcadores-de-conflicto.png'),
    'El editor de conflictos: <code>&lt;&lt;&lt;&lt;&lt;&lt;&lt; feature/titulo-b (Current change)</code> '
    'abre mi versión, <code>=======</code> separa, <code>&gt;&gt;&gt;&gt;&gt;&gt;&gt; main (Incoming '
    'change)</code> cierra la que ya está en <code>main</code>. Arriba a la derecha, «1 conflict» y '
    '<em>Mark as resolved</em> deshabilitado.')
FIG4  = fig(b64('04-release-v1.0.0.png'),
    'La release publicada, con la etiqueta <em>Latest</em>, el tag <code>v1.0.0</code>, el commit que '
    'marca y las notas de qué incluye esta versión.')

FECHA = datetime.date.today().strftime('%d/%m/%Y')


CSS = """
@page { size: A4; margin: 18mm 16mm 20mm 16mm; }
* { box-sizing: border-box; }
body { font: 10.5pt/1.55 -apple-system, "Segoe UI", Helvetica, Arial, sans-serif; color: #1c1e21; margin: 0; }
h1, h2, h3 { color: #0b2447; line-height: 1.25; }
h2 { font-size: 14pt; margin: 22pt 0 8pt; padding-bottom: 4pt; border-bottom: 2px solid #0b2447; break-after: avoid; }
h3 { font-size: 11.5pt; margin: 14pt 0 5pt; break-after: avoid; }
p  { margin: 0 0 8pt; text-align: justify; }
ul, ol { margin: 0 0 8pt; padding-left: 18pt; }
li { margin-bottom: 4pt; }
code { font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 9pt;
       background: #f0f2f5; padding: 1px 4px; border-radius: 3px; }
pre { background: #12161c; color: #e6e9ef; padding: 9pt 11pt; border-radius: 5px;
      font: 8.5pt/1.5 "SF Mono", Menlo, Consolas, monospace; overflow-wrap: break-word;
      white-space: pre-wrap; margin: 0 0 9pt; break-inside: avoid; }
pre .cm { color: #8b96a5; }
table { width: 100%; border-collapse: collapse; margin: 0 0 10pt; font-size: 9.5pt; break-inside: avoid; }
th, td { border: 1px solid #ccd2da; padding: 5pt 7pt; text-align: left; vertical-align: top; }
th { background: #eef1f6; font-weight: 600; }
figure { margin: 10pt 0 14pt; break-inside: avoid; }
figure img { width: 100%; border: 1px solid #ccd2da; border-radius: 4px; display: block; }
figcaption { font-size: 8.5pt; color: #56606d; margin-top: 4pt; }
.cover { height: 232mm; display: flex; flex-direction: column; justify-content: center; text-align: center; }
.cover .materia { font-size: 12pt; letter-spacing: .12em; text-transform: uppercase; color: #56606d; }
.cover .tp { font-size: 30pt; font-weight: 700; color: #0b2447; margin: 10pt 0 2pt; }
.cover .sub { font-size: 15pt; color: #2b4a70; margin-bottom: 26pt; }
.cover .rule { width: 70px; height: 3px; background: #0b2447; margin: 0 auto 26pt; }
.cover table { width: 78%; margin: 0 auto; font-size: 10.5pt; }
.cover td { border: none; padding: 4pt 6pt; }
.cover td:first-child { font-weight: 600; width: 38%; color: #56606d; }
.cover td:nth-child(2) { text-align: left; }
.callout { border-left: 3px solid #0b2447; background: #f4f7fb; padding: 8pt 11pt; margin: 0 0 10pt;
           font-size: 9.5pt; break-inside: avoid; }
.callout strong:first-child { color: #0b2447; }
.pb { break-before: page; }
"""

P = []
A = P.append

A('<!doctype html><html lang="es"><head><meta charset="utf-8">')
A('<title>TP1 — Git colaborativo</title><style>' + CSS + '</style></head><body>')

# ── Portada ──────────────────────────────────────────────────────────────
A('''<section class="cover">
  <div class="materia">Ingeniería del Software 3 · UCC 2026</div>
  <div class="tp">Trabajo Práctico 01</div>
  <div class="sub">Git colaborativo</div>
  <div class="rule"></div>
  <table>
    <tr><td>Alumno</td><td>Marcos Don</td></tr>
    <tr><td>Matrícula</td><td>2319274</td></tr>
    <tr><td>Usuario GitHub</td><td>marcosdon28</td></tr>
    <tr><td>Repositorio</td><td>github.com/marcosdon28/IngeSoft3-2319274</td></tr>
    <tr><td>Versión entregada</td><td>v1.0.0</td></tr>
    <tr><td>Fecha</td><td>''' + FECHA + '''</td></tr>
    <tr><td>Riel</td><td>GitHub (canónico)</td></tr>
  </table>
</section>''')

# ── 1 ────────────────────────────────────────────────────────────────────
A('''<section class="pb">
<h2>1. Objetivo y qué se evalúa</h2>
<p>El TP1 pide poner a funcionar —y poder defender— el flujo con el que un equipo integra código:
ramas cortas que entran por Pull Request, revisión antes de integrar, protecciones sobre
<code>main</code> y versionado de la entrega. Antes de escribir una línea de código de producción se
deja armado <em>cómo</em> va a entrar ese código.</p>
<p>Este repositorio no es sólo el del TP1: es <strong>el repositorio del semestre</strong>. La app
elegida en el TP2 entra acá mismo, y cada TP siguiente le suma una capa. Por eso las decisiones de
este trabajo —protecciones, convención de ramas, estrategia de merge— condicionan todo lo que viene.</p>
<h3>Tareas exigidas por el enunciado</h3>
<table>
  <tr><th>Requisito</th><th>Estado</th></tr>
  <tr><td>Repositorio público con <code>.gitignore</code> en la raíz</td><td>✔ Cumplido</td></tr>
  <tr><td><code>main</code> protegida: imposible pushear directo, sin bypass ni para el dueño</td><td>✔ Cumplido y verificado</td></tr>
  <tr><td>Al menos 2 PRs mergeados, uno con conflicto resuelto</td><td>✔ 3 PRs; el #3 con conflicto</td></tr>
  <tr><td>Tag <code>v1.0.0</code> con su release publicada</td><td>✔ Cumplido</td></tr>
  <tr><td><code>decisiones.md</code> y <code>evidencias.md</code> en la raíz</td><td>✔ Cumplido, entraron por PR</td></tr>
</table>
<div class="callout"><strong>La regla innegociable de la materia:</strong> «si no lo podés explicar,
no lo aprobás — aunque funcione». La defensa oral pesa 50 %. Por eso este informe no se limita a
listar comandos: explica <em>por qué</em> cada uno.</div>
</section>''')

# ── 2 ────────────────────────────────────────────────────────────────────
A('''<section>
<h2>2. Entorno y setup</h2>
<p>Antes de tocar el repositorio hay que tener resueltas dos cosas: la identidad con la que van a
quedar firmados los commits, y cómo se autentica Git contra GitHub. Desde 2021 GitHub no acepta la
contraseña de la cuenta desde la terminal, así que hace falta un token o —el camino que usé— el
GitHub CLI, que además deja Git configurado.</p>
<pre>$ git config --global user.name
marcosdon28
$ git config --global user.email
marcosdon28@gmail.com
$ gh auth status
github.com
  ✓ Logged in to github.com account marcosdon28 (keyring)
  - Git operations protocol: ssh
$ ssh -T git@github.com
Hi marcosdon28! You've successfully authenticated…</pre>
<p>La autenticación es por <strong>SSH</strong>: la clave de esta máquina está cargada en la cuenta,
así que <code>git push</code> no pide credenciales en cada operación. El protocolo elegido explica
por qué los mensajes de error que aparecen más adelante dicen
<code>github.com:marcosdon28/…</code> con dos puntos, y no <code>https://…</code>.</p>
</section>''')

# ── 3 y 4 ────────────────────────────────────────────────────────────────
A('''<section>
<h2>3. Creación del repositorio</h2>
<p>Crear un repositorio es un acto de <em>administrador</em>, y ahí se toman tres decisiones:</p>
<ul>
  <li><strong>Público</strong> — requisito de la materia, y no por capricho: las funciones que se usan
  durante el semestre (protecciones, minutos de Actions ilimitados, environments con aprobaciones,
  secret scanning, CodeQL) son gratuitas <em>sólo</em> en repositorios públicos.</li>
  <li><strong>Con README</strong> — así el repositorio nace con un archivo y con la rama
  <code>main</code> ya creada, en vez de nacer vacío.</li>
  <li><strong>El nombre</strong> — <code>IngeSoft3-2319274</code>, que identifica materia y matrícula.
  Es el repositorio que se entrega en las dos presentaciones del año.</li>
</ul>
<pre>$ gh repo create IngeSoft3-2319274 --public --add-readme --clone
https://github.com/marcosdon28/IngeSoft3-2319274</pre>
</section>

<section>
<h2>4. El primer commit (y el único push directo del semestre)</h2>
<p>El repositorio arranca con dos archivos, commiteados <strong>antes</strong> de activar la
protección. Es el único momento del semestre en que un push directo a <code>main</code> va a
funcionar, y queda declarado como tal.</p>
<h3><code>.gitignore</code></h3>
<p>Le dice a Git qué <em>no</em> se versiona. Arranca con el bloque base de la guía —artefactos de
build, secretos, basura del sistema operativo y del editor— y le agregué desde ya los bloques de
Python y Node, porque la app del semestre es FastAPI + React y esas carpetas
(<code>__pycache__/</code>, <code>.venv/</code>, <code>node_modules/</code>) aparecen apenas empiece
el TP2. La línea que más importa es <code>.env</code>: los secretos no se commitean nunca.</p>
<h3><code>CLAUDE.md</code></h3>
<p>Deja escritas las reglas de trabajo del repositorio: todo entra por PR, qué archivo se actualiza en
qué momento, cómo se cierra cada TP con su tag. Es la misma idea que la protección de rama aplicada a
las convenciones: <strong>un proceso importante no debería depender de que alguien se acuerde</strong>.
Si está en un archivo, se lee, se revisa y se discute.</p>
<pre>$ git add .gitignore CLAUDE.md
$ git commit -m "chore: agrega .gitignore base y CLAUDE.md con las reglas de trabajo del repo"
$ git push                          <span class="cm"># funciona: la protección todavía no existe</span></pre>
</section>''')

# ── 5 ────────────────────────────────────────────────────────────────────
A('''<section class="pb">
<h2>5. Proteger <code>main</code></h2>
<p>Es la configuración más importante del trabajo práctico: hacer que <strong>nadie</strong> pueda
pushear directo a <code>main</code> — ni siquiera yo, que soy el dueño. Todo cambio pasa a tener que
entrar por un Pull Request.</p>
<p>La configuré por API en vez de por la web. Las tres tildes de la interfaz son más rápidas, pero un
comando queda <strong>reproducible y auditable</strong>: se puede volver a correr, versionar y
revisar. Es el mismo principio de <em>policy as code</em> que después sostiene los pipelines.</p>
<pre>$ gh api --method PUT "repos/{owner}/{repo}/branches/main/protection" --input - &lt;&lt;'EOF'
{
  "required_pull_request_reviews": { "required_approving_review_count": 0 },
  "required_status_checks": null,
  "enforce_admins": true,
  "restrictions": null
}
EOF</pre>
<table>
  <tr><th>Opción</th><th>Por qué está así</th></tr>
  <tr><td><code>required_pull_request_reviews</code></td>
      <td>Es la regla del juego: nada entra a <code>main</code> sin pasar por un PR.</td></tr>
  <tr><td><code>required_approving_review_count: 0</code></td>
      <td>Cero aprobaciones obligatorias. El TP es individual y GitHub <strong>nunca</strong> permite
      aprobar el propio Pull Request (por API devuelve <code>422 Can not approve your own pull
      request</code>). Con 1 aprobación no podría mergear nunca. En un equipo real acá iría 1 o más.</td></tr>
  <tr><td><code>enforce_admins: true</code></td>
      <td>Es el equivalente de <em>Do not allow bypassing</em>: la regla me alcanza también a mí. Sin
      esto GitHub me dejaría saltearla — y una protección que el dueño puede saltear es de adorno.</td></tr>
  <tr><td><code>required_status_checks: null</code></td>
      <td>Todavía no hay pipeline que exigir. En el TP4 este campo pasa a listar los checks de CI y el
      merge va a necesitar además el pipeline en verde.</td></tr>
</table>''' + FIG1C + '</section>')

# ── 6 ────────────────────────────────────────────────────────────────────
A('''<section class="pb">
<h2>6. La prueba de fuego: que la protección me rechace a mí</h2>
<p>Una protección que nunca rechazó nada no se sabe si funciona. La única forma de verificarla es
intentar violarla.</p>
<pre>$ echo "test" &gt;&gt; README.md
$ git commit -am "test: intento de push directo a main"
$ git push                          <span class="cm"># ← esto TIENE que fallar</span></pre>''' + FIG1 + '''
<div class="callout"><strong>Dónde se rechaza, y por qué importa:</strong> el mensaje empieza con
<code>remote:</code>. El commit se creó sin problema en mi máquina — Git local no sabe nada de
políticas de GitHub. Lo que falló fue la <em>publicación</em>: el servidor evaluó la regla y se negó.
Local y remoto son dos repositorios independientes, y la protección vive en uno solo de los dos.</div>
<p>La misma política, vista desde el navegador: intentando editar el README desde la web, GitHub avisa
que no se puede commitear a <code>main</code> y ofrece la única salida posible.</p>''' + FIG1B + '</section>')

# ── 7 ────────────────────────────────────────────────────────────────────
A('''<section class="pb">
<h2>7. El ciclo del Pull Request</h2>
<p>Este es el ciclo que se repite todo el semestre: rama corta → cambio → PR → lectura del diff →
merge → borrar la rama → traer el cambio a la máquina.</p>
<pre>$ git switch -c feature/seccion-instalacion
<span class="cm"># … editar el README …</span>
$ git add README.md
$ git commit -m "docs: agrega sección de instalación al README"
$ git push -u origin feature/seccion-instalacion
$ gh pr create --title "…" --body "…"
$ gh pr diff 1                      <span class="cm"># leer el cambio antes de integrarlo</span>
$ gh pr merge 1 --squash --delete-branch
$ git switch main &amp;&amp; git pull       <span class="cm"># ← el paso que siempre se olvida</span></pre>
<h3>Por qué <em>squash</em></h3>
<p>Las tres estrategias reales del botón de merge son <em>merge commit</em>, <em>squash</em> y
<em>rebase</em>. Elegí squash: aplasta todos los commits de la rama en uno solo sobre
<code>main</code>, así el historial queda lineal y legible —un commit por PR— y revertir un cambio
completo es un solo <code>git revert</code>. Lo que se pierde es el paso a paso interno de la rama,
que en ramas cortas no aporta gran cosa. El <em>fast-forward</em>, aclaración fina, no es una opción
que se elija: es lo que pasa automáticamente cuando <code>main</code> no avanzó.</p>
<h3>El último comando no es decorativo</h3>
<p>El merge ocurrió <strong>en GitHub</strong>. Mi copia local no se entera sola: hasta que no hago
<code>git pull</code>, mi <code>main</code> sigue en el commit viejo. Saltearse ese paso es la causa
número uno del próximo conflicto tonto — y es exactamente lo que se fabrica a propósito en la sección
que sigue.</p>
</section>''')

# ── 8 ────────────────────────────────────────────────────────────────────
A('''<section class="pb">
<h2>8. Provocar y resolver un conflicto</h2>
<p>Un conflicto no es un error: es lo que pasa cuando dos personas tocan la misma línea. Trabajando
solo hay que fabricarlo, y conviene: es mucho mejor que el primer conflicto sea en un entorno
controlado y no en el primer trabajo.</p>
<h3>La receta</h3>
<p>Dos ramas que nacen <strong>las dos del mismo commit de <code>main</code></strong> y cambian la
<strong>misma</strong> primera línea del README. El detalle donde se arruina el ejercicio es la base
de la segunda rama: si B nace de A, ya tiene el cambio de A adentro y el merge entra limpio. Por eso
nombré la base explícitamente en vez de confiar en dónde estaba parado.</p>
<pre>$ git switch -c feature/titulo-a main    <span class="cm"># → "# Proyecto IngSoft3 - versión A"</span>
$ git switch -c feature/titulo-b main    <span class="cm"># ← la base va explícita: main, no la rama A</span>
                                         <span class="cm"># → "# Proyecto IngSoft3 - versión B"</span>
$ gh pr merge 2 --squash --delete-branch <span class="cm"># A entra limpio…</span></pre>''' + FIG2 + '''
<h3>Por qué Git no puede resolverlo solo</h3>
<p>Git fusiona automáticamente cuando los cambios tocan partes distintas: compara ambas puntas contra
el ancestro común y aplica los dos. Acá no puede: la misma línea cambió de dos formas incompatibles.
Git tiene toda la información del problema y <strong>ninguna para resolverlo</strong> — cuál versión
es «la correcta» no es una pregunta técnica, es una decisión de contenido. Elegir por su cuenta
significaría descartar en silencio el trabajo de alguien. Por eso marca el archivo y delega.</p>''' + FIG3 + '''
<h3>Cómo lo resolví</h3>
<p>Con una <strong>síntesis</strong>, no con una de las dos versiones. Los sufijos «versión A» y
«versión B» existían sólo para fabricar el conflicto: quedarme con cualquiera de los dos habría
dejado el README del semestre con un título de ejercicio. El título final quedó
<code>#&nbsp;Proyecto IngSoft3 — Inventario de productos (UCC 2026)</code>. Ése es el punto del
ejercicio: resolver es decidir contenido, y a veces el contenido correcto no es ninguna de las dos
ramas.</p>
<pre>$ git switch feature/titulo-b
$ git merge origin/main            <span class="cm"># ← acá aparece el conflicto, con sus marcadores</span>
<span class="cm"># … editar el archivo, dejar el contenido final, borrar los tres marcadores …</span>
$ git add README.md
$ git commit -m "fix: resuelve el conflicto de título del README con una síntesis"
$ git push
$ gh pr merge 3 --squash --delete-branch</pre>
<h3>Qué habría evitado que apareciera</h3>
<ol>
  <li><strong>Integrar seguido.</strong> Si antes de abrir la rama B hubiera hecho
  <code>git switch main &amp;&amp; git pull</code>, B habría nacido del <code>main</code> que ya tenía el
  cambio de A: no hay dos versiones compitiendo, hay una sobre la otra. El conflicto no nace de tocar
  la misma línea, nace de <em>tocarla partiendo de estados distintos</em>.</li>
  <li><strong>Ramas cortas.</strong> Cuanto más vive una rama, más se aleja de <code>main</code> y más
  superficie de choque acumula. Es lo que DORA correlaciona con alto rendimiento: integrar a trunk al
  menos una vez por día.</li>
  <li><strong>Trabajo repartido.</strong> Si dos personas necesitan tocar la misma línea al mismo
  tiempo, suele ser señal de que las tareas no estaban bien separadas.</li>
</ol>
</section>''')

# ── 9 ────────────────────────────────────────────────────────────────────
A('''<section class="pb">
<h2>9. Versionar la entrega: tag y release</h2>
<p>Un <strong>tag</strong> marca un commit con un nombre inmutable; una <strong>release</strong> le
agrega la comunicación de qué cambió, escrita para humanos.</p>
<pre>$ git tag -a v1.0.0 -m "TP1 cerrado - Git colaborativo"
$ git push origin v1.0.0           <span class="cm"># los tags NO viajan con un push común</span>
$ gh release create v1.0.0 --title "v1.0.0 — TP1: Git colaborativo" --notes "…"</pre>''' + FIG4 + '''
<h3>Qué significa el número</h3>
<p>Versionado semántico: <code>MAJOR.MINOR.PATCH</code>. <strong>MAJOR</strong> sube cuando se rompe
compatibilidad; <strong>MINOR</strong>, cuando se agrega funcionalidad compatible;
<strong>PATCH</strong>, cuando se corrige un bug sin cambiar el comportamiento esperado. Acá es
<code>1.0.0</code> porque es la primera versión estable: no hay compatibilidad previa que romper, ni
funcionalidad agregada sobre algo anterior, ni bug corregido. Es el punto de partida.</p>
<p>El número de versión no es decorativo: es <strong>información para el que consume</strong> el
software. En el TP2 la misma disciplina se aplica a las imágenes de contenedor, y en el TP6 los
deploys nacen de tags.</p>
<div class="callout"><strong>El tag se movió, y queda declarado.</strong> Siguiendo el orden de la
guía, la release se publicó antes de agregar <code>decisiones.md</code> y <code>evidencias.md</code>
—que son justamente los archivos que documentan esa release—. Como el reglamento dice que el tag es
«el punto exacto que se mira de cada TP», moví <code>v1.0.0</code> al commit final del trabajo con
<code>git tag -f v1.0.0 &amp;&amp; git push -f origin v1.0.0</code>, que es el procedimiento que el propio
reglamento contempla.</div>
</section>''')

# ── 10 ───────────────────────────────────────────────────────────────────
A('''<section class="pb">
<h2>10. Los entregables, y dónde está cada cosa</h2>
<table>
  <tr><th>Qué</th><th>Dónde</th></tr>
  <tr><td>URL del repositorio público</td><td><code>github.com/marcosdon28/IngeSoft3-2319274</code></td></tr>
  <tr><td>Justificación de cada decisión + uso de IA</td><td><code>decisiones.md</code> (raíz)</td></tr>
  <tr><td>Las capturas con su explicación</td><td><code>evidencias.md</code> + <code>img/</code></td></tr>
  <tr><td>Reglas de trabajo del repositorio</td><td><code>CLAUDE.md</code> (raíz)</td></tr>
  <tr><td>Este informe</td><td><code>informes/TP1-informe.pdf</code> (fuente en <code>.html</code>)</td></tr>
  <tr><td>Historial: 3 PRs con su diff y su conversación</td><td>pestaña <em>Pull requests</em>, cerrados</td></tr>
  <tr><td>Estado congelado del TP</td><td>tag y release <code>v1.0.0</code></td></tr>
</table>
<p>Los tres Pull Requests mergeados, todos con estrategia squash y con la rama borrada después:</p>
<table>
  <tr><th>#</th><th>Qué hizo</th><th>Particularidad</th></tr>
  <tr><td>1</td><td>Sección de instalación en el README</td><td>Primer PR: valida el flujo con la protección recién puesta</td></tr>
  <tr><td>2</td><td>Título del README, versión A</td><td>Entró limpio</td></tr>
  <tr><td>3</td><td>Título del README, versión B</td><td><strong>Requirió resolver un conflicto de merge</strong></td></tr>
</table>
<h3>Dos archivos que existen y no se commitean</h3>
<p><code>aprendizajes.md</code> y <code>notas-defensa-p1.md</code> son notas personales de estudio, no
parte del entregable. Están ignorados vía <code>.git/info/exclude</code> y no vía
<code>.gitignore</code>: el primero es el ignore <strong>privado de este clon</strong> y no viaja a
quien clone el repositorio, mientras que el segundo se versiona y sí viaja. La contrapartida asumida
es que <code>.git/info/exclude</code> no se clona, así que en otra máquina hay que rehacerlo — queda
anotado en <code>CLAUDE.md</code>.</p>
</section>''')

# ── 11 ───────────────────────────────────────────────────────────────────
A('''<section class="pb">
<h2>11. Problemas encontrados y aprendizajes</h2>
<h3>El orden de los pasos no es opcional</h3>
<p>El <code>.gitignore</code> y el <code>CLAUDE.md</code> se commitearon antes de activar la
protección. Queda entonces <strong>exactamente un push directo a <code>main</code></strong> en todo el
historial, y está declarado. Si la protección se activa primero, ni el commit inicial puede entrar sin
PR: es correcto, pero hay que saberlo antes, no descubrirlo.</p>
<h3>Al fabricar el conflicto, casi lo arruino</h3>
<p>La rama B tiene que salir de <code>main</code>, no de la A. Nombrar la base explícitamente
(<code>git switch -c feature/titulo-b main</code>) evita depender de dónde estaba parado.</p>
<h3>GitHub no sabe al instante si un PR tiene conflicto</h3>
<p>Apenas mergeada la rama A, consultar el estado del PR de B devolvía <code>mergeable: UNKNOWN</code>.
No estaba roto: GitHub recalcula la mergeabilidad de forma asíncrona. Unos segundos después pasó a
<code>CONFLICTING / DIRTY</code>. Es el mismo motivo por el que, después de resolver, a veces hay que
esperar antes de poder mergear.</p>
<h3><code>sed -i</code> en macOS no es el de Linux</h3>
<p>Pide un argumento de sufijo de backup: <code>sed -i '' '1s/.*/…/' README.md</code>, con las comillas
vacías. Sin ellas, macOS interpreta el patrón como nombre de archivo de backup y falla con un mensaje
que no menciona el problema real.</p>
<h3>Verificar «existe» no es verificar «vale lo que espero»</h3>
<p>Para automatizar las capturas del navegador, el chequeo de sesión iniciada miraba si existía el
<code>&lt;meta name="user-login"&gt;</code> de GitHub. Existe <strong>también cuando estás
deslogueado</strong>, con el atributo vacío — así que el chequeo daba positivo siempre y las primeras
capturas salieron con los botones <em>Sign in / Sign up</em> y sin el cuadro de merge, que GitHub no le
muestra a un visitante anónimo. Se arregló exigiendo que el contenido no esté vacío. La lección excede
a la herramienta: una aserción débil da falsos verdes, que es peor que no tener aserción.</p>
<h3>No pude capturar una ventana de terminal con el sistema</h3>
<p>El proceso desde el que trabajo no tiene el permiso de <em>Grabación de pantalla</em> de macOS:
<code>screencapture</code> devuelve el fondo de escritorio sin ninguna ventana. En vez de dejar la
evidencia incompleta, la salida real del push rechazado quedó transcripta literalmente en
<code>evidencias.md</code> además de renderizada como imagen, y se agregaron dos evidencias
equivalentes tomadas del navegador. Las tres muestran la misma política desde ángulos distintos.</p>

<h2>Declaración de uso de Inteligencia Artificial</h2>
<p>Usé <strong>Claude Code (Claude Opus)</strong> como asistente durante todo el TP1. El reglamento lo
permite y lo alienta, con tres condiciones: declararlo, verificarlo y poder defenderlo.</p>
<table>
  <tr><th>Qué fue asistido</th><th>Cómo lo verifiqué</th></tr>
  <tr><td>Ejecución de los comandos de <code>git</code> y <code>gh</code></td>
      <td>Leí cada comando antes de que corriera y comprobé su efecto en la web: el repositorio existe
      y es público, los PRs figuran mergeados con su diff, las ramas están borradas, el tag aparece en
      <em>Releases</em>.</td></tr>
  <tr><td>Configuración de la protección por API</td>
      <td>La leí de vuelta con <code>gh api … --jq</code> y la comparé contra lo que muestra
      <em>Settings → Branches</em>. Y sobre todo, <strong>la probé</strong>: el push directo tiene que
      fallar, y falla.</td></tr>
  <tr><td>Capturas de evidencia del navegador</td>
      <td>Automatizadas con Playwright sobre este mismo repositorio y con mi sesión. Revisé cada imagen
      a ojo antes de aceptarla: descarté dos tandas, una deslogueada y otra con un tooltip tapando la
      interfaz. Las URLs son públicas y contrastables.</td></tr>
  <tr><td>Redacción de <code>decisiones.md</code>, <code>evidencias.md</code> y este informe</td>
      <td>Los revisé y corregí para que digan lo que efectivamente pasó. Los problemas listados son los
      que me pasaron a mí, no ejemplos genéricos.</td></tr>
</table>
<p>Lo que <strong>no</strong> delegué: qué versión conservar al resolver el conflicto, la estrategia de
merge, y el criterio de qué va commiteado y qué no.</p>
</section>''')

# ── Anexo ────────────────────────────────────────────────────────────────
A('''<section class="pb">
<h2>Anexo — Los comandos, en orden</h2>
<pre><span class="cm"># ── Repositorio ──────────────────────────────────────────────</span>
gh repo create IngeSoft3-2319274 --public --add-readme --clone

<span class="cm"># ── Primer (y único) push directo ────────────────────────────</span>
git add .gitignore CLAUDE.md
git commit -m "chore: agrega .gitignore base y CLAUDE.md…"
git push

<span class="cm"># ── Ignore privado de este clon (no viaja al repo) ───────────</span>
printf 'aprendizajes.md\\nnotas-defensa-p1.md\\n' &gt;&gt; .git/info/exclude

<span class="cm"># ── Protección de main ───────────────────────────────────────</span>
gh api --method PUT "repos/{owner}/{repo}/branches/main/protection" --input - &lt;&lt;'EOF'
{ "required_pull_request_reviews": { "required_approving_review_count": 0 },
  "required_status_checks": null, "enforce_admins": true, "restrictions": null }
EOF
gh api "repos/{owner}/{repo}/branches/main/protection" \\
  --jq '{approvals: .required_pull_request_reviews.required_approving_review_count,
         admins: .enforce_admins.enabled}'

<span class="cm"># ── Prueba de fuego ──────────────────────────────────────────</span>
echo "test" &gt;&gt; README.md
git commit -am "test: intento de push directo a main"
git push                                   <span class="cm"># falla: protected branch hook declined</span>
git reset --hard HEAD~1

<span class="cm"># ── PR #1 ────────────────────────────────────────────────────</span>
git switch -c feature/seccion-instalacion
git add README.md &amp;&amp; git commit -m "docs: agrega sección de instalación al README"
git push -u origin feature/seccion-instalacion
gh pr create --title "…" --body "…"
gh pr diff 1
gh pr merge 1 --squash --delete-branch
git switch main &amp;&amp; git pull

<span class="cm"># ── El conflicto: PR #2 y #3 ─────────────────────────────────</span>
git switch -c feature/titulo-a main        <span class="cm"># base explícita</span>
git commit -am "docs: cambia el título del README a versión A"
git push -u origin feature/titulo-a &amp;&amp; gh pr create …

git switch -c feature/titulo-b main        <span class="cm"># base explícita otra vez</span>
git commit -am "docs: cambia el título del README a versión B"
git push -u origin feature/titulo-b &amp;&amp; gh pr create …

gh pr merge 2 --squash --delete-branch     <span class="cm"># A entra limpio</span>
gh pr view 3 --json mergeable              <span class="cm"># → CONFLICTING</span>

git switch feature/titulo-b
git merge origin/main                      <span class="cm"># aparece el conflicto</span>
<span class="cm"># … resolver, borrar los tres marcadores …</span>
git add README.md
git commit -m "fix: resuelve el conflicto de título del README con una síntesis"
git push
gh pr merge 3 --squash --delete-branch

<span class="cm"># ── Tag y release ────────────────────────────────────────────</span>
git switch main &amp;&amp; git pull
git tag -a v1.0.0 -m "TP1 cerrado - Git colaborativo"
git push origin v1.0.0
gh release create v1.0.0 --title "v1.0.0 — TP1: Git colaborativo" --notes "…"

<span class="cm"># ── Entregables, por PR como todo lo demás ───────────────────</span>
git switch -c docs/entregables-tp1
git add decisiones.md evidencias.md img/ informes/
git commit -m "docs: agrega decisiones, evidencias e informe del TP1"
git push -u origin docs/entregables-tp1 &amp;&amp; gh pr create …

<span class="cm"># ── Congelar el estado final del TP ──────────────────────────</span>
git tag -f v1.0.0 &amp;&amp; git push -f origin v1.0.0</pre>
</section>

</body></html>''')

out = REPO / 'informes' / 'TP1-informe.html'
out.parent.mkdir(exist_ok=True)
out.write_text(''.join(P), encoding='utf-8')
print('HTML escrito:', out.name, '%.0f KB' % (out.stat().st_size/1024))
