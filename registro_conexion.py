from datetime import datetime
class registro_conexion:
    id_estudiante=""
    fecha=""
    hora=""
    ap_group=""
    client_device_type=""
    place=""
    programa=""
    duracion=5

    def __init__(self, id_estudiante, fecha, hora, place , ap_group, client_device_type, programa):
        self.id_estudiante = id_estudiante
        self.fecha = fecha
        self.hora = hora
        self.ap_group = ap_group
        self.client_device_type = client_device_type
        self.place=place
        self.programa = programa
