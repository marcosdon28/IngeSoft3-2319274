#!/usr/bin/env python3
"""Genera informes/TP4-informe.html embebiendo las capturas de img/ en base64.

Después, para producir el PDF:
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf=informes/TP4-informe.pdf file://$PWD/informes/TP4-informe.html
"""
import base64
import datetime
import pathlib

REPO = pathlib.Path(__file__).resolve().parent.parent
IMG = REPO / "img"


def b64(name):
    return "data:image/png;base64," + base64.b64encode((IMG / name).read_bytes()).decode()


def fig(name, cap):
    return f'<figure><img src="{b64(name)}"/><figcaption>{cap}</figcaption></figure>'


FECHA = datetime.date.today().strftime("%d/%m/%Y")

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
.callout { border-left: 3px solid #0b2447; background: #f4f7fb; padding: 8pt 11pt; margin: 0 0 10pt;
           font-size: 9.5pt; break-inside: avoid; }
.callout strong:first-child { color: #0b2447; }
.pb { break-before: page; }
"""

P = []
A = P.append
A('<!doctype html><html lang="es"><head><meta charset="utf-8">')
A("<title>TP4 — CI: Pipelines as Code</title><style>" + CSS + "</style></head><body>")

A('''<section class="cover">
  <div class="materia">Ingeniería del Software 3 · UCC 2026</div>
  <div class="tp">Trabajo Práctico 04</div>
  <div class="sub">CI: Pipelines as Code</div>
  <div class="rule"></div>
  <table>
    <tr><td>Alumno</td><td>Marcos Don</td></tr>
    <tr><td>Matrícula</td><td>2319274</td></tr>
    <tr><td>Repositorio</td><td>github.com/marcosdon28/IngeSoft3-2319274</td></tr>
    <tr><td>Workflow</td><td>.github/workflows/ci.yml</td></tr>
    <tr><td>Jobs</td><td>build-backend · build-frontend (en paralelo)</td></tr>
    <tr><td>Gate</td><td>required status checks + strict</td></tr>
    <tr><td>Versión entregada</td><td>v4.0.0</td></tr>
    <tr><td>Fecha</td><td>''' + FECHA + '''</td></tr>
  </table>
</section>''')

A('''<section class="pb">
<h2>1. Objetivo y qué se evalúa</h2>
<p>Automatizar la verificación de la app: cada Pull Request y cada push a <code>main</code>
construyen las dos imágenes, con el pipeline como <strong>requisito obligatorio de merge</strong>.</p>
<table>
  <tr><th>Requisito</th><th>Estado</th></tr>
  <tr><td>Workflow en el repo, que entró por PR</td><td>✔ PR #18</td></tr>
  <tr><td>Corre en cada PR y cada push a <code>main</code></td><td>✔ 12 corridas registradas</td></tr>
  <tr><td>Build de las dos imágenes con los Dockerfiles del TP2, en paralelo</td><td>✔ 1m53s en vez de 2m40s</td></tr>
  <tr><td>Cache de capas funcionando</td><td>✔ 7 capas <code>CACHED</code>; 1m53s → 21s</td></tr>
  <tr><td>Required status checks activos sobre <code>main</code></td><td>✔ los dos jobs, <code>strict: true</code></td></tr>
  <tr><td>Demostración del gate: rojo → bloqueado → fix → verde → merge</td><td>✔ PR #20</td></tr>
  <tr><td>Status badge en el README</td><td>✔ PR #21</td></tr>
</table>
<div class="callout"><strong>Qué NO hace este pipeline todavía, a propósito:</strong> no corre tests
—eso es el TP5— y no publica las imágenes —eso es el TP7—. Hoy verifica que la app
<strong>se construye en una máquina limpia</strong>, que ya es bastante más de lo que había.</div>
</section>''')

A('''<section>
<h2>2. Qué es CI, y qué no</h2>
<p>Integración continua <strong>no es «tener un pipeline»</strong>: es la práctica de integrar el
trabajo con frecuencia, verificando cada integración automáticamente. La herramienta es el medio.</p>
<p>El problema que ataca: <strong>integrar tarde es integrar caro</strong>. Si cada uno trabaja
semanas en su rama, el día de la integración es un evento traumático. Si todos integran a diario y
cada integración dispara la verificación, los problemas aparecen en minutos — cuando el cambio que
los causó es chico y está fresco.</p>
<p>Se puede tener <strong>pipeline sin CI</strong>: un YAML que corre una vez por semana sobre ramas
que viven meses. Y se puede tener <strong>CI sin pipeline</strong>, si todos integran a diario y
verifican a mano — funciona hasta que el equipo crece o alguien se olvida. Lo que hace este TP es
juntar las dos cosas: la práctica, y la máquina que la hace cumplir.</p>
<h3>Pipeline as Code</h3>
<p>El pipeline es un archivo <strong>dentro del repo</strong>, no una configuración clickeada en una
web. Consecuencias: se versiona y se revisa como el código —un cambio al pipeline es un PR más, y de
hecho el PR #22 de este práctico modifica el pipeline y <strong>pasa por su propio gate</strong>—,
viaja con el código, y es reproducible.</p>
<p>Es la <strong>cuarta aparición del mismo patrón</strong> en la materia: todo lo importante se
declara explícitamente en vez de hacerse a mano. TP1 las protecciones, TP2 el entorno, TP3 el plan
enlazado al código, y ahora el proceso de build.</p>
</section>''')

A('''<section class="pb">
<h2>3. El workflow, decisión por decisión</h2>
<pre>name: CI

on:
  pull_request:
    branches: [main]      <span class="cm"># el que hace el trabajo: verifica ANTES del merge</span>
  push:
    branches: [main]      <span class="cm"># deja la corrida que lee el badge, y su cache</span>

jobs:
  build-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v6
      - uses: docker/setup-buildx-action@v4
      - uses: docker/build-push-action@v7
        with:
          context: ./backend
          push: false
          tags: inventario-backend:ci
          cache-from: type=gha,scope=backend
          cache-to: type=gha,mode=max,scope=backend

  build-frontend:
    <span class="cm"># … idéntico, con context ./frontend y scope=frontend</span></pre>
<table>
  <tr><th>Decisión</th><th>Por qué</th></tr>
  <tr><td>Dos jobs, uno por imagen</td><td>Son <strong>artefactos independientes</strong>. Un job único daría un solo check en rojo sin decir cuál se rompió</td></tr>
  <tr><td>En paralelo</td><td>Es el default de Actions y no hay dependencia que justifique serializarlos. El tiempo total pasa a ser el del más lento</td></tr>
  <tr><td><code>push: false</code></td><td>Hoy sólo se verifica que la imagen se construya. Publicarla es el TP7</td></tr>
  <tr><td><code>scope</code> distinto por job</td><td><strong>No es opcional</strong> con dos jobs: sin él comparten estante y se pisan</td></tr>
  <tr><td>Versiones fijadas (<code>@v6</code>, no <code>@main</code>)</td><td>Sin versión fijada el pipeline cambiaría solo el día que sus autores publiquen algo</td></tr>
</table>
<h3>Lo que NO está en el archivo, y es lo más importante</h3>
<p>No hay <strong>una sola línea de Python ni de Node</strong>. El workflow no sabe cómo se construye
la app — eso lo sabe el Dockerfile del TP2. Si el pipeline compilara aparte, con <code>pip</code> y
<code>npm</code> escritos en el YAML, habría <strong>dos definiciones de build</strong> que tarde o
temprano divergen: estaría verificando una compilación distinta de la que después se despliega.</p>
<div class="callout"><strong>Los jobs no comparten filesystem.</strong> Cada uno corre en un runner
limpio y distinto — son dos máquinas. Si un job necesitara algo que produjo otro, tendría que viajar
como artefacto o declararse <code>needs:</code> para el orden.</div>
</section>''')

A('''<section class="pb">
<h2>4. El paralelismo, medido</h2>
<table>
  <tr><th>Job</th><th>Duración</th></tr>
  <tr><td><code>build-backend</code></td><td>1 m 53 s</td></tr>
  <tr><td><code>build-frontend</code></td><td>47 s</td></tr>
  <tr><td><strong>Suma, si fueran secuenciales</strong></td><td>2 m 40 s</td></tr>
  <tr><td><strong>Reloj real, en paralelo</strong></td><td><strong>1 m 53 s</strong></td></tr>
</table>
<p>Los dos jobs arrancaron en el <strong>mismo instante</strong> (<code>12:45:20Z</code>), así que el
tiempo total es el del más lento y no la suma. El ahorro crece con cada job que se agregue: en el TP5
entran los tests.</p>
<p>El backend tarda más porque su etapa de build parte de <code>python:3.12</code> completa —1,62 GB,
la que trae compilador— mientras que el frontend usa <code>node:22-alpine</code>. Es el costo del
multi-stage del TP2, y se paga una sola vez gracias al cache.</p>

<h2>5. El cache de capas</h2>''' + fig("tp4-02-cache.png",
    "Las dos corridas, con las líneas extraídas de <code>gh run view --log</code>. En la primera, el "
    "paso que crea el venv e instala dependencias se ejecutó de verdad; en la segunda salió del cache "
    "junto con otras seis capas.") + '''
<table>
  <tr><th>Capa</th><th>¿Se reutiliza?</th><th>Por qué</th></tr>
  <tr><td>Las imágenes base</td><td>✅</td><td>No cambian nunca</td></tr>
  <tr><td><code>COPY requirements.txt</code> + <code>pip install</code></td><td>✅</td><td>Sólo se rehace si cambia <code>requirements.txt</code></td></tr>
  <tr><td><code>COPY app ./app</code></td><td>❌ si toqué código</td><td>Es lo que cambia en casi todos los PRs</td></tr>
  <tr><td>Las capas posteriores a una que cambió</td><td>❌</td><td>Docker invalida esa capa <strong>y todas las siguientes</strong></td></tr>
</table>
<p>Ese orden no es casual: es la razón por la que el Dockerfile del TP2 copia las dependencias
<strong>antes</strong> que el código. Al revés, cada cambio de una línea reinstalaría todo.</p>
<h3>Qué pasa si el cache desaparece</h3>
<p><strong>Nada grave: el pipeline funciona igual, sólo más lento.</strong> El cache es una
<strong>optimización</strong>, no una dependencia — vuelve a construir todo desde cero y a repoblarlo.
Es importante que sea así, porque el cache se desaloja solo: GitHub lo purga por antigüedad y por
límite de tamaño. Un pipeline que <em>necesita</em> el cache para funcionar está roto.</p>
<div class="callout"><strong>Detalle honesto:</strong> la primera corrida es más lenta que una sin
cache, porque además de construir tiene que <strong>exportar</strong> las capas — ese paso tardó
66,6 s. El cache se paga una vez y se cobra en todas las corridas siguientes.</div>
</section>''')

A('''<section class="pb">
<h2>6. El pipeline como gate</h2>
<p>En el TP1 la protección exigía que todo entrara por Pull Request. Este TP le suma la verificación
automática: <strong>required status checks</strong>. Hoy <code>main</code> exige dos condiciones, y
hacen falta las dos.</p>
<pre>gh api --method PUT "repos/{owner}/{repo}/branches/main/protection" --input - &lt;&lt;'EOF'
{
  "required_pull_request_reviews": { "required_approving_review_count": 0 },
  "required_status_checks": {
    "strict": true,
    "contexts": ["build-backend", "build-frontend"]
  },
  "enforce_admins": true,
  "restrictions": null
}
EOF</pre>
<div class="callout"><strong>El <code>PUT</code> reescribe la protección entera, no le agrega una
línea.</strong> Todo campo omitido vuelve a su default — por eso el JSON re-declara también lo del
TP1 (cero approvals y <code>enforce_admins</code>). Después de aplicarlo leí la protección de vuelta
para confirmar que no se había perdido nada.</div>
<p>Los <code>contexts</code> son el <strong>id del job</strong>. Si mañana le pusiera
<code>name:</code> a un job, el gate quedaría esperando un check que ya no existe y bloquearía todo.</p>''' +
    fig("tp4-01-gate-bloquea.png",
    "El gate actuando: los dos checks marcados <strong>Required</strong>, "
    "<code>build-frontend</code> en rojo, <code>build-backend</code> en verde, y el botón "
    "<em>Squash and merge</em> deshabilitado. Alcanza con un solo check en rojo.") + '''
<p>Desde la consola dice lo mismo, sin ambigüedad:</p>
<pre>$ gh pr merge 20 --squash
X Pull request #20 is not mergeable: <span class="cm">the base branch policy prohibits the merge.</span></pre>
<h3>Un detalle de vocabulario que confunde</h3>
<p>Con el build roto, la API devolvía <code>mergeable: MERGEABLE</code> y
<code>mergeStateStatus: BLOCKED</code>. <strong>No es contradictorio</strong>: <code>mergeable</code>
habla de <strong>conflictos de contenido</strong> (no había ninguno) y <code>mergeStateStatus</code>
habla de <strong>política</strong> (el gate). Son dos preguntas distintas.</p>
</section>''')

A('''<section class="pb">
<h2>7. La demostración: rojo → bloqueado → fix → verde</h2>
<ol>
  <li><strong>Rojo</strong>: un <code>import</code> a un archivo inexistente en
  <code>frontend/src/App.jsx</code>. <code>build-frontend</code> falla a los 30 s.</li>
  <li><strong>Bloqueado</strong>: botón de merge deshabilitado; la consola lo confirma.</li>
  <li><strong>Fix</strong>: un commit que saca el import. El pipeline <strong>re-corre solo</strong>.</li>
  <li><strong>Verde</strong> → <code>mergeStateStatus: CLEAN</code> → merge.</li>
</ol>
<h3>Por qué rompí el frontend y no el backend</h3>
<p>Es una diferencia de stack que vale la pena entender. El frontend <strong>se empaqueta</strong> —
Vite resuelve los imports al hacer el bundle—, así que un import roto lo tumba durante
<code>npm run build</code>. El backend es <strong>Python: no compila ni se empaqueta</strong>, y su
Dockerfile <strong>nunca ejecuta el código</strong> — sólo instala dependencias. Escribir
<code>import estonoexiste</code> en un <code>.py</code> daría <strong>verde igual</strong>: para
romperlo habría que romper la <strong>dependencia</strong>, con un paquete inexistente en
<code>requirements.txt</code>. Desde el TP5, con los tests adentro, el código del backend sí va a
poder romperlo.</p>

<h3><code>strict: true</code>: por qué hacen falta dos PRs para verlo</h3>
<p>Con un solo PR abierto esto no se puede demostrar. Dejé un segundo PR abierto <strong>antes</strong>
de mergear el de la rotura; al mergearlo, el otro quedó desactualizado.</p>''' +
    fig("tp4-03-strict-update-branch.png",
    "<strong>All checks have passed</strong> y aun así el merge deshabilitado: la rama está "
    "<em>out-of-date with the base branch</em>. Su verde se sacó contra un <code>main</code> que ya "
    "no existe.") + '''
<p>Sin <code>strict</code>, ese PR podría entrar en verde habiendo sido verificado contra un
<code>main</code> anterior — y romper <code>main</code> sin que ningún check lo haya visto venir.</p>
</section>''')

A('''<section class="pb">
<h2>8. Visibilidad: el badge y el historial</h2>''' + fig("tp4-04-badge-readme.png",
    "El badge en el README, mostrando el estado del último build de <code>main</code>.") + '''
<pre>[![CI](…/actions/workflows/ci.yml/badge.svg)](…/actions/workflows/ci.yml)</pre>
<p><strong>Son dos direcciones, y por eso los corchetes de afuera.</strong> La de adentro es la
<strong>imagen</strong>; la de afuera es <strong>adónde lleva al hacerle clic</strong>. Con sólo la
imagen el badge se ve igual, pero al clickearlo se abre el SVG suelto: una página en blanco. Es el
error más fácil de cometer acá porque no se nota mirando el README.</p>
<p>El badge lee el <strong>último build de <code>main</code></strong> — por eso el workflow necesita
el trigger <code>push: branches: [main]</code>: con sólo <code>pull_request</code> no tendría de
dónde leer.</p>''' + fig("tp4-05-historial-corridas.png",
    "El historial completo: la corrida en rojo del build roto, el fix en verde, y el merge a "
    "<code>main</code>. Se ven los dos tipos de evento, <code>pull_request</code> y <code>push</code>.") + '''
<p>Parece cosmético y es cultura: hace visible el estado del proyecto a cualquiera que entre al repo.
Un badge en rojo, a la vista, es una presión sana para arreglarlo.</p>
</section>''')

A('''<section class="pb">
<h2>9. Problemas encontrados y aprendizajes</h2>
<h3>Estaba usando versiones viejas de las actions</h3>
<p>Empecé con <code>checkout@v4</code>, <code>setup-buildx@v3</code> y <code>build-push@v6</code> —
dos o tres majors por detrás. <strong>Funcionaban</strong>, así que el pipeline en verde no me lo iba
a avisar nunca. Lo detecté consultando las releases de cada repositorio, y las subí en un PR aparte
que pasó por su propio gate. Un pipeline en verde dice que algo <em>funciona</em>, no que esté
<em>bien</em>.</p>
<h3>Buscar <code>CACHED</code> por la API no funciona</h3>
<p><code>gh api .../actions/jobs/&lt;id&gt;/logs</code> devuelve una redirección a un zip, así que el
<code>grep</code> daba cero y parecía que el cache no actuaba — cuando los tiempos decían lo
contrario. El comando correcto es <code>gh run view &lt;run&gt; --log</code>. Antes de creerle a una
medición conviene entender qué devuelve el comando que la produjo.</p>
<h3>El contexto en los Pull Requests</h3>
<p>En un PR, <code>GITHUB_REF_NAME</code> no vale el nombre de la rama sino
<code>&lt;numero&gt;/merge</code>: GitHub construye una mezcla de la rama con <code>main</code> y
verifica <strong>eso</strong>. Para loguear la rama real hay que usar <code>github.head_ref</code>.
No es cosmético — aclara que lo que el pipeline verifica no es tu rama, sino el
<strong>resultado propuesto del merge</strong>.</p>

<h2>Declaración de uso de Inteligencia Artificial</h2>
<table>
  <tr><th>Qué fue asistido</th><th>Cómo lo verifiqué</th></tr>
  <tr><td>El <code>ci.yml</code></td><td>Lo leí antes de commitearlo y sobre todo <strong>lo vi funcionar</strong>: los dos jobs arrancando en el mismo instante, 7 capas reutilizadas, y el gate frenando un merge de verdad</td></tr>
  <tr><td>La configuración del gate por API</td><td>Leí la protección de vuelta después del <code>PUT</code> para confirmar que no se había perdido nada del TP1</td></tr>
  <tr><td>Las mediciones</td><td>Salen de <code>gh api .../jobs</code> y <code>gh run view --log</code>, no de estimaciones</td></tr>
</table>
<div class="callout"><strong>Un error que cometí y corregí, porque viene al caso.</strong> Al armar la
evidencia del cache, la primera versión de la imagen tenía líneas de log de la primera corrida que
<strong>no había leído</strong>: estaban escritas a mano para ilustrar. Lo detecté al releerla, la
descarté entera y la rehíce extrayendo cada línea de <code>gh run view --log</code> de las dos
corridas reales. <strong>Una evidencia inventada es peor que no tener evidencia</strong>: la segunda
se nota, la primera no.</div>
<p>Lo que <strong>no</strong> delegué: la estructura del pipeline, la decisión de construir con el
Dockerfile en vez de compilar aparte, qué romper para demostrar el gate, y la interpretación de las
mediciones.</p>
</section>''')

A('''<section class="pb">
<h2>Anexo — Los comandos, en orden</h2>
<pre><span class="cm"># ── El workflow, por PR como todo ────────────────────────────────</span>
git switch -c feature/ci-build-imagenes
<span class="cm"># … escribir .github/workflows/ci.yml …</span>
gh pr create --title 'ci: construye las dos imágenes en paralelo, con cache'
gh pr merge 18 --squash --delete-branch

<span class="cm"># ── El gate (OJO: el PUT reescribe TODA la protección) ──────────</span>
gh api "repos/{owner}/{repo}/branches/main/protection"      <span class="cm"># mirar ANTES</span>
gh api --method PUT "repos/{owner}/{repo}/branches/main/protection" --input - &lt;&lt;'EOF'
{ "required_pull_request_reviews": { "required_approving_review_count": 0 },
  "required_status_checks": { "strict": true,
                              "contexts": ["build-backend","build-frontend"] },
  "enforce_admins": true, "restrictions": null }
EOF
gh api "repos/{owner}/{repo}/branches/main/protection" --jq '.required_status_checks'

<span class="cm"># ── Segundo PR abierto ANTES, para poder ver strict: true ───────</span>
git switch -c docs/muestra-del-freno   <span class="cm"># … cambio cualquiera … gh pr create</span>

<span class="cm"># ── La demostración del gate ────────────────────────────────────</span>
git switch -c feature/demo-gate
<span class="cm"># … import a un archivo inexistente en App.jsx …</span>
docker build ./frontend               <span class="cm"># comprobar que falla también local</span>
gh pr create --fill
gh pr merge 20 --squash               <span class="cm"># → "the base branch policy prohibits the merge"</span>
<span class="cm"># … sacar el import …</span>
git commit -am 'fix: saca el import al archivo que no existe' &amp;&amp; git push
gh pr checks 20                       <span class="cm"># → los dos en SUCCESS</span>
gh pr merge 20 --squash --delete-branch

<span class="cm"># ── strict: true en acción ──────────────────────────────────────</span>
gh pr view 19 --json mergeStateStatus  <span class="cm"># → BEHIND, con los checks en verde</span>
gh pr update-branch 19                 <span class="cm"># el pipeline re-corre sobre la mezcla</span>
gh pr merge 19 --squash --delete-branch

<span class="cm"># ── El badge ────────────────────────────────────────────────────</span>
git switch -c docs/badge-ci            <span class="cm"># … la línea en el README … gh pr create</span>

<span class="cm"># ── Medir lo que se afirma ──────────────────────────────────────</span>
gh api "repos/{owner}/{repo}/actions/runs/&lt;run&gt;/jobs" --jq '.jobs[].started_at'
gh run view &lt;run&gt; --log | grep -E 'importing cache|CACHED'

<span class="cm"># ── Cerrar el práctico ──────────────────────────────────────────</span>
git tag -a v4.0.0 -m "TP4 cerrado" &amp;&amp; git push origin v4.0.0</pre>
</section>

</body></html>''')

out = REPO / "informes" / "TP4-informe.html"
out.write_text("".join(P), encoding="utf-8")
print("HTML escrito:", out.name, "%.0f KB" % (out.stat().st_size / 1024))
