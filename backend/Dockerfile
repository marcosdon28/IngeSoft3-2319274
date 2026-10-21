# ---- Etapa 1: build (imagen completa: trae compilador y herramientas) ----
# Las dependencias se instalan en un virtualenv aparte, que es lo único que
# después viaja a la etapa final.
FROM python:3.12 AS build
WORKDIR /app
ENV PIP_NO_CACHE_DIR=1

# El archivo de dependencias PRIMERO y la instalación después: esta capa sólo se
# rehace si cambia requirements.txt, así que tocar código no re-descarga nada.
COPY requirements.txt .
RUN python -m venv /opt/venv \
 && /opt/venv/bin/pip install --upgrade pip \
 && /opt/venv/bin/pip install -r requirements.txt

# ---- Etapa 2: tests (parte del build: ya tiene el venv con las dependencias) ----
# Hereda de `build`: mismo código fuente y mismas dependencias que se compilaron.
# Agrega SÓLO las herramientas de test (pytest, pytest-cov), que la imagen final
# nunca se lleva. No corre durante el `docker build`: corre en el `docker run`
# del pipeline, que monta /out para sacar el reporte afuera.
FROM build AS test
COPY requirements-dev.txt .
RUN /opt/venv/bin/pip install -r requirements-dev.txt
ENV PATH="/opt/venv/bin:$PATH"
COPY .coveragerc .
COPY app ./app
COPY tests ./tests
# El umbral que FRENA el build (--cov-fail-under) vive acá: una sola receta para
# la máquina local y el pipeline. Se mide línea y rama; el umbral mira las dos.
ENTRYPOINT ["pytest", "--cov=app", "--cov-branch", "--cov-fail-under=85", \
            "--cov-report=term-missing", \
            "--cov-report=xml:/out/coverage.xml", \
            "--cov-report=html:/out/htmlcov", \
            "--junitxml=/out/tests.xml"]

# ---- Etapa 3: runtime (imagen mínima, sin compilador ni pip cache) ----
FROM python:3.12-slim AS final
WORKDIR /app

# Linkea la imagen publicada con este repositorio en la pestaña Packages.
LABEL org.opencontainers.image.source=https://github.com/marcosdon28/IngeSoft3-2319274

# Sólo el virtualenv ya resuelto. Nada de las herramientas de compilación.
COPY --from=build /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# El código va último: es lo que más cambia, así invalida la menor cantidad de capas.
COPY app ./app

# Usuario sin privilegios: si alguien escapa del proceso, no es root.
RUN useradd --create-home --uid 1001 appuser
USER appuser

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
