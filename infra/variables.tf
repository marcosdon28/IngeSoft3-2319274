# Nada de esto es secreto: el nombre de una imagen pública, una etiqueta, una
# región, el id de una organización. Por eso van con `default` en un archivo
# que SÍ se commitea. Lo que no se publica va en *.tfvars (ignorados) o en el
# entorno (las API keys).

variable "neon_org_id" {
  description = "Organización de Neon donde nace el proyecto de preprod (la API lo exige)."
  default     = "org-little-scene-51474302"
}

variable "image_repo_api" {
  description = "Imagen del backend, SIN etiqueta."
  default     = "ghcr.io/marcosdon28/inventario-backend"
}

variable "image_repo_front" {
  description = "Imagen del frontend, SIN etiqueta."
  default     = "ghcr.io/marcosdon28/inventario-frontend"
}

variable "image_tag" {
  description = "La etiqueta sha-<commit> de un merge del TP7 que el pipeline publicó. Preprod corre ESA imagen: para cambiarla se edita esta línea por PR, y Render free no actualiza servicios: destroy + apply (o apply -replace)."
  default     = "sha-304025231bd3a76378f29b4817292291d520134c"
}

variable "region" {
  description = "Región de Render: frankfurt | ohio | oregon | singapore | virginia."
  default     = "oregon"
}
