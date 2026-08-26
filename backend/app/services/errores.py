class ReglaDeNegocioError(Exception):
    """Una regla de negocio impidió la operación.

    Existe para que los services no dependan de FastAPI: lanzan esto, y la capa
    de routers la traduce a un HTTP 400. Así las reglas se pueden testear sin
    levantar la API (que es lo que va a necesitar el TP5).
    """

    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje


class NoEncontradoError(Exception):
    def __init__(self, mensaje: str):
        super().__init__(mensaje)
        self.mensaje = mensaje
