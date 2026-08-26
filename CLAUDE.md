# Reglas de trabajo — IngeSoft3-2319274

Repositorio del semestre de **Ingeniería del Software 3 (UCC 2026)**. Un solo repo para los nueve
trabajos prácticos y el Integrador: cada TP agrega una capa sobre el mismo artefacto.

Enunciados: <https://github.com/ingsoft3ucc/TPs_2026> (clonado en `../TPs_2026`).

---

## 1. Todo cambio entra por Pull Request

`main` está protegida (TP1 §4.4) con `enforce_admins`, así que la regla alcanza también al dueño del
repo. No hay push directo a `main` — la única excepción fue el commit inicial, hecho antes de
configurar la protección.

- Ramas: `feature/<descripcion>` para funcionalidad, `fix/<descripcion>` para correcciones,
  `docs/<descripcion>` para documentación, `ci/<descripcion>` para pipeline.
- Merge: **squash**, un commit por PR. La rama se borra después del merge.
- Cero aprobaciones obligatorias: GitHub nunca deja aprobar el PR propio, y el trabajo es individual.

## 2. Los cuatro archivos se actualizan EN EL MOMENTO

No al final del TP. El reglamento avisa que el historial de Git muestra *cuándo* se trabajó, y un
`decisiones.md` escrito la noche anterior a la defensa se nota.

| Archivo | ¿Se commitea? | Qué lleva y cuándo se toca |
|---|---|---|
| `decisiones.md` | ✅ sí | Cada decisión técnica **con su porqué**, cada problema y cómo se resolvió, y la declaración de uso de IA. Se **acumula** con un `## TPn — …` por trabajo práctico: nunca se reescribe ni se borra lo anterior |
| `evidencias.md` | ✅ sí | Cada captura 📸 con una línea que explique qué se está viendo. Se actualiza apenas se saca la captura (las imágenes van en `img/`) |
| `aprendizajes.md` | ❌ **local** | Qué se aprendió, qué hace cada comando, qué confundió y cómo se entendió |
| `notas-defensa-p1.md` | ❌ **local** | Las preguntas de ejemplo de cada enunciado, con la respuesta armada |

**Los dos locales se ignoran vía `.git/info/exclude`**, no vía `.gitignore`. Diferencia:
`.gitignore` se versiona y viaja a quien clone el repo; `.git/info/exclude` es el ignore **privado
de este clon** y no sale de esta máquina — que es exactamente lo que se quiere para notas
personales.

> ⚠️ `.git/info/exclude` **no se clona**. Si este repo se clona en otra máquina, hay que volver a
> agregar estas dos líneas:
> ```bash
> printf 'aprendizajes.md\nnotas-defensa-p1.md\n' >> .git/info/exclude
> ```

## 3. Cada TP se cierra con su tag y su release

`TP1 → v1.0.0`, `TP2 → v2.0.0`, … El tag marca el commit exacto que se mira de cada TP. Si un TP ya
etiquetado se corrige después, se mueve el tag (`git tag -f vN.0.0 && git push -f origin vN.0.0`) y
**se declara el movimiento en `decisiones.md`**.

## 4. Uso de IA

Permitido y alentado por la cátedra (reglamento §6), con tres condiciones **innegociables**:
declararlo en `decisiones.md`, verificar lo que produjo, y poder defenderlo. Si en la defensa no se
puede explicar una decisión que tomó la IA, ese punto no se aprueba.

Por eso: **nada entra al repo sin que se entienda qué hace y por qué**. Cuando se resuelve algo con
asistencia, se anota en `decisiones.md` qué parte fue asistida y **cómo se verificó**.

## 5. Secretos

Jamás se commitean. Van en `.env` (ignorado) con un `.env.example` commiteado que documente qué
variables hacen falta, sin valores reales. Desde el TP4 migran a los secrets de la plataforma de CI.

---

## Stack de la app del semestre (desde el TP2)

Inventario de productos — **FastAPI + React/Vite + PostgreSQL**, organizado en MVC:

| Capa | Implementación |
|---|---|
| Model | SQLAlchemy (`backend/models/`) + Pydantic (`backend/schemas/`) |
| Controller | `backend/routers/` (endpoints) + `backend/services/` (reglas de negocio) |
| View | React + Vite; llama a `/api/...` con **ruta relativa** (proxy de Vite en dev, nginx en contenedor) |

La conexión a la base se lee **siempre** de la variable de entorno `DATABASE_URL`, nunca hardcodeada:
es lo que permite que la misma imagen corra en local, QA y producción (TP6).
