import estudiante as e
import registro_conexion as r
from datetime import datetime
import csv

def generar_lista_estudiantes(fecha_inicio , fecha_fin):
    lista_estudiantes=[]
    with open('data_muysca_ALL.csv', newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            existe=False
            atributos = row[0].split(";")
            id = atributos[0]
            programa = atributos[13]
            for est in lista_estudiantes:
                if id == est.id:
                    existe=True
            if existe==False and id != "ï»¿id_estudiante":
               lista_estudiantes.append(e.estudiante(id, programa , fecha_inicio ,fecha_fin ))
    return lista_estudiantes



def registros_por_estudiante(id_estudiante):
    lista_registros=[]
    with open('data_muysca_ALL.csv', newline='') as File:
        reader = csv.reader(File)
        for row in reader:
            if row[0].split(";")[0] == id_estudiante  :
                atributos=row[0].split(";")
                id=atributos[0]
                fecha=atributos[1]
                ap_grupal=atributos[5]
                device=atributos[7]
                place=atributos[11]
                programa=atributos[13]
                hora=atributos[18].replace("Â","")
                fecha=calcular_fecha(fecha,hora)
                registro= r.registro_conexion(id,fecha,hora,place,ap_grupal,device,programa)
                lista_registros.append(registro)
    return lista_registros

def calcular_fecha( fecha ,hora):
        fecha = fecha.split("/")
        aux = hora.split(":")
        hora = int(aux[0])
        aux2 = aux[1].split()
        minuto = int(aux2[0])
        am_pm = aux2[1]
        if am_pm == "pm":
            if hora==12:
                hora=12
            else:
                hora+=12
        nueva_fecha=  datetime(int(fecha[2]), int(fecha[1]), int(fecha[0]), hora, minuto, 0, 00000)
        return nueva_fecha

def print_registro( registro):
    print(registro.id_estudiante, registro.fecha, registro.hora, registro.ap_group, registro.client_device_type,
              registro.place , registro.duracion)