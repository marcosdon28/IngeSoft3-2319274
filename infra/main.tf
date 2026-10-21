# Infraestructura como código — TP8.
#
# Declara un entorno NUEVO, `preprod`, completo: su base de datos (un proyecto
# propio de Neon) y sus dos servicios de Render ejecutando la imagen del TP7.
# QA y producción NO se tocan: se crearon a mano (por API) en el TP6 y viven
# fuera de este código. Preprod nace con `terraform apply` y muere con
# `terraform destroy`, sin rozar a los otros dos.

terraform {
  required_version = ">= 1.5"

  required_providers {
    # Los dos providers FIJADOS por versión: sin esto, un día `init` baja otra
    # cosa y el archivo que ayer andaba deja de compilar. El de Neon lo mantiene
    # una persona (repositorio archivado); el oficial de Neon todavía no existe
    # con otro `source`: migrar cuando salga es, justamente, un ejercicio de IaC.
    neon = {
      source  = "kislerdm/neon"
      version = "0.18.0"
    }
    render = {
      source  = "render-oss/render"
      version = "1.9.1"
    }
  }
}

# Las credenciales NO están acá: los providers las leen del entorno.
#   NEON_API_KEY · RENDER_API_KEY · RENDER_OWNER_ID
provider "neon" {}
provider "render" {}

# Sin bloque `backend`: el estado vive en infra/terraform.tfstate, en esta
# máquina, cubierto por el .gitignore. Alcanza porque el que aplica soy yo.

# --- La base de datos de PREPROD: un proyecto de Neon que no existe hasta que esto se aplica ---

resource "neon_project" "preprod" {
  name   = "inventario-preprod"
  org_id = var.neon_org_id

  # El plan gratuito admite hasta 21600 s (6 h) de historial; el default del
  # provider pide 86400 y el primer apply falla con un error que no dice qué hacer.
  history_retention_seconds = 21600
}

resource "neon_role" "preprod" {
  project_id = neon_project.preprod.id
  branch_id  = neon_project.preprod.default_branch_id # default_branch_id, NO branch_id
  name       = "app_preprod_owner"
}

resource "neon_database" "preprod" {
  project_id = neon_project.preprod.id
  branch_id  = neon_project.preprod.default_branch_id
  name       = "app_preprod"
  owner_name = neon_role.preprod.name
}

# --- Los dos servicios de PREPROD en Render, ejecutando la IMAGEN del TP7 ---

locals {
  # La cadena de conexión se ARMA acá, con lo que devolvió Neon (host, base,
  # rol y la contraseña que generó). Nadie la copia y pega: ése era el error
  # más caro del TP6, un entorno apuntando a la base de otro. Es el formato que
  # lee app/config.py (DATABASE_URL, driver psycopg 3).
  database_url = "postgresql+psycopg://${neon_role.preprod.name}:${neon_role.preprod.password}@${neon_project.preprod.database_host}/${neon_database.preprod.name}?sslmode=require"
}

resource "render_web_service" "api" {
  name   = "inventario-api-preprod"
  plan   = "free"
  region = var.region

  runtime_source = {
    image = {
      image_url = var.image_repo_api # SIN la etiqueta: la etiqueta va en `tag`
      tag       = var.image_tag
    }
  }

  env_vars = {
    DATABASE_URL = { value = local.database_url }
    # NO va APP_COMMIT: lo hornea el pipeline en la imagen (ARG). Una variable
    # del servicio lo pisaría y /health dejaría de decir qué imagen corre.
  }
}

resource "render_web_service" "front" {
  name   = "inventario-front-preprod"
  plan   = "free"
  region = var.region

  runtime_source = {
    image = {
      image_url = var.image_repo_front
      tag       = var.image_tag
    }
  }

  env_vars = {
    # La dirección de SU api sale del atributo `url` del recurso, no de un
    # copy-paste; sin barra final (con barra, nginx manda todo a `/`: 404).
    BACKEND_URL  = { value = trimsuffix(render_web_service.api.url, "/") }
    DNS_RESOLVER = { value = "8.8.8.8" }
  }
}
