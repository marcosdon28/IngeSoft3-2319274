#!/usr/bin/env python3
"""Genera informes/TP3-informe.html embebiendo las capturas de img/ en base64.

Después, para producir el PDF:
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf=informes/TP3-informe.pdf file://$PWD/informes/TP3-informe.html
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
A("<title>TP3 — Planificación y trazabilidad</title><style>" + CSS + "</style></head><body>")

A('''<section class="cover">
  <div class="materia">Ingeniería del Software 3 · UCC 2026</div>
  <div class="tp">Trabajo Práctico 03</div>
  <div class="sub">Planificación y trazabilidad</div>
  <div class="rule"></div>
  <table>
    <tr><td>Alumno</td><td>Marcos Don</td></tr>
    <tr><td>Matrícula</td><td>2319274</td></tr>
    <tr><td>Repositorio</td><td>github.com/marcosdon28/IngeSoft3-2319274</td></tr>
    <tr><td>Proyecto (público)</td><td>github.com/users/marcosdon28/projects/2</td></tr>
    <tr><td>Sprint</td><td>Sprint 1 · 26/08 – 01/09/2026 · 1 semana</td></tr>
    <tr><td>Límite de trabajo en progreso</td><td>2</td></tr>
    <tr><td>Versión entregada</td><td>v3.0.0</td></tr>
    <tr><td>Fecha</td><td>''' + FECHA + '''</td></tr>
  </table>
</section>''')

A('''<section class="pb">
<h2>1. Objetivo y qué se evalúa</h2>
<p>Montar la gestión del proyecto sobre el mismo repositorio del semestre: jerarquía de trabajo,
sprint, tablero, y <strong>trazabilidad demostrable</strong> entre lo que se pide y el código que lo
implementa. El escenario del enunciado: el cliente pide visibilidad — quiere saber qué se está
haciendo, qué falta, y cómo se conecta cada cambio con lo pedido.</p>
<table>
  <tr><th>Requisito</th><th>Estado</th></tr>
  <tr><td>1 épica, 1 historia con criterios, 2 tareas, 1 bug</td><td>✔ issues #10 a #14</td></tr>
  <tr><td>Jerarquía <strong>navegable</strong> (sub-issues, no task-lists)</td><td>✔ verificada por GraphQL</td></tr>
  <tr><td>Sprint con duración elegida, con la historia y sus tareas</td><td>✔ Sprint 1, 1 semana</td></tr>
  <tr><td>Tablero con automatización mínima (cerrar → Done)</td><td>✔ y <strong>se la vio actuar</strong></td></tr>
  <tr><td>Límite de trabajo en progreso</td><td>✔ 2 en <em>In Progress</em></td></tr>
  <tr><td>1 PR mergeado que cierra su issue automáticamente</td><td>✔ PR #16 → cierra #12</td></tr>
  <tr><td>Proyecto <strong>público</strong> + <code>decisiones.md</code></td><td>✔</td></tr>
</table>
<div class="callout"><strong>Este práctico se lee distinto que el anterior.</strong> En el TP2 la guía
era práctica y la entrega era otra cosa; acá <strong>lo que la guía hace ES la entrega</strong>. Y no
lleva <code>evidencias.md</code>: el proyecto es público, así que quien corrige lo abre y lo ve en
vivo. Las capturas de este informe son para estudiar, no para reemplazar esa URL.</div>
</section>''')

A('''<section>
<h2>2. La jerarquía: épica, historia, tareas — y el bug al costado</h2>
<p>Tres niveles, y la diferencia entre ellos no es de tamaño sino de <strong>qué responden</strong>:</p>
<table>
  <tr><th>Nivel</th><th>Qué responde</th><th>¿Criterios de aceptación?</th></tr>
  <tr><td><strong>Épica</strong> #10</td><td>Cuál es el objetivo grande</td><td><strong>No.</strong> No se verifica por sí misma: se cierra cuando sus historias están cerradas</td></tr>
  <tr><td><strong>Historia</strong> #11</td><td>Qué valor se entrega, y a quién</td><td><strong>Sí.</strong> Es el nivel donde algo se puede comprobar</td></tr>
  <tr><td><strong>Tareas</strong> #12, #13</td><td>Qué hay que construir para entregarlo</td><td>No hace falta: se verifican contra la historia</td></tr>
</table>''' + fig("tp3-03-epica-jerarquia.png",
    "La épica con su historia colgando como <strong>sub-issue</strong> y la barra de progreso "
    "<code>0/1</code>: sigue abierta porque su historia sigue abierta.") + '''
<h3>Por qué sub-issues y no task-lists</h3>
<p>Una task-list (<code>- [ ] #12</code> escrito en el cuerpo) se ve casi igual y <strong>no sirve
para esto</strong>: no crea la relación padre-hijo navegable, que es justamente lo que el enunciado
pide. Con sub-issues se sube de la tarea a su historia y de ahí a la épica, y cada padre muestra una
barra de progreso real.</p>
<h3>El bug va al costado</h3>
<p>La jerarquía cuenta <strong>lo que se planificó construir</strong>. Un bug es un defecto de algo
<strong>ya construido</strong>: no era parte del plan, así que no forma parte del árbol. Colgarlo de
la historia que lo originó tendría además un efecto feo — esa historia ya estaría cerrada, y su barra
de progreso pasaría a mentir.</p>
<p><em>Matiz que conviene saber</em>: hay equipos que sí los cuelgan, no para planificar sino para
<strong>medir</strong> cuántos defectos se escapan por sprint; y en Azure Boards un Bug puede ser
hijo de una Feature. O sea que «al costado» es una <strong>convención de trabajo</strong>, no una
regla de la herramienta.</p>
</section>''')

A('''<section class="pb">
<h2>3. La historia y sus criterios de aceptación</h2>''' + fig("tp3-04-historia.png",
    "La historia en formato <em>Como… quiero… para…</em>, con sus cuatro criterios y sus dos tareas "
    "como sub-issues. La barra marca <code>1/2</code>.") + '''
<h3>Qué hace verificable a un criterio</h3>
<p>Un criterio sirve si dice <strong>qué hay que mirar</strong> para saber si está cumplido. Por eso
el issue lleva, además de la lista, una tabla que lo explicita:</p>
<table>
  <tr><th>Criterio</th><th>Cómo se verifica</th></tr>
  <tr><td>El workflow corre en cada PR a main</td><td>Se abre un PR y en <em>Checks</em> aparece la corrida</td></tr>
  <tr><td>Un test que falla bloquea el merge</td><td>Se rompe algo a propósito: el check queda en rojo y el botón de merge, deshabilitado</td></tr>
  <tr><td>El reporte queda como artefacto</td><td>Al final de la corrida, en <em>Artifacts</em>, hay un archivo descargable</td></tr>
  <tr><td>Badge visible en el README</td><td>Se abre el README y el badge está ahí</td></tr>
</table>
<p>El contraejemplo que conviene tener a mano: <em>«que el CI funcione bien»</em> <strong>no</strong>
es un criterio. No dice qué mirar ni cuándo está cumplido — dos personas pueden discutir para siempre
si se cumple.</p>
<h3>La historia mal escrita (el ejercicio)</h3>
<p>Creé a propósito el issue #15 —<em>«Como desarrollador quiero crear la tabla usuarios para guardar
los datos»</em>— para diagnosticarlo. Tiene la <strong>forma</strong> de historia y es una
<strong>tarea técnica disfrazada</strong>: «para guardar los datos» no es un beneficio, es la
definición de lo que hace una tabla; el «como desarrollador» tampoco ayuda, porque es quien la
implementa y no quien recibe el valor; y no tiene nada verificable. Es además una historia
<strong>horizontal</strong>: entrega una capa técnica, no una rebanada que alguien pueda usar.</p>
<p>Reescrita, con beneficiario y criterios: <em>«Como encargado de depósito quiero registrarme con
usuario y contraseña para que cada movimiento de stock quede asociado a quien lo hizo»</em>. La tabla
<code>usuarios</code> sigue haciendo falta — pero pasa a ser una <strong>tarea</strong> de esa
historia, que es su lugar. La diferencia no es de redacción: es de <strong>nivel</strong>.</p>
</section>''')

A('''<section class="pb">
<h2>4. El sprint y el tablero</h2>''' + fig("tp3-01-tablero.png",
    "El tablero: <em>Todo</em> con la épica, la historia (1/2), la tarea pendiente y el bug; "
    "<em>In Progress</em> con el límite <strong>0 / 2</strong>; <em>Done</em> con la tarea #12 y el "
    "chip del PR <strong>#16</strong> que la cerró.") + '''
<h3>Por qué el sprint dura una semana</h3>
<p>Porque es el <strong>ciclo real de entrega</strong>: la cátedra publica un TP por semana y la
defensa P1 cae en la clase 5. Con sprints de dos semanas el tablero mostraría un ritmo que no es el
que tengo — planificaría contra un calendario y trabajaría contra otro.</p>
<p>El argumento general: el sprint debería durar lo que dura el <strong>ciclo de feedback</strong>.
Más largo, y uno se entera tarde de que estimó mal; muy corto, y se gasta más tiempo en la ceremonia
que en el trabajo.</p>
<h3>Por qué el límite de trabajo en progreso es 2</h3>
<p>La regla de arranque: <strong>personas + 1</strong>. Trabajando solo, 2. El «más uno» es la
<strong>válvula</strong> para cuando algo queda esperando por fuera de mí —una revisión, un pipeline
corriendo— y necesito avanzar sin dejar lo anterior a medias.</p>
<p>Por qué un límite en primer lugar: <strong>el trabajo empezado y no terminado no vale nada</strong>.
Cuatro cosas al 60 % entregan cero; dos al 100 % entregan dos. El límite hace <em>visible</em> ese
costo. Y la mecánica es justamente ésa: <strong>no te lo impide, te lo muestra</strong> — el contador
de la columna se pone en rojo al pasarse.</p>
<ul>
  <li><strong>Qué me haría subirlo</strong>: sumar gente (la regla escala con personas), o descubrir
  que me bloqueo seguido esperando algo externo.</li>
  <li><strong>La señal de que quedó alto</strong>: <strong>si nunca lo alcanzo</strong>. Un límite que
  nunca frena nada no limita: es decorativo. En diez, con una persona, sería el mismo tablero sin
  límite y con un número al lado.</li>
</ul>''' + fig("tp3-06-sprint-api.png",
    "El sprint y el estado del tablero consultados por API: la historia y sus dos tareas en Sprint 1; "
    "la épica y el bug sin sprint. La épica abarca todo el semestre y el bug todavía no fue "
    "priorizado en ninguna iteración.") + '''
</section>''')

A('''<section class="pb">
<h2>5. Trazabilidad: del requerimiento al código</h2>
<p>La vuelta completa que pide el enunciado: desde una tarea cerrada llegar al PR y a los commits que
la implementaron, y de ahí subir a su historia y a la épica.</p>''' +
    fig("tp3-05-trazabilidad.png",
    "La tarea #12 cerrada. Arriba: el chip <strong>Parent</strong> hacia la historia y el chip "
    "<strong>#16</strong> del PR. En la línea de tiempo: <code>closed this as completed in #16</code> "
    "y <code>moved this from In Progress to Done</code>, hecho por "
    "<code>github-project-automation</code>. A la derecha: Status <strong>Done</strong>, el "
    "<em>Parent issue</em> con <code>1/2</code>, y la rama en <em>Development</em>.") + '''
<h3>Dos precisiones que cambian el resultado</h3>
<table>
  <tr><th>Detalle</th><th>Por qué importa</th></tr>
  <tr><td><code>Closes #12</code> va en la <strong>descripción del PR</strong>, no en el mensaje del commit</td>
      <td>Por mensaje de commit el issue <strong>igual se cierra</strong>, pero <strong>no queda enlazado al PR</strong> — y ese enlace es lo que permite navegar de la tarea al código, y lo primero que se mira al corregir</td></tr>
  <tr><td>El número es el de la <strong>tarea</strong>, no el de la historia</td>
      <td>Un PR implementa una tarea concreta. Cerrando la historia #11 la estaría dando por terminada con la mitad del trabajo sin hacer: la tarea #13 sigue abierta. La trazabilidad quedaría mintiendo</td></tr>
</table>
<h3>El PR hace lo que el issue dice</h3>
<p>La tarea #12 era «escribir el workflow de build y tests», y el PR crea exactamente ese archivo:</p>
<pre><span class="cm"># .github/workflows/ci.yml</span>
name: CI
on: [pull_request]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4</pre>
<p>Hoy el workflow sólo tiene que <strong>existir y correr</strong>: los builds reales de las dos
imágenes y el cache llegan en el TP4 —que va a reemplazar el job <code>build</code> por
<code>build-backend</code> y <code>build-frontend</code>— y los tests con su reporte, en el TP5. Esa
parte es la tarea #13, que <strong>queda abierta a propósito</strong>.</p>
<div class="callout"><strong>Un PR que cierra un issue que no implementó es trazabilidad de mentira:</strong>
el issue queda cerrado y el trabajo, sin hacer. Es lo primero que se mira al corregir.</div>
<h3>El estado en el que queda la entrega</h3>
<table>
  <tr><th>Issue</th><th>Estado</th><th>Por qué</th></tr>
  <tr><td>#12 — tarea del workflow</td><td><strong>Cerrada</strong></td><td>La cerró el PR #16</td></tr>
  <tr><td>#13 — tarea del artefacto</td><td>Abierta</td><td>Depende de los tests, que llegan en el TP5</td></tr>
  <tr><td>#11 — la historia</td><td>Abierta (1/2)</td><td>Falta una de sus dos tareas</td></tr>
  <tr><td>#10 — la épica</td><td>Abierta (0/1)</td><td>Su historia sigue abierta</td></tr>
  <tr><td>#14 — el bug</td><td>Abierta</td><td>Al costado, sin sprint: no fue priorizado todavía</td></tr>
</table>
<p>Es el estado correcto, y conviene poder explicarlo: la automatización mueve tarjetas, pero
<strong>no cierra una historia porque se hayan cerrado sus sub-issues</strong>. La barra puede llegar
a 2/2 y la historia sigue abierta hasta que alguien la cierre.</p>
</section>''')

A('''<section class="pb">
<h2>6. El bug: uno propio, no el de la guía</h2>
<p>El enunciado permite usar el bug del video, pero dice que uno propio es mejor. Usé uno
<strong>real de mi app</strong>, que puedo reproducir en vivo.</p>
<p><strong>Qué pasa</strong>: al levantar el sistema con <code>docker compose up -d</code> y abrir la
app enseguida, se ve el cartel de error con las listas vacías — y <strong>no se recupera solo</strong>
aunque el backend termine de arrancar dos segundos después.</p>
<p><strong>Por qué</strong>: en <code>frontend/src/App.jsx</code>, <code>recargar()</code> está
memoizada con <code>useCallback(…, [])</code> y se dispara desde un <code>useEffect</code> que corre
<strong>una sola vez</strong>. El <code>catch</code> guarda el mensaje y ahí termina: no hay reintento
ni estado de carga.</p>
<pre>const recargar = useCallback(async () =&gt; {
  try {
    const [p, c, m] = await Promise.all([...])
    setProductos(p); setCategorias(c); setMovimientos(m); setError(null)
  } catch (e) {
    setError(e.message)      <span class="cm">// ← se muestra el error y no se vuelve a intentar</span>
  }
}, [])

useEffect(() =&gt; { recargar() }, [recargar])   <span class="cm">// ← corre una sola vez</span></pre>
<p>El <code>healthcheck</code> del compose hace que <strong>el backend</strong> espere a que la base
esté lista, pero nginx sirve la SPA apenas arranca: no hay nada que retenga al browser hasta que la
API responda.</p>
<div class="callout"><strong>Por qué es un bug y no «trabajo que faltaba»:</strong> aparece sobre algo
<strong>ya entregado</strong> — la app del TP2, que está cerrada y etiquetada <code>v2.0.0</code>. Si
lo hubiera encontrado <em>mientras</em> esa historia estaba en curso, no sería un bug: sería que la
historia todavía no cumplía sus criterios de aceptación. El principio que ordena las dos situaciones
es uno solo: <strong>una historia con defectos no está terminada</strong>.</div>
</section>''')

A('''<section class="pb">
<h2>7. Problemas encontrados y aprendizajes</h2>
<h3>El CLI no puede crear campos <em>Iteration</em>, pero la API sí</h3>
<p><code>gh project field-create</code> sólo acepta <code>TEXT</code>, <code>NUMBER</code>,
<code>DATE</code> y <code>SINGLE_SELECT</code>, así que di por sentado que el campo Sprint había que
crearlo a mano. Probé igual la mutación <code>createProjectV2Field</code> con
<code>dataType: ITERATION</code> y <strong>funcionó</strong>.</p>
<p><strong>La lección excede a la herramienta</strong>: que una interfaz no exponga algo no significa
que la plataforma no lo soporte. Vale la pena mirar el esquema antes de resignarse.</p>
<h3>…pero el campo nace sin configurar, y eso sí es sólo web</h3>
<p>La mutación crea el campo con <code>duration: 0</code> y cero iteraciones: no existe mutación
pública para definir la duración ni generar las iteraciones. Una vez configurado desde la interfaz,
en cambio, <strong>asignar el sprint a cada item sí se puede por API</strong>, con
<code>updateProjectV2ItemFieldValue</code> y el <code>iterationId</code>.</p>
<h3>Dónde frené de automatizar, y por qué</h3>
<p>Intenté configurar la iteración, crear la vista de tablero y poner el límite con Playwright, y no
fue viable: Projects v2 es una aplicación propia donde los controles no exponen roles accesibles
estándar. El botón <em>New view</em> no es un <code>button</code> con nombre accesible; el selector de
fechas usa <code>div</code>s con <code>aria-label</code> dinámicos del tipo
<code>"Tuesday, September 1 (Inside selected range)"</code>, que cambian según el estado de la
selección.</p>
<p>Después de varios intentos frené y lo hice a mano. <strong>Automatizar algo que tarda treinta
segundos por interfaz no se justifica</strong>, y forzar selectores frágiles hubiera dejado un
procedimiento que se rompe con el próximo rediseño.</p>
<h3>Una verificación apurada me hizo dar por fallado algo que funcionó</h3>
<p>Consulté el campo Sprint inmediatamente después de guardarlo y la API devolvió cero iteraciones,
así que lo di por fallado. Al rato el mismo query devolvía la iteración de 7 días correctamente
guardada: GitHub propaga el cambio de forma asíncrona. <strong>Verificar demasiado rápido puede ser
peor que no verificar</strong>, porque uno actúa sobre una conclusión falsa — en este caso, casi
rehago a mano algo que ya estaba hecho.</p>
<h3>Los Projects de usuario nacen privados</h3>
<p>Y el entregable de este práctico <strong>es la URL</strong>: entregada privada, quien la abre ve un
404 — ni siquiera «no tenés permiso», sino «no existe». Se cambia con
<code>gh project edit 2 --owner "@me" --visibility PUBLIC</code>, que además es
<strong>idempotente</strong>. El control antes de entregar: abrir la propia URL en una ventana de
incógnito.</p>

<h2>Declaración de uso de Inteligencia Artificial</h2>
<table>
  <tr><th>Qué fue asistido</th><th>Cómo lo verifiqué</th></tr>
  <tr><td>Labels, issues, jerarquía y Project por CLI</td><td>Consulté la jerarquía <strong>de vuelta por GraphQL</strong> (<code>subIssues</code>) en vez de mirar la pantalla: épica → historia → dos tareas, con el bug fuera del árbol</td></tr>
  <tr><td>La historia y sus criterios de aceptación</td><td>Revisé cada criterio preguntándome <strong>cómo se comprueba</strong>. El que no pasaba esa prueba no entraba — por eso el issue lleva una tabla que dice, para cada uno, qué hay que mirar</td></tr>
  <tr><td>El PR de trazabilidad</td><td>Verifiqué que el PR <strong>hace lo que el issue dice</strong>, y después por API que #12 quedó cerrada y enlazada al PR #16, y que #11, #13 y #10 siguen abiertas</td></tr>
  <tr><td>El bug</td><td>Lo encontré leyendo mi propio código y lo reproduje: <code>down -v && up -d</code> y abrir la app enseguida. El issue cita la línea exacta</td></tr>
</table>
<p>Lo que <strong>no</strong> delegué: la duración del sprint, el límite de trabajo en progreso, el
diagnóstico de la historia mal escrita, y la decisión de usar un bug propio en vez del de la guía.</p>
</section>''')

A('''<section class="pb">
<h2>Anexo — Los comandos, en orden</h2>
<pre><span class="cm"># ── Permiso que faltaba ──────────────────────────────────────────</span>
gh auth refresh -h github.com -s project

<span class="cm"># ── Etiquetas (bug ya viene de fábrica) ──────────────────────────</span>
gh label create epic  --color 6f42c1 --description "Épica"
gh label create story --color 0e8a16 --description "Historia de usuario"
gh label create task  --color 1d76db --description "Tarea técnica"

<span class="cm"># ── La jerarquía ─────────────────────────────────────────────────</span>
gh issue create --title 'EPIC: Pipeline DevOps completo para mi app' --label epic  --body '…'
gh issue create --title 'CI: build y tests automáticos en cada PR'   --label story --body '…'
gh issue create --title 'Escribir el workflow de build y tests'      --label task  --body '…'
gh issue create --title 'Publicar el reporte de tests como artefacto' --label task --body '…'
gh issue create --title 'El front muestra error si el backend no responde' --label bug --body '…'

gh issue edit 10 --add-sub-issue 11      <span class="cm"># épica  → historia</span>
gh issue edit 11 --add-sub-issue 12      <span class="cm"># historia → tarea</span>
gh issue edit 11 --add-sub-issue 13

<span class="cm"># ── El proyecto ──────────────────────────────────────────────────</span>
gh project create --owner "@me" --title "IngSoft3 — Inventario DevOps"
gh project edit 2 --owner "@me" --visibility PUBLIC     <span class="cm"># nacen PRIVADOS</span>
for n in 10 11 12 13 14; do gh project item-add 2 --owner "@me" --url .../issues/$n; done

<span class="cm"># ── El campo Sprint: el CLI no puede, la API sí ─────────────────</span>
gh api graphql -f query='mutation { createProjectV2Field(input: {
  projectId: "PVT_…", dataType: ITERATION, name: "Sprint" }) { … } }'
<span class="cm"># … la duración y las iteraciones se configuran desde la interfaz …</span>

<span class="cm"># ── Asignar el sprint (esto SÍ por API) ─────────────────────────</span>
gh api graphql -f query='mutation { updateProjectV2ItemFieldValue(input: {
  projectId: "PVT_…", itemId: "PVTI_…", fieldId: "PVTIF_…",
  value: { iterationId: "91d15287" } }) { … } }'

<span class="cm"># ── Trazabilidad ─────────────────────────────────────────────────</span>
git switch -c ci/workflow-de-build-y-tests
mkdir -p .github/workflows        <span class="cm"># … escribir ci.yml …</span>
git add .github/workflows/ci.yml && git commit -m 'ci: esqueleto del workflow'
git push -u origin ci/workflow-de-build-y-tests
gh pr create --title '…' --body '… Closes #12'      <span class="cm"># ← en la DESCRIPCIÓN</span>
gh pr merge 16 --squash --delete-branch

<span class="cm"># ── Verificación ─────────────────────────────────────────────────</span>
gh issue view 12 --json state    <span class="cm"># CLOSED</span>
gh issue view 11 --json state    <span class="cm"># OPEN — la historia sigue abierta</span>
gh api graphql -f query='{ … subIssuesSummary … }'   <span class="cm"># 1/2 (50%)</span>

<span class="cm"># ── Cerrar el práctico ───────────────────────────────────────────</span>
git tag -a v3.0.0 -m "TP3 cerrado" && git push origin v3.0.0</pre>
</section>

</body></html>''')

out = REPO / "informes" / "TP3-informe.html"
out.write_text("".join(P), encoding="utf-8")
print("HTML escrito:", out.name, "%.0f KB" % (out.stat().st_size / 1024))
