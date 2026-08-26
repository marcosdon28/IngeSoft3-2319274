#!/usr/bin/env python3
"""Genera informes/TP2-informe.html embebiendo las capturas de img/ en base64.

Después, para producir el PDF:
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    --headless --disable-gpu --no-pdf-header-footer \
    --print-to-pdf=informes/TP2-informe.pdf file://$PWD/informes/TP2-informe.html
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
A("<title>TP2 — Contenedores</title><style>" + CSS + "</style></head><body>")

A('''<section class="cover">
  <div class="materia">Ingeniería del Software 3 · UCC 2026</div>
  <div class="tp">Trabajo Práctico 02</div>
  <div class="sub">Contenedores: la app del semestre</div>
  <div class="rule"></div>
  <table>
    <tr><td>Alumno</td><td>Marcos Don</td></tr>
    <tr><td>Matrícula</td><td>2319274</td></tr>
    <tr><td>Repositorio</td><td>github.com/marcosdon28/IngeSoft3-2319274</td></tr>
    <tr><td>Aplicación</td><td>Inventario de productos</td></tr>
    <tr><td>Stack</td><td>FastAPI + React/Vite + PostgreSQL</td></tr>
    <tr><td>Imágenes</td><td>ghcr.io/marcosdon28/inventario-{backend,frontend}:v0.1.0</td></tr>
    <tr><td>Versión entregada</td><td>v2.0.0</td></tr>
    <tr><td>Fecha</td><td>''' + FECHA + '''</td></tr>
  </table>
</section>''')

A('''<section class="pb">
<h2>1. Objetivo y qué se evalúa</h2>
<p>Contenerizar la aplicación que va a acompañar toda la materia: Dockerfiles multi-etapa para
backend y frontend, orquestación completa con compose, e imágenes publicadas en un registry. El
escenario del enunciado lo resume bien: dejar el proyecto en un estado donde <strong>cualquiera que
clone el repositorio levante el sistema completo con un comando</strong>, y donde las imágenes estén
publicadas para que otros entornos las consuman.</p>
<table>
  <tr><th>Requisito</th><th>Estado</th></tr>
  <tr><td>App full-stack (front + back + base) corriendo, justificada en <code>decisiones.md</code></td><td>✔ Inventario de productos, elegida contra los 5 criterios</td></tr>
  <tr><td>Dockerfile multi-stage para back y front, cada uno con su <code>.dockerignore</code></td><td>✔ 1,62 GB → 326 MB y 229 MB → 93 MB</td></tr>
  <tr><td><code>nginx.conf</code> con el proxy hacia el backend</td><td>✔ con <code>resolver</code> y <code>proxy_pass</code> por variable</td></tr>
  <tr><td>Compose con volumen, red por nombre, <code>depends_on</code> + <code>healthcheck</code>, secreto por <code>.env</code></td><td>✔</td></tr>
  <tr><td>Imágenes en registry gratuito, tag semver, visibilidad pública</td><td>✔ ghcr.io, <code>v0.1.0</code>, públicas</td></tr>
  <tr><td><code>docker-compose.registry.yml</code> probado de verdad</td><td>✔ probado deslogueado</td></tr>
  <tr><td><code>README.md</code> con los pasos de arranque desde cero</td><td>✔</td></tr>
</table>
<div class="callout"><strong>La guía se hace dos veces.</strong> Primero sobre el sample de la
cátedra —para practicar, y eso no se entrega— y después sobre la app propia, que es lo que se
defiende. Hice las dos, en ese orden, y la §4 de este informe cuenta qué me dejó la primera.</div>
</section>''')

A('''<section>
<h2>2. La aplicación elegida</h2>
<p><strong>Un sistema de inventario de productos</strong>, escrito por mí: FastAPI (Python 3.12) +
React/Vite + PostgreSQL 16. La escribí en vez de adoptar un proyecto de GitHub porque el quinto
criterio de la guía de selección —<em>entenderla lo suficiente para modificarla en vivo</em>— se
cumple de verdad sólo cuando el código es propio: en la mesa del Integrador hay que hacer un cambio
delante del profesor.</p>
<table>
  <tr><th>Criterio de <code>elegir-app.md</code></th><th>Cómo lo cumple</th></tr>
  <tr><td>1. Que corra hoy</td><td><code>cp .env.example .env &amp;&amp; docker compose up -d --build</code>. No necesita Python, Node ni PostgreSQL instalados</td></tr>
  <tr><td>2. Conocer los comandos de build</td><td><code>pip install -r requirements.txt</code> + <code>uvicorn</code>; <code>npm ci</code> + <code>npm run build</code>. Son las líneas de los Dockerfiles</td></tr>
  <tr><td>3. Dónde se configura la base</td><td>En <strong>una</strong> variable: <code>DATABASE_URL</code>, leída en <code>app/config.py</code>. Nunca hardcodeada</td></tr>
  <tr><td>4. Lógica para testear</td><td><strong>7 reglas de negocio</strong> con casos válidos, inválidos y de borde — el TP5 pide 8 tests de back y 4 de front</td></tr>
  <tr><td>5. Entenderla para modificarla</td><td>Código propio, en capas explícitas</td></tr>
</table>
<p><strong>Tamaño</strong>: cuatro pantallas y tres entidades. La guía avisa que más grande no suma
nota — sólo builds más lentos y más puntos de falla.</p>
<h3>Las 7 reglas de negocio</h3>
<table>
  <tr><th>#</th><th>Regla</th><th>Por qué existe</th></tr>
  <tr><td>1</td><td>Una salida no puede superar el stock disponible</td><td>El stock son unidades físicas: nunca puede quedar negativo</td></tr>
  <tr><td>2</td><td>El SKU es único</td><td>Dos productos con el mismo SKU hacen imposible saber cuál se movió</td></tr>
  <tr><td>3</td><td>No se puede eliminar una categoría con productos</td><td>Evita productos huérfanos; borrar en cascada destruiría datos sin avisar</td></tr>
  <tr><td>4</td><td>Precio y stock no negativos; cantidad &gt; 0</td><td>Validación de dominio en el borde de entrada</td></tr>
  <tr><td>5</td><td>Descuento por cantidad desde un umbral</td><td>Cálculo con bordes — el umbral es <strong>inclusive</strong></td></tr>
  <tr><td>6</td><td><code>stock &lt;= stock_minimo</code> marca bajo stock</td><td>Propiedad <strong>derivada</strong>, no columna: no puede desincronizarse</td></tr>
  <tr><td>7</td><td>Un producto inactivo no admite movimientos</td><td>Si igual se le cargan movimientos, la baja es decorativa</td></tr>
</table>
<div class="callout"><strong>Un caso de borde que apareció al probar la regla 5:</strong> con umbral
en 10 unidades y 10 % de descuento, <strong>llevar 9 cuesta lo mismo que llevar 10</strong>
(9 × 1800 = 16.200 y 10 × 1800 × 0,9 = 16.200). No es un error —es lo que la regla dice— pero es
exactamente el tipo de cosa que un test de borde expone y una lectura del código no.</div>
</section>''')

A('''<section class="pb">
<h2>3. Arquitectura: MVC en FastAPI</h2>
<table>
  <tr><th>Capa</th><th>Dónde vive</th><th>Qué sabe</th></tr>
  <tr><td>Model</td><td><code>app/models/</code> (SQLAlchemy) + <code>app/schemas/</code> (Pydantic)</td><td>Las entidades, su persistencia y el contrato de la API</td></tr>
  <tr><td>Controller</td><td><code>app/routers/</code> + <code>app/services/</code></td><td>Los routers traducen HTTP; los <strong>services tienen las reglas</strong></td></tr>
  <tr><td>View</td><td><code>frontend/src/</code></td><td>Presentación; las reglas de la vista aisladas en <code>lib/reglas.js</code></td></tr>
</table>
<p>La decisión que más importa de todo el diseño: <strong>los <code>services/</code> no importan
FastAPI</strong>. Lanzan excepciones propias (<code>ReglaDeNegocioError</code>) y los routers las
traducen a códigos HTTP. Gracias a eso una regla se testea llamando a una función, sin levantar un
servidor — que es exactamente lo que va a necesitar el TP5. Lo mismo del lado del frontend:
<code>lib/reglas.js</code> son funciones puras, sin React ni <code>fetch</code> adentro.</p>
<pre>backend/app/
  models/      SQLAlchemy: Categoria, Producto, Movimiento
  schemas/     Pydantic: el contrato de entrada y salida
  services/    <span class="cm">← las 7 reglas viven acá, sin HTTP</span>
  routers/     los endpoints: traducen HTTP a llamadas a services
  config.py    DATABASE_URL y los parámetros del descuento, del entorno</pre>
</section>''')

A('''<section>
<h2>4. La primera pasada: el sample de la cátedra</h2>
<p>Antes de tocar mi app hice la guía completa sobre <code>demo-fullstack</code> (.NET 8 + React +
PostgreSQL), que es lo que el enunciado pide y que en su momento parece una pérdida de tiempo. No lo
fue: los tres problemas que me frenaron ahí volvieron a aparecer en mi app, y la segunda vez ya sabía
qué eran.</p>
<h3>Lo que me dejó</h3>
<ul>
  <li><strong>La diferencia SDK / runtime, con números.</strong> La imagen que compila
  (<code>dotnet/sdk:8.0</code>) pesa <strong>1,25 GB</strong>; la que sólo ejecuta
  (<code>dotnet/aspnet:8.0</code>), 350 MB. Ver esos dos números al lado explica el multi-stage mejor
  que cualquier definición.</li>
  <li><strong>El 502 del frontend sin red compartida.</strong> Con el contenedor del front y el del
  back corriendo por separado, <code>curl localhost:3000/api/tareas</code> devuelve
  <strong>502</strong>: existen los dos, pero no se conocen — el nombre <code>backend</code> del
  <code>nginx.conf</code> no resuelve. Eso es exactamente el problema que resuelve compose, y verlo
  fallar primero hace que el <code>docker-compose.yml</code> deje de ser magia.</li>
  <li><strong>El orden <code>Waiting → Healthy → Starting</code></strong> en la salida de compose:
  la diferencia entre "el contenedor arrancó" y "el servicio está listo", que es lo que separa
  <code>depends_on</code> a secas de <code>depends_on</code> + <code>healthcheck</code>.</li>
</ul>
<div class="callout"><strong>Un obstáculo que no era de Docker:</strong> el sample es .NET y yo no
tenía el SDK. <code>brew install --cask dotnet-sdk</code> pide contraseña de administrador; lo
resolví con el script oficial <code>dot.net/v1/dotnet-install.sh --channel 8.0</code>, que instala en
<code>~/.dotnet</code> sin privilegios. Detalle que conviene entender: para <em>construir la
imagen</em> el SDK local no hace falta —vive dentro del contenedor— pero sí para el paso de correr la
app nativa antes de contenerizarla.</div>
</section>''')

A('''<section class="pb">
<h2>5. Los Dockerfiles multi-etapa</h2>
<h3>Backend</h3>
<pre><span class="cm"># ---- Etapa 1: build (imagen completa: compilador y herramientas) ----</span>
FROM python:3.12 AS build
COPY requirements.txt .                  <span class="cm"># las dependencias PRIMERO…</span>
RUN python -m venv /opt/venv \\
 &amp;&amp; /opt/venv/bin/pip install -r requirements.txt

<span class="cm"># ---- Etapa 2: runtime (mínima, sin compilador ni cache de pip) ----</span>
FROM python:3.12-slim AS final
COPY --from=build /opt/venv /opt/venv    <span class="cm"># sólo el venv ya resuelto</span>
ENV PATH="/opt/venv/bin:$PATH"
COPY app ./app                           <span class="cm"># …y el código ÚLTIMO</span>
RUN useradd --create-home --uid 1001 appuser
USER appuser                             <span class="cm"># no corre como root</span>
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]</pre>
<p>Dos reglas de oro, las dos visibles ahí: <strong>el archivo de dependencias se copia antes que el
código</strong>, porque cuando una capa cambia Docker invalida esa capa y todas las siguientes — con
este orden, tocar una línea de código no vuelve a instalar nada; y <strong>el SDK no viaja a
producción</strong>: la etapa final sólo recibe el virtualenv ya resuelto.</p>
<h3>Frontend</h3>
<p>Mismo patrón con otro argumento, todavía más claro: una SPA compilada son <strong>archivos
estáticos</strong>. Node compila en la primera etapa y no aparece en la segunda, donde sólo hay nginx
y los archivos de <code>dist/</code>.</p>''' + fig("tp2-06-tamanos-imagenes.png",
    "Los tamaños medidos, no estimados. Sin multi-stage la imagen del backend pesaría 1,62 GB en vez "
    "de 326 MB — y viajaría a producción con un compilador adentro, que es superficie de ataque que "
    "no hace falta.") + '''
<div class="callout"><strong>Los <code>.dockerignore</code> son dos, no uno.</strong> Docker los busca
en el <strong>contexto</strong> que se le pasa (<code>./backend</code> y <code>./frontend</code>), no
en la raíz del repositorio. Y tienen contenidos distintos: el del backend excluye
<code>__pycache__/</code> y <code>.venv/</code>; el del frontend, <code>node_modules/</code> —
que no es opcional, porque si no se excluye, el <code>COPY . .</code> pisa los módulos que
<code>npm ci</code> acaba de instalar para Linux con los de la máquina local.</div>
</section>''')

A('''<section class="pb">
<h2>6. Cómo se hablan los tres servicios</h2>
<p>Tres ámbitos distintos, y confundirlos explica casi todos los problemas de red de este práctico.</p>
<table>
  <tr><th>Camino</th><th>Cómo se resuelve</th></tr>
  <tr><td><strong>backend → db</strong></td><td>Por el <strong>nombre del servicio</strong> (<code>@db:5432</code>). Compose crea una red interna con DNS embebido: no importa en qué IP cayó la base</td></tr>
  <tr><td><strong>host → backend</strong></td><td>Sólo por los puertos publicados (<code>8000:8000</code>). La base <strong>no publica ninguno</strong>: no es accesible desde afuera</td></tr>
  <tr><td><strong>browser → backend</strong></td><td>El caso trampa: el JavaScript de la SPA <strong>corre en el browser</strong>, que vive en mi máquina y no en la red de compose. <code>http://backend:8000</code> no resolvería nunca</td></tr>
</table>
<p>Para el tercero elegí la solución (a) de la guía: la SPA llama a <strong>rutas relativas</strong>
(<code>/api/...</code>), y quien las traduce es el servidor de Vite en desarrollo y <strong>nginx</strong>
en el contenedor. Dos consecuencias, y las dos importan más adelante: la <strong>misma imagen sirve
en cualquier entorno</strong> porque no tiene ninguna URL compilada adentro (eso es lo que va a hacer
posible el TP6), y como para el browser todo sale del mismo origen, <strong>no hay CORS que
configurar</strong>.</p>
<pre>location /api/ {
    resolver 127.0.0.11 valid=10s ipv6=off;   <span class="cm"># el DNS de Docker</span>
    set $backend_api http://backend:8000;     <span class="cm"># ← el nombre en una VARIABLE</span>
    proxy_pass $backend_api;                  <span class="cm"># ← y SIN barra al final</span>
}</pre>
<p>Los dos detalles del bloque parecen de más y no lo son. <strong>El nombre va en una variable</strong>
porque con el nombre escrito directo nginx lo resuelve <em>al arrancar</em> y, si el backend todavía
no existe, se niega a levantar con <code>host not found in upstream</code> — o sea que el contenedor
del frontend no podría correr solo. Y el <strong><code>proxy_pass</code> va sin barra final</strong>:
con barra, nginx reescribe el prefijo y manda <code>/api/productos</code> a <code>/productos</code>,
con lo que la API devuelve 404 en todas las llamadas.</p>
</section>''')

A('''<section class="pb">
<h2>7. El sistema completo con un comando</h2>''' + fig("tp2-08-compose-up.png",
    "Arranque desde cero, empezando por <code>down -v</code> para no arrastrar estado. En el medio se "
    "ve <code>db Waiting → db Healthy → backend Starting</code>: el backend no arranca hasta que "
    "PostgreSQL acepta conexiones.") + '''
<h3>Por qué <code>depends_on</code> no alcanza</h3>
<p><code>depends_on</code> garantiza el orden de <strong>arranque</strong>, no de
<strong>disponibilidad</strong>. Que el contenedor de PostgreSQL haya arrancado no significa que
acepte conexiones — hay varios segundos entre una cosa y la otra, y en ese hueco el backend se
conecta, falla y se muere. Por eso el servicio <code>db</code> declara un <code>healthcheck</code>
con <code>pg_isready</code> y el backend espera con <code>condition: service_healthy</code>.</p>
<p>La distinción "arrancó" contra "está listo" reaparece en cada sistema distribuido que uno toque.</p>
<h3>Los secretos</h3>
<p>La contraseña de la base sale de <code>${DB_PASSWORD}</code>, que vive en un <code>.env</code>
<strong>que no se commitea</strong>. Lo que sí se versiona es <code>.env.example</code>, que documenta
qué variables hacen falta sin traer ningún valor real. Por eso el arranque son <strong>dos comandos y
no uno</strong> — y eso no es un defecto de la entrega: es el precio de que el secreto no viaje en el
repositorio. En el TP4 esos secretos migran a los secrets de la plataforma de CI.</p>
</section>''')

A('''<section class="pb">
<h2>8. La aplicación funcionando</h2>''' + fig("tp2-01-app-resumen.png",
    "El tablero con datos reales de PostgreSQL. «Bajo stock: 2» en rojo es la regla 6: la lista se "
    "calcula desde el stock actual, no de una columna guardada, así que no puede quedar "
    "desincronizada.") + fig("tp2-04-app-movimientos.png",
    "La regla 5 visible: la salida de 10 unidades lleva 10 % de descuento y la de 9 no. Arriba, el "
    "botón deshabilitado con el motivo escrito — las reglas 1, 4 y 7 evaluadas en vivo.") + '''
<p>La validación de la interfaz es <strong>comodidad, no seguridad</strong>: el backend rechaza igual
cada operación inválida, con un 400 y el motivo. Las dos capas dicen lo mismo porque las dos leen la
misma regla, no porque estén duplicadas a mano — en el front vive en <code>lib/reglas.js</code>, en
el back en <code>services/</code>.</p>''' + fig("tp2-03-app-categorias.png",
    "La regla 3 reflejada en la vista: el botón <em>Eliminar</em> está deshabilitado cuando la "
    "categoría tiene productos asociados.") + '''
</section>''')

A('''<section class="pb">
<h2>9. Persistencia: qué sobrevive y qué no</h2>
<p>Los contenedores son <strong>efímeros por diseño</strong>: la capa de escritura muere con el
contenedor. Eso es una ventaja para la aplicación —contenedores descartables ⇒ deploys y rollbacks
triviales— y una catástrofe para los datos. La solución es separar el estado explícitamente: el
directorio de datos de PostgreSQL vive en el volumen <strong>nombrado</strong>
<code>db_data</code>.</p>''' + fig("tp2-07-persistencia.png",
    "Los stocks antes y después. <code>down</code> destruye los contenedores y los datos siguen; "
    "<code>down -v</code> se lleva también el volumen y la lista vuelve vacía.") + '''
<table>
  <tr><th></th><th>Cómo se escribe</th><th>Dónde viven los datos</th><th>Cuándo usarlo</th></tr>
  <tr><td><strong>Volumen nombrado</strong></td><td><code>db_data:/var/lib/postgresql/data</code></td><td>En un área que administra Docker (en Mac, dentro de su VM)</td><td><strong>Bases de datos</strong> — es lo que usa este TP</td></tr>
  <tr><td><strong>Bind mount</strong></td><td><code>./datos:/var/lib/postgresql/data</code></td><td>En una carpeta mía, que puedo abrir</td><td>Meter código o configuración, ver cambios en vivo</td></tr>
</table>
<p>La diferencia visual es un carácter: si lo de la izquierda empieza con <code>./</code> es una ruta;
si es una palabra suelta, es un volumen de Docker. Para la base va volumen nombrado: en Mac hay una
máquina virtual en el medio, así que un bind mount del directorio de datos de PostgreSQL es
notablemente más lento y da problemas de permisos.</p>
<p><code>down</code> apaga; <code>down -v</code> además <strong>olvida</strong>.</p>
</section>''')

A('''<section class="pb">
<h2>10. Publicar en el registry</h2>
<p>Un <strong>registry</strong> es a las imágenes lo que GitHub es al código. Publiqué en
<strong>GitHub Container Registry</strong> (ghcr.io): la cuenta ya existe —es la del TP1—, las
imágenes quedan junto al código, y en el TP7 el pipeline va a poder autenticarse contra ghcr
<strong>sin secretos</strong>, usando el <code>GITHUB_TOKEN</code> del propio workflow.</p>
<pre>gh auth refresh -h github.com -s write:packages   <span class="cm"># el scope no venía del TP1</span>
gh auth token | docker login ghcr.io -u marcosdon28 --password-stdin
docker tag  ingesoft3-2319274-backend ghcr.io/marcosdon28/inventario-backend:v0.1.0
docker push ghcr.io/marcosdon28/inventario-backend:v0.1.0</pre>
<div class="callout"><strong>El <code>docker login</code> miente.</strong> Da
<code>Login Succeeded</code> con cualquier token válido, tenga o no permiso sobre packages — y recién
falla el <code>push</code>, con <code>denied</code>. La única comprobación real de la credencial es
empujar algo.</div>''' + fig("tp2-11-package-backend.png",
    "El package con la etiqueta <strong>Public</strong>, el tag semver <code>v0.1.0</code> y el "
    "comando exacto para bajarlo. Los packages de ghcr <strong>nacen privados</strong>: hubo que "
    "cambiarles la visibilidad una por una.") + '''
<h3>La prueba de verdad: bajarlas sin credenciales</h3>
<p>Decir que una imagen está pública es fácil. La prueba es bajarla estando deslogueado — y para que
la prueba signifique algo hay que borrar antes <strong>las tres copias locales</strong>, porque
Docker no guarda imágenes sino <strong>capas identificadas por su contenido</strong>.</p>''' +
    fig("tp2-09-registry-pull.png",
    "Las tres limpiezas y después el pull anónimo. El <code>builder prune</code> es el que nadie ve "
    "venir: acá liberó 40 GB de capas guardadas. Al final, el sistema completo levantado desde el "
    "registry — en el <code>ps</code> la columna IMAGE dice <code>ghcr.io/…</code>, no un nombre "
    "local.") + '''
<div class="callout"><strong>Una advertencia honesta sobre arquitecturas.</strong> Estas imágenes se
construyeron en una Mac con chip ARM, y lo verifiqué en vez de suponerlo:
<code>docker manifest inspect</code> devuelve una sola plataforma real, <code>linux/arm64</code> (el
<code>unknown/unknown</code> que aparece al lado es el manifiesto de atestación de BuildKit, no una
arquitectura). Alguien con Intel/AMD recibiría <code>no matching manifest for linux/amd64</code> — y
<strong>los runners de GitHub Actions son Intel</strong>, así que esto va a reaparecer en el TP7,
donde se resuelve con <code>docker buildx</code>.</div>
</section>''')

A('''<section class="pb">
<h2>11. Problemas encontrados y aprendizajes</h2>
<h3><code>npm ci</code> falló en el build: no había lockfile</h3>
<p>Escribí el <code>package.json</code> a mano y fui directo al <code>docker build</code>, sin haber
corrido nunca <code>npm install</code>. <code>npm ci</code> <strong>exige</strong> el
<code>package-lock.json</code> — es justamente lo que lo hace reproducible, y por eso es el comando
correcto para un build de contenedor. Se resolvió generando el lockfile y commiteándolo, que es donde
tiene que estar.</p>
<h3><code>docker images</code> no mostraba las imágenes base</h3>
<p>Docker 29 guarda las imágenes base de las etapas de build en el <strong>cache de
construcción</strong>, no en el store de imágenes, así que el comando de comparación de la guía
devolvía la tabla vacía. No estaba roto: hay que bajarlas explícitamente con <code>docker pull</code>
para poder compararlas. El mensaje no sugiere nada de esto.</p>
<h3>Los packages de ghcr nacen privados</h3>
<p>Después del <code>push</code>, <code>gh api /user/packages</code> los mostraba como
<code>private</code>. Mientras lo estén nadie puede hacer <code>docker pull</code>: ni la cátedra, ni
otra máquina, ni un pipeline. Hay que cambiar la visibilidad desde la página del package, y hacerlo
<strong>para las dos</strong> imágenes.</p>
<h3>El cache se esconde en tres lugares</h3>
<p>Para probar el pull anónimo hay que borrar: (1) las imágenes que construyó compose
(<code>--rmi local</code>), (2) los nombres que uno les puso (<code>docker rmi</code>), y (3) el
<strong>cache de construcción</strong> (<code>docker builder prune -af</code>). Si se saltea
cualquiera de los tres, el <code>pull</code> contesta <code>Already exists</code> en todas las capas
y no baja nada — y uno cree que probó algo que no probó.</p>

<h2>Declaración de uso de Inteligencia Artificial</h2>
<p>Usé <strong>Claude Code (Claude Opus)</strong>, declarado según el reglamento §6.</p>
<table>
  <tr><th>Qué fue asistido</th><th>Cómo lo verifiqué</th></tr>
  <tr><td>El código de la aplicación</td><td><strong>Probé las 7 reglas contra la API levantada</strong>, una por una, verificando código HTTP y mensaje: SKU duplicado → 400, borrar categoría con productos → 400, salida mayor al stock → 400, cantidad cero → 422, producto inactivo → 400, y el descuento en el borde exacto (9 sin, 10 con)</td></tr>
  <tr><td>Dockerfiles, compose y <code>nginx.conf</code></td><td>Los leí línea por línea y los probé: el sistema levanta con un comando, el front habla con el back por el proxy, y la prueba de persistencia se comporta como esperaba. Los tamaños los <strong>medí</strong></td></tr>
  <tr><td>La publicación en el registry</td><td>La verificación no es que la página diga <em>Public</em>: es que el <code>pull</code> funcione <strong>deslogueado</strong>, y que el sistema levante desde el registry sin compilar nada</td></tr>
  <tr><td>Redacción de <code>decisiones.md</code>, <code>evidencias.md</code> y este informe</td><td>Los revisé para que digan lo que efectivamente pasó. Los problemas listados son los que me pasaron a mí</td></tr>
</table>
<p>Lo que <strong>no</strong> delegué: la elección de la app y su dominio, las 7 reglas de negocio, la
decisión de llamar a la API por ruta relativa en vez de URL absoluta, y qué persiste y qué no.</p>
</section>''')

A('''<section class="pb">
<h2>Anexo — Los comandos, en orden</h2>
<pre><span class="cm"># ── Primera pasada: el sample de la cátedra (no se entrega) ──────</span>
git clone --branch demo-c2-inicio https://github.com/ingsoft3ucc/demo-fullstack.git practica-tp2
curl -fsSL https://dot.net/v1/dotnet-install.sh | bash -s -- --channel 8.0
docker run -d --name pg-tp2 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=app -p 5432:5432 postgres:16-alpine
docker build -t mi-backend:dev ./backend
docker run --rm -d -p 8080:8080 -e ConnectionStrings__Default='Host=host.docker.internal;…' mi-backend:dev
docker compose up -d --build

<span class="cm"># ── Segunda pasada: mi app (esto SÍ se entrega) ──────────────────</span>
cp .env.example .env
docker compose up -d --build
./scripts/datos-demo.sh

<span class="cm"># ── Las 7 reglas, probadas contra la API ─────────────────────────</span>
curl -X POST localhost:8000/api/productos   -d '{"sku":"BEB-001",…}'   <span class="cm"># → 400 SKU duplicado</span>
curl -X DELETE localhost:8000/api/categorias/1                         <span class="cm"># → 400 tiene productos</span>
curl -X POST localhost:8000/api/movimientos -d '{"cantidad":100,…}'    <span class="cm"># → 400 stock insuficiente</span>
curl -X POST localhost:8000/api/movimientos -d '{"cantidad":0,…}'      <span class="cm"># → 422 cantidad &gt; 0</span>

<span class="cm"># ── Persistencia ─────────────────────────────────────────────────</span>
docker compose down    &amp;&amp; docker compose up -d    <span class="cm"># los datos SIGUEN</span>
docker compose down -v &amp;&amp; docker compose up -d    <span class="cm"># la lista vuelve VACÍA</span>

<span class="cm"># ── Registry ─────────────────────────────────────────────────────</span>
gh auth refresh -h github.com -s write:packages
gh auth token | docker login ghcr.io -u marcosdon28 --password-stdin
docker tag  ingesoft3-2319274-backend  ghcr.io/marcosdon28/inventario-backend:v0.1.0
docker push ghcr.io/marcosdon28/inventario-backend:v0.1.0
<span class="cm"># … y hacerlas públicas desde Package settings → Change visibility</span>

<span class="cm"># ── La prueba de verdad: pull sin credenciales ───────────────────</span>
docker compose down --rmi local     <span class="cm"># 1. las imágenes que construyó compose</span>
docker rmi ghcr.io/marcosdon28/inventario-backend:v0.1.0   <span class="cm"># 2. los nombres propios</span>
docker builder prune -af            <span class="cm"># 3. el CACHE DE CONSTRUCCIÓN (liberó 40 GB)</span>
docker logout ghcr.io
docker pull ghcr.io/marcosdon28/inventario-backend:v0.1.0
docker compose -f docker-compose.registry.yml up -d        <span class="cm"># descarga, no construye</span>

<span class="cm"># ── Cerrar el práctico ───────────────────────────────────────────</span>
git tag -a v2.0.0 -m "TP2 cerrado" &amp;&amp; git push origin v2.0.0</pre>
</section>

</body></html>''')

out = REPO / "informes" / "TP2-informe.html"
out.write_text("".join(P), encoding="utf-8")
print("HTML escrito:", out.name, "%.0f KB" % (out.stat().st_size / 1024))
