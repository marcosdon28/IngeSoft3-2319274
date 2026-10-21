# Lo que sale por output se imprime en la consola: sólo direcciones y nombres,
# nunca la cadena de conexión (lleva la contraseña del rol).
output "api_url" {
  value = render_web_service.api.url
}

output "front_url" {
  value = render_web_service.front.url
}

output "db_host" {
  value = neon_project.preprod.database_host
}

output "database" {
  value = neon_database.preprod.name
}
