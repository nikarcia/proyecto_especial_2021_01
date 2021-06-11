import pandas as pd

class conexion:
    id_estudiante = ""
    fecha_inicio=""
    fecha_fin = ""
    dia_semana=""
    ap_group = ""
    client_device_type = ""
    place = ""
    duracion = ""
    uso=""
    registros=[]
    N_registros=""

    def __init__(self,id_estudiante, fecha_inicio, fecha_fin, ap_group, client_device_type, place ,duracion , uso , registros):
        self.id_estudiante = id_estudiante
        self.fecha_inicio = fecha_inicio
        self.fecha_fin = fecha_fin
        self.ap_group = ap_group
        self.client_device_type = client_device_type
        self.place = place
        self.duracion = duracion
        self.uso=uso
        self.dia_semana = self.calcular_dia_semana()
        self.registros = registros
        self.N_registros=len(self.registros)


    def calcular_dia_semana(self):
        dia= pd.Timestamp(self.fecha_inicio).dayofweek
        if dia==0:
            return "lunes"
        if dia==1:
            return "martes"
        if dia==2:
            return "miercoles"
        if dia==3:
            return "jueves"
        if dia==4:
            return "viernes"
        if dia==5:
            return "sabado"
        if dia==6:
            return "domingo"
