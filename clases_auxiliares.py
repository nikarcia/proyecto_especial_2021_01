import matplotlib.pyplot as plt

class habito:
    caracteristica = ""
    tiempo = 0
    porcentaje = ""
    N_conexiones=""
    promedio=""

    def __init__(self, caracteristica, cantidad, porcentaje , N_conexiones,promedio):
        self.caracteristica = caracteristica
        self.cantidad = cantidad
        self.porcentaje = porcentaje
        self.N_conexiones = N_conexiones
        self.promedio = promedio


class tipo_habito:
    tipo=""
    duracion=0
    def __init__(self, tipo, duracion):
        self.tipo = tipo
        self.duracion = duracion


class conexion_comun:
    inicio=""
    fin=""
    duracion=""
    conexion1=""
    conexion2=""

    def __init__(self, inicio, fin, duracion , conexion1,conexion2):
        self.inicio = inicio
        self.fin = fin
        self.duracion = duracion
        self.conexion1 = conexion1
        self.conexion2 = conexion2

class conexiones_comun_por_estudiante:
    id_estudiante=""
    tiempo_conectado_estudiante=""
    tiempo_conectado_amigo=""
    porcentaje=""
    lista_conexion_comun=[]
    tiempo_total=""
    N_conexiones=""
    promedio=""
    afinidad=""
    frecuenciaXuso = []
    frecuenciaXdia_semana = []
    frecuenciaXap_group = []
    frecuenciaXplace = []
    def __init__(self, id_estudiante, lista_conexion_comun ,tiempo_conectado_total , tiempo_conectado_estudiante ):
        self.id_estudiante = id_estudiante
        self.lista_conexion_comun = lista_conexion_comun
        self.tiempo_total=self.calcular_tiempo_total()
        self.tiempo_conectado_estudiante=tiempo_conectado_total
        self.tiempo_conectado_amigo=tiempo_conectado_estudiante
        self.porcentaje=self.tiempo_total/self.tiempo_conectado_amigo *100
        self.N_conexiones=len(self.lista_conexion_comun)
        self.promedio=self.tiempo_total/self.N_conexiones
        self.frecuenciaXuso = self.calcular_frecuencia("uso")
        self.frecuenciaXplace = self.calcular_frecuencia("place")
        self.frecuenciaXap_group = self.calcular_frecuencia("ap_group")
        self.frecuenciaXdia_semana = self.calcular_frecuencia("dia_semana")

    def calcular_frecuencia(self , tipo):
        tiempo_total_conexion=0
        habitos = []
        aux_tipo_habito=[]
        for i in self.lista_conexion_comun:
            tiempo_total_conexion+=i.duracion.seconds/60
            if tipo=="uso":
                aux_tipo_habito.append(tipo_habito(i.conexion2.uso,i.duracion.seconds/60))
            elif tipo=="place":
                aux_tipo_habito.append(tipo_habito(i.conexion2.place, i.duracion.seconds/60))
            elif tipo=="dia_semana":
                aux_tipo_habito.append(tipo_habito(i.conexion2.dia_semana, i.duracion.seconds/60))
            elif tipo=="ap_group":
                aux_tipo_habito.append(tipo_habito(i.conexion2.ap_group, i.duracion.seconds/60))
            else:
                aux_tipo_habito.append(tipo_habito(i.place, i.duracion.seconds/60))
        for i in aux_tipo_habito:
            existe_habito = False
            for j in habitos:
                if i.tipo == j.caracteristica:
                    existe_habito = True
                    j.tiempo += i.duracion
                    j.porcentaje = j.tiempo / tiempo_total_conexion * 100
                    #print("--------------",j.porcentaje , j.tiempo , self.tiempo_conectado_amigo )
                    j.N_conexiones+=1
                    j.promedio=j.tiempo/j.N_conexiones
            if existe_habito == False:
                if tiempo_total_conexion == 0 :
                    tiempo_total_conexion=1
                nuevo_habito=habito(i.tipo, i.duracion, i.duracion / tiempo_total_conexion * 100 , 1 , i.duracion)
                habitos.append(nuevo_habito)
        habitos = sorted(habitos, key=lambda objeto: objeto.porcentaje , reverse=True)
        return habitos

    def print_frecuencia(self, habito):
        print(habito.caracteristica, habito.cantidad, habito.porcentaje ,habito.N_conexiones ,habito.promedio)

    def print_frecuenciaXuso(self ):
        frecuencia =[]
        nombres =[]
        print("----------------------------------------------------------------------frecuenciaXuso estudiante : ", self.id_estudiante)
        for i in self.frecuenciaXuso:
            print(i.caracteristica ,"   tiempo_conexion:", i.tiempo ,"  porcentaje",i.porcentaje , "N_conexiones"  , i.N_conexiones , "promedio", i.promedio )
            nombres.append(i.caracteristica)
            frecuencia.append(i.porcentaje)
        plt.pie(frecuencia, labels=nombres, autopct="%0.1f %%")
        plt.axis("equal")
        plt.savefig(self.id_estudiante+"_frecuenciaXuso.jpg")
        plt.close()

    def print_frecuenciaXplace(self ):
        frecuencia =[]
        nombres =[]
        print("----------------------------------------------------------------------frecuenciaXplace estudiante : ", self.id_estudiante)
        for i in self.frecuenciaXplace:
            print(i.caracteristica ,"   tiempo_conexion:", i.tiempo ,"  porcentaje",i.porcentaje , "N_conexiones"  , i.N_conexiones , "promedio", i.promedio )
            nombres.append(i.caracteristica)
            frecuencia.append(i.porcentaje)
        plt.pie(frecuencia, labels=nombres, autopct="%0.1f %%")
        plt.axis("equal")
        plt.savefig(self.id_estudiante+"frecuenciaXplace.jpg")
        plt.close()

    def print_frecuenciaXap_group(self):
        frecuencia = []
        nombres = []
        print("----------------------------------------------------------------------frecuenciaXap_group estudiante : ",
              self.id_estudiante)
        for i in self.frecuenciaXap_group:
            print(i.caracteristica, "   tiempo_conexion:", i.tiempo, "  porcentaje", i.porcentaje, "N_conexiones",
                  i.N_conexiones, "promedio", i.promedio)
            nombres.append(i.caracteristica)
            frecuencia.append(i.porcentaje)
        plt.pie(frecuencia, labels=nombres, autopct="%0.1f %%")
        plt.axis("equal")
        plt.savefig(self.id_estudiante+"frecuenciaXap_group.jpg")
        plt.close()

    def print_frecuenciaXdia_semana(self):
        frecuencia = []
        nombres = []
        print("----------------------------------------------------------------------frecuenciaXdia_semana estudiante : ",
              self.id_estudiante)
        for i in self.frecuenciaXdia_semana:
            print(i.caracteristica, "   tiempo_conexion:", i.tiempo, "  porcentaje", i.porcentaje, "N_conexiones",
                  i.N_conexiones, "promedio", i.promedio)
            nombres.append(i.caracteristica)
            frecuencia.append(i.porcentaje)
        plt.pie(frecuencia, labels=nombres, autopct="%0.1f %%")
        plt.axis("equal")
        plt.savefig(self.id_estudiante+"frecuenciaXdia_semana.jpg")
        plt.close()

    def calcular_tiempo_total(self):
        tiempo=0
        for i in self.lista_conexion_comun:
            tiempo+=i.duracion.seconds/60
        return tiempo






class materias_comun:
    id_estudiante=""
    cantidad=""
    lista_materias=[]
    def __init__(self, id_estudiante, lista_materias):
        self.id_estudiante = id_estudiante
        self.lista_materias = lista_materias
        self.cantidad = len(lista_materias)



class asistencia:
    Nclase=""
    materia=""
    conexion=""
    clase=""
    asistio=""
    def __init__(self,Nclase ,materia, conexion, clase, asistio):
        self.Nclase = Nclase
        self.materia = materia
        self.conexion = conexion
        self.clase = clase
        self.asistio = asistio

class porcentaje_asistencia:
    Nclase=""
    materia=""
    frecuencia_asistio=""
    frecuencia_no_asistio=""
    porcentaje=""
    def __init__(self,Nclase ,materia, frecuencia_asistio, frecuencia_no_asistio, porcentaje):
        self.Nclase = Nclase
        self.materia = materia
        self.frecuencia_asistio = frecuencia_asistio
        self.frecuencia_no_asistio = frecuencia_no_asistio
        self.porcentaje = porcentaje