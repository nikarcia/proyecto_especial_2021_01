import DB as r
import conexion as c
import clases_auxiliares as ca
from datetime import datetime
import diccionario_usoXplace as d
import matplotlib.pyplot as plt
import grupos_estudiantes as ge
from datetime import timedelta

tiempo_conexion_minimo=5
intervalo_entre_conexiones=15

class estudiante:
    id = ""
    carrera = ""
    conexiones = []
    materias = []
    lista_registros_conexion = []
    frecuenciaXuso=[]
    frecuenciaXdia_semana = []
    frecuenciaXap_group = []
    frecuenciaXclient_device_type = []
    frecuenciaXplace = []
    lista_asistencia=[]
    conexiones_comun_por_estudiante=[]
    tiempo_conectado=""
    tiempo_conectado_con_otros=""


    def __init__(self, id, carrera , fecha_inicio,fecha_fin ):
        self.id = id
        self.carrera = carrera
        self.calcular_registros_conexion_rango(fecha_inicio, fecha_fin)
        self.calcular_conexiones()
        self.frecuenciaXuso = self.calcular_frecuencia("uso")
        self.frecuenciaXplace = self.calcular_frecuencia("place")
        self.frecuenciaXap_group = self.calcular_frecuencia("ap_group")
        self.frecuenciaXdia_semana = self.calcular_frecuencia("dia_semana")
        self.frecuenciaXclient_device_type = self.calcular_frecuencia("client_device_type")
        self.tiempo_conectado=self.calcular_tiempo_conectado()
        self.tiempo_conectado_con_otros=self.calcular_tiempo_conectado_otros()

    def calcular_tiempo_conectado(self):
        tiempo_conectado=0
        for i in self.conexiones:
            tiempo_conectado+=i.duracion
        return tiempo_conectado

    def calcular_tiempo_conectado_otros(self):
        tiempo=0
        for j in self.conexiones_comun_por_estudiante:
            tiempo= tiempo + j.tiempo_total
            print(j.id_estudiante , j.tiempo_total)

        return tiempo

    def calcular_registros_conexion_rango(self , fecha_inicio , fecha_fin):
        self.lista_registros_conexion.clear()
        for registro in r.registros_por_estudiante(self.id):
            if registro.id_estudiante == self.id:
                inicio = fecha_inicio.split('/')
                fin = fecha_fin.split('/')
                inicio_date = datetime(int(inicio[2]), int(inicio[1]), int(inicio[0]), 23, 59, 59, 00000)
                fin_date = datetime(int(fin[2]), int(fin[1]), int(fin[0]), 23, 59, 59, 00000)
                if registro.fecha >= inicio_date and registro.fecha <= fin_date:
                    self.lista_registros_conexion.append(registro)
        self.lista_registros_conexion = sorted(self.lista_registros_conexion, key=lambda objeto: objeto.fecha)

    def print_registros(self ):
        print("--------------------------------------------------------------------------------",len(self.lista_registros_conexion),"registros conexion estudiante" , self.id )
        for registro in self.lista_registros_conexion:
            self.print_registro(registro)

    def print_registro(self, registro):
        print("     " , registro.id_estudiante, registro.fecha, registro.hora, registro.ap_group, registro.client_device_type,
              registro.place , registro.duracion)

    def calcular_conexiones(self ):
        self.conexiones.clear()
        i = 0
        while i < len(self.lista_registros_conexion):
            registros_por_conexion=[]
            actual = self.lista_registros_conexion[i]
            registros_por_conexion.append(actual)
            j=i+1
            duracion = 0
            while j < len(self.lista_registros_conexion):
                actual = self.lista_registros_conexion[j-1]
                siguiente = self.lista_registros_conexion[j]
                diferencia = (siguiente.fecha - actual.fecha).seconds / 60
                if actual.place == siguiente.place and actual.fecha.day == siguiente.fecha.day and diferencia <=intervalo_entre_conexiones:
                    registros_por_conexion.append(siguiente)
                    duracion+=diferencia
                else:
                    duracion+=tiempo_conexion_minimo
                    primera=registros_por_conexion[0]
                    ultima=registros_por_conexion[len(registros_por_conexion)-1]
                    self.conexiones.append(c.conexion(primera.id_estudiante, primera.fecha, ultima.fecha + timedelta(minutes=tiempo_conexion_minimo), primera.ap_group, primera.client_device_type, primera.place ,duracion ,d.uso(primera.place) ,registros_por_conexion ))
                    i=j-1
                    break
                if j == len(self.lista_registros_conexion) - 1:
                    i = j
                    break
                j+=1
            i += 1
        self.conexiones = sorted(self.conexiones, key=lambda objeto: objeto.fecha_inicio)

    def print_conexiones(self):
        N_conexiones=len(self.conexiones)
        print("------------------------------------------------------------------------------------------",N_conexiones,"---conexiones estudiante " , self.id)
        for i in self.conexiones:
            print("-------------------------------------------------------")
            self.print_conexion(i)
            for j in i.registros:
               self.print_registro(j)

    def print_conexion(self , conexion):
        print(conexion.id_estudiante, conexion.dia_semana, conexion.fecha_inicio, conexion.fecha_fin, conexion.ap_group, conexion.client_device_type, conexion.place ,conexion.duracion , conexion.uso , conexion.N_registros)


    def calcular_frecuencia(self , tipo):
        tiempo_total_conexion=0
        habitos = []
        tipo_habito=[]
        for i in self.conexiones:
            tiempo_total_conexion+=i.duracion
            if tipo=="uso":
                tipo_habito.append(ca.tipo_habito(i.uso,i.duracion))
            elif tipo=="place":
                tipo_habito.append(ca.tipo_habito(i.place, i.duracion))
            elif tipo=="dia_semana":
                tipo_habito.append(ca.tipo_habito(i.dia_semana, i.duracion))
            elif tipo=="ap_group":
                tipo_habito.append(ca.tipo_habito(i.ap_group, i.duracion))
            elif tipo=="client_device_type":
                tipo_habito.append(ca.tipo_habito(i.client_device_type, i.duracion))
            else:
                tipo_habito.append(ca.tipo_habito(i.place, i.duracion))
        for i in tipo_habito:
            existe_habito = False
            for j in habitos:
                if i.tipo == j.caracteristica:
                    existe_habito = True
                    j.tiempo += i.duracion
                    j.porcentaje = j.tiempo / tiempo_total_conexion * 100
                    j.N_conexiones+=1
                    j.promedio=j.tiempo/j.N_conexiones
            if existe_habito == False:
                nuevo_habito=ca.habito(i.tipo, i.duracion, i.duracion / tiempo_total_conexion * 100 , 1 , i.duracion)
                habitos.append(nuevo_habito)
        habitos = sorted(habitos, key=lambda objeto: objeto.porcentaje , reverse=True)
        return habitos

    def print_frecuencia(self, habito):
        print(habito.caracteristica, habito.cantidad, habito.porcentaje ,habito.N_conexiones ,habito.promedio)

    def print_frecuenciaXuso(self ):
        frecuencia =[]
        nombres =[]
        print("-------------------------------frecuenciaXuso estudiante : ", self.id , "tiempo_total" , self.tiempo_conectado)
        for i in self.frecuenciaXuso:
            print(i.caracteristica ,"   tiempo_conexion:", i.tiempo ,"  porcentaje",i.porcentaje , "N_conexiones"  , i.N_conexiones , "promedio", i.promedio )
            nombres.append(i.caracteristica)
            frecuencia.append(i.porcentaje)
        plt.pie(frecuencia, labels=nombres, autopct="%0.1f %%")
        plt.axis("equal")
        plt.savefig(self.id+"_frecuenciaXuso.jpg")
        plt.close()

    def print_frecuenciaXplace(self ):
        import matplotlib.pyplot as plt
        frecuencia =[]
        nombres =[]
        print("----------------------------------------------------------------------frecuenciaXplace estudiante : ", "tiempo_total" , self.tiempo_conectado)
        for i in self.frecuenciaXplace:
            print(i.caracteristica ,"   tiempo_conexion:", i.tiempo ,"  porcentaje",i.porcentaje , "N_conexiones"  , i.N_conexiones , "promedio", i.promedio )
            nombres.append(i.caracteristica)
            frecuencia.append(i.porcentaje)
        plt.pie(frecuencia, labels=nombres, autopct="%0.1f %%")
        plt.axis("equal")
        plt.savefig(self.id+"frecuenciaXplace.jpg")
        plt.close()

    def print_frecuenciaXap_group(self):
        import matplotlib.pyplot as plt
        frecuencia = []
        nombres = []
        print("----------------------------------------------------------------------frecuenciaXap_group estudiante : ",
              self.id, "tiempo_total" , self.tiempo_conectado)
        for i in self.frecuenciaXap_group:
            print(i.caracteristica, "   tiempo_conexion:", i.tiempo, "  porcentaje", i.porcentaje, "N_conexiones",
                  i.N_conexiones, "promedio", i.promedio)
            nombres.append(i.caracteristica)
            frecuencia.append(i.porcentaje)
        plt.pie(frecuencia, labels=nombres, autopct="%0.1f %%")
        plt.axis("equal")
        plt.savefig(self.id+"frecuenciaXap_group.jpg")
        plt.close()

    def print_frecuenciaXdia_semana(self):
        import matplotlib.pyplot as plt
        frecuencia = []
        nombres = []
        print("----------------------------------------------------------------------frecuenciaXdia_semana estudiante : ",
              self.id, "tiempo_total" , self.tiempo_conectado)
        for i in self.frecuenciaXdia_semana:
            print(i.caracteristica, "   tiempo_conexion:", i.tiempo, "  porcentaje", i.porcentaje, "N_conexiones",
                  i.N_conexiones, "promedio", i.promedio)
            nombres.append(i.caracteristica)
            frecuencia.append(i.porcentaje)
        plt.pie(frecuencia, labels=nombres, autopct="%0.1f %%")
        plt.axis("equal")
        plt.savefig(self.id+"frecuenciaXdia_semana.jpg")
        plt.close()

    def print_frecuenciaXclient_device_type(self):
        import matplotlib.pyplot as plt
        frecuencia = []
        nombres = []
        print("----------------------------------------------------------------------client_device_type estudiante : ",
              self.id, "tiempo_total" , self.tiempo_conectado)
        for i in self.frecuenciaXclient_device_type:
            print(i.caracteristica, "   tiempo_conexion:", i.tiempo, "  porcentaje", i.porcentaje, "N_conexiones",
                  i.N_conexiones, "promedio", i.promedio)
            nombres.append(i.caracteristica)
            frecuencia.append(i.porcentaje)
        plt.pie(frecuencia, labels=nombres, autopct="%0.1f %%")
        plt.axis("equal")
        plt.savefig(self.id+"frecuenciaXclient_device_type.jpg")
        plt.close()

    def print_conexiones_comun(self):

        for i in self.conexiones_comun_por_estudiante:
            print("####################################################", i.id_estudiante,self.id,
                  "#############################################################3")
            print("tiempo total conectado", i.id_estudiante,i.tiempo_conectado_estudiante)
            print("tiempo total conectado", self.id, i.tiempo_conectado_amigo)
            print("tiempo conectado comun", i.tiempo_total)
            print("N_conexiones", i.N_conexiones)
            print("promedio", i.promedio)
            print("% " ,self.id, i.tiempo_total/i.tiempo_conectado_amigo *100)
            print("% ", i.id_estudiante, i.tiempo_total/i.tiempo_conectado_estudiante*100)
            for j in i.lista_conexion_comun:
                ge.print_conexion_comun(j)
            i.print_frecuenciaXuso()
            #i.print_frecuenciaXplace()
            #i.print_frecuenciaXap_group()
            #i.print_frecuenciaXdia_semana()

    def print_tiempo_total_tiempo_por_amigo(self):
        estudiantes=[]
        porcentaje=[]
        porcentaje_amigo=[]
        for i in self.conexiones_comun_por_estudiante:
            print("############################################# tiempo total ",i.id_estudiante,self.id,)
            print("tiempo total ", i.id_estudiante, i.tiempo_conectado_estudiante)
            print("tiempo total ", self.id, i.tiempo_conectado_amigo)
            print("tiempo conectado comun", i.tiempo_total)
            print("porcentaje" , i.porcentaje)
            print("N_conexiones", i.N_conexiones)
            print("promedio", i.promedio)
            estudiantes.append(i.id_estudiante.replace('Estudiante',''))
            porcentaje.append(round(i.porcentaje,2))
            porcentaje_amigo.append(round(i.tiempo_total/i.tiempo_conectado_estudiante*100, 2))
        import numpy as np
        asistencia =   estudiantes
        men_means =   porcentaje
        women_means =   porcentaje_amigo
        # Obtenemos la posicion de cada etiqueta en el eje de X
        x = np.arange(len(asistencia))
        # tamaño de cada barra
        width = 0.35
        fig, ax = plt.subplots()
        # Generamos las barras para el conjunto de hombres
        rects1 = ax.bar(x - width / 2, men_means, width, label=self.id)
        # Generamos las barras para el conjunto de mujeres
        rects2 = ax.bar(x + width / 2, women_means, width, label='Amigo')
        # Añadimos las etiquetas de identificacion de valores en el grafico
        ax.set_ylabel('porcentaje tiempo ')
        ax.set_title('Estudiantes')
        ax.set_xticks(x)
        ax.set_xticklabels(asistencia)
        # Añadimos un legen() esto permite mmostrar con colores a que pertence cada valor.
        ax.legend()
        def autolabel(rects):
            """Funcion para agregar una etiqueta con el valor en cada barra"""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')
        # Añadimos las etiquetas para cada barra
        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        plt.savefig('tiempo_total_tiempo_por_amigo'+self.id+'barras.png')
        # Mostramos la grafica con el metodo show()

        #grafico pastel
        fig1, ax1 = plt.subplots()
        # Creamos el grafico, añadiendo los valores
        ax1.pie(porcentaje, labels=estudiantes, autopct='%1.1f%%',
                shadow=True, startangle=90)
        # señalamos la forma, en este caso 'equal' es para dar forma circular
        ax1.axis('equal')
        plt.title('porcentaje tiempo ' + self.id)
        plt.legend()
        plt.savefig('tiempo_total_tiempo_por_amigo'+self.id+'pastel.png')
        plt.show()

    def print_tiempo_amigos_tiempo_por_amigo(self):
        estudiantes=[]
        porcentaje=[]
        porcentaje_amigo=[]
        tiempo_con_amigos=0
        for i in self.conexiones_comun_por_estudiante:
            tiempo_con_amigos+=i.tiempo_total
        for i in self.conexiones_comun_por_estudiante:
            print("############################################# tiempo con amigos ",i.id_estudiante,self.id,)
            print("tiempo con amigos ", self.id, tiempo_con_amigos)
            #print("tiempo con amigos ", self.id, i.tiempo_conectado_amigo)
            print("tiempo conectado comun", i.tiempo_total)
            print("N_conexiones", i.N_conexiones)
            print("promedio", i.promedio)
            estudiantes.append(i.id_estudiante.replace('Estudiante', ''))
            porcentaje.append(round(i.tiempo_total / tiempo_con_amigos * 100, 2))
            porcentaje_amigo.append(round(0 / tiempo_con_amigos * 100, 2))
        import numpy as np
        asistencia = estudiantes
        men_means = porcentaje
        women_means = porcentaje_amigo
        # Obtenemos la posicion de cada etiqueta en el eje de X
        x = np.arange(len(asistencia))
        # tamaño de cada barra
        width = 0.35
        fig, ax = plt.subplots()
        # Generamos las barras para el conjunto de hombres
        rects1 = ax.bar(x - width / 2, men_means, width, label=self.id)
        # Generamos las barras para el conjunto de mujeres
        rects2 = ax.bar(x + width / 2, women_means, width, label='Amigo')
        # Añadimos las etiquetas de identificacion de valores en el grafico
        ax.set_ylabel('porcentaje tiempo ')
        ax.set_title('Estudiantes')
        ax.set_xticks(x)
        ax.set_xticklabels(asistencia)
        # Añadimos un legen() esto permite mmostrar con colores a que pertence cada valor.
        ax.legend()

        def autolabel(rects):
            """Funcion para agregar una etiqueta con el valor en cada barra"""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        # Añadimos las etiquetas para cada barra
        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        plt.savefig('tiempo_amigos_tiempo_por_amigo'+self.id+'barras.png')
        # Mostramos la grafica con el metodo show()

        # grafico pastel
        fig1, ax1 = plt.subplots()
        # Creamos el grafico, añadiendo los valores
        ax1.pie(porcentaje, labels=estudiantes, autopct='%1.1f%%',
                shadow=True, startangle=90)
        # señalamos la forma, en este caso 'equal' es para dar forma circular
        ax1.axis('equal')
        plt.title('porcentaje tiempo ' + self.id)
        plt.legend()
        plt.savefig('tiempo_amigos_tiempo_por_amigo'+self.id+'pastel.png')
        plt.show()

    def print_tiempo_uso_tiempo_por_amigo(self):
        estudiantes=[]
        usos=[]
        data2=[]
        usos.append('Estudiante')
        for j in self.conexiones_comun_por_estudiante:
            if (j.id_estudiante in estudiantes) == False:
                estudiantes.append(j.id_estudiante)
            for k in j.frecuenciaXuso:
                for i in self.frecuenciaXuso:
                    if k.caracteristica == i.caracteristica:
                        if (i.caracteristica in usos) == False:
                            usos.append(i.caracteristica)
        for j in self.conexiones_comun_por_estudiante:
            vector=[]
            print("---------", j.id_estudiante)
            vector.append(j.id_estudiante.replace('Estudiante ',''))
            for u in usos:
                existe=False
                for k in j.frecuenciaXuso:
                    for i in self.frecuenciaXuso:
                        if k.caracteristica == i.caracteristica and k.caracteristica==u:
                            print("        ", k.caracteristica, "   tiempo_conexion:", k.tiempo, "  porcentaje",
                                  k.porcentaje,
                                  "N_conexiones",
                                  k.N_conexiones, "promedio", k.promedio)
                            print("        ", i.caracteristica, "   tiempo_conexion:", i.tiempo, "  porcentaje",
                                  i.porcentaje,
                                  "N_conexiones", i.N_conexiones, "promedio", i.promedio)
                            aux=k.tiempo
                            aux2=i.tiempo
                            if aux==0:
                                aux=1
                            if aux2==0:
                                aux2=1
                            print(aux,aux2,(aux/aux2)*100)

                            vector.append((aux/aux2)*100)
                            existe=True
                if existe==False and u != 'Estudiante':
                    vector.append(0)
            print(vector)
            aux=vector
            data2.append(aux)
        print(usos)
        print(data2)

        import pandas as pd
        import matplotlib.pyplot as plt

        df = pd.DataFrame(data2, columns=usos)
        df.plot(x=usos.pop(0), y=usos, kind="bar", figsize=(9, 8))
        plt.show()

    def print_tiempo_place_tiempo_por_amigo(self):
        estudiantes=[]
        usos=[]
        data2=[]
        usos.append('Estudiante')
        for j in self.conexiones_comun_por_estudiante:
            if (j.id_estudiante in estudiantes) == False:
                estudiantes.append(j.id_estudiante)
            for k in j.frecuenciaXplace:
                for i in self.frecuenciaXplace:
                    if k.caracteristica == i.caracteristica:
                        if (i.caracteristica in usos) == False:
                            usos.append(i.caracteristica)
        for j in self.conexiones_comun_por_estudiante:
            vector=[]
            print("---------", j.id_estudiante)
            vector.append(j.id_estudiante.replace('Estudiante ',''))
            for u in usos:
                existe=False
                for k in j.frecuenciaXplace:
                    for i in self.frecuenciaXplace:
                        if k.caracteristica == i.caracteristica and k.caracteristica==u:
                            print("        ", k.caracteristica, "   tiempo_conexion:", k.tiempo, "  porcentaje",
                                  k.porcentaje,
                                  "N_conexiones",
                                  k.N_conexiones, "promedio", k.promedio)
                            print("        ", i.caracteristica, "   tiempo_conexion:", i.tiempo, "  porcentaje",
                                  i.porcentaje,
                                  "N_conexiones", i.N_conexiones, "promedio", i.promedio)
                            aux=k.tiempo
                            aux2=i.tiempo
                            if aux==0:
                                aux=1
                            if aux2==0:
                                aux2=1
                            print(aux,aux2,(aux/aux2)*100)

                            vector.append((aux/aux2)*100)
                            existe=True
                if existe==False and u != 'Estudiante':
                    vector.append(0)
            print(vector)
            aux=vector
            data2.append(aux)
        print(usos)
        print(data2)

        import pandas as pd
        import matplotlib.pyplot as plt

        df = pd.DataFrame(data2, columns=usos)
        df.plot(x=usos.pop(0), y=usos, kind="bar", figsize=(9, 8))
        plt.show()

    def print_tiempo_dia_tiempo_por_amigo(self):
        estudiantes=[]
        usos=[]
        data2=[]
        usos.append('Estudiante')
        for j in self.conexiones_comun_por_estudiante:
            if (j.id_estudiante in estudiantes) == False:
                estudiantes.append(j.id_estudiante)
            for k in j.frecuenciaXdia_semana:
                for i in self.frecuenciaXdia_semana:
                    if k.caracteristica == i.caracteristica:
                        if (i.caracteristica in usos) == False:
                            usos.append(i.caracteristica)
        for j in self.conexiones_comun_por_estudiante:
            vector=[]
            print("---------", j.id_estudiante)
            vector.append(j.id_estudiante.replace('Estudiante ',''))
            for u in usos:
                existe=False
                for k in j.frecuenciaXdia_semana:
                    for i in self.frecuenciaXdia_semana:
                        if k.caracteristica == i.caracteristica and k.caracteristica==u:
                            print("        ", k.caracteristica, "   tiempo_conexion:", k.tiempo, "  porcentaje",
                                  k.porcentaje,
                                  "N_conexiones",
                                  k.N_conexiones, "promedio", k.promedio)
                            print("        ", i.caracteristica, "   tiempo_conexion:", i.tiempo, "  porcentaje",
                                  i.porcentaje,
                                  "N_conexiones", i.N_conexiones, "promedio", i.promedio)
                            aux=k.tiempo
                            aux2=i.tiempo
                            if aux==0:
                                aux=1
                            if aux2==0:
                                aux2=1
                            print(aux,aux2,(aux/aux2)*100)

                            vector.append((aux/aux2)*100)
                            existe=True
                if existe==False and u != 'Estudiante':
                    vector.append(0)
            print(vector)
            aux=vector
            data2.append(aux)
        print(usos)
        print(data2)

        import pandas as pd
        import matplotlib.pyplot as plt

        df = pd.DataFrame(data2, columns=usos)
        df.plot(x=usos.pop(0), y=usos, kind="bar", figsize=(9, 8))
        plt.show()




    def print_porcentaje_asistencia_clase(self):
        import matplotlib.pyplot as plt
        import numpy as np
        asistencia = []
        men_means = []
        women_means = []
        res=""

        print("-------------------------------------------porcentaje asistencia a clase del estudiante  : ", self.id)
        res+="                                            porcentaje asistencia a clase del estudiante  : "+ self.id + "\n"
        for i in self.porcentaje_asistencia_clase():
            print(i.Nclase,i.materia,"%asistencia:" ,i.porcentaje,"         asistio:", i.frecuencia_asistio, " no_asistio:",i.frecuencia_asistio )
            res+=i.Nclase + " " + i.materia +"%asistencia:"  +str(i.porcentaje) + "         asistio: "+ str( i.frecuencia_asistio )+ " no_asistio:"+str(i.frecuencia_asistio) + "\n"
            asistencia.append(i.Nclase + " " + i.materia)
            men_means.append(i.porcentaje)
            women_means.append(100-i.porcentaje)
        # Obtenemos la posicion de cada etiqueta en el eje de X
        x = np.arange(len(asistencia))
        # tamaño de cada barra
        width = 0.35
        fig, ax = plt.subplots()
        # Generamos las barras para el conjunto de hombres
        rects1 = ax.bar(x - width / 2, men_means, width, label='asistio')
        # Generamos las barras para el conjunto de mujeres
        rects2 = ax.bar(x + width / 2, women_means, width, label='No asistio')
        # Añadimos las etiquetas de identificacion de valores en el grafico
        ax.set_ylabel('porcentaje asistencia')
        ax.set_title('porcentaje asistencia a clase')
        ax.set_xticks(x)
        ax.set_xticklabels(asistencia)
        # Añadimos un legen() esto permite mmostrar con colores a que pertence cada valor.
        ax.legend()

        def autolabel(rects):
            """Funcion para agregar una etiqueta con el valor en cada barra"""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2, height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        # Añadimos las etiquetas para cada barra
        autolabel(rects1)
        autolabel(rects2)
        fig.tight_layout()
        plt.savefig('porcentaje_asistencia_clase.png')
        # Mostramos la grafica con el metodo show()
        #plt.show()
        return res

    def asistencias(self):
        asistencias=[]
        for conexion in self.conexiones:
            for materia in self.materias:
                    for clase in materia.clases:
                        if conexion.dia_semana == clase.dia:
                            if conexion.hora >= clase.hora_inicio and conexion.hora <= clase.hora_fin:
                                if conexion.ap == clase.aula:
                                    asistencias.append(asistencia(materia.Nclase , materia.nombre , conexion,clase,True))
                                else:
                                    asistencias.append(asistencia(materia.Nclase , materia.nombre , conexion,clase,False))
        return asistencias

    def print_asistencias(self):
        print("---------------------------------------------conexiones en horario de clase del estudiante : ", self.id)
        for asistencia in self.asistencias():
            print(asistencia.asistio ,
                  asistencia.conexion.ano,
                  asistencia.conexion.mes,
                  asistencia.conexion.dia,
                  asistencia.Nclase,
                  asistencia.materia,
                  asistencia.clase.dia,
                  asistencia.clase.hora_inicio,
                  asistencia.clase.hora_fin,
                  asistencia.clase.aula)

    def porcentaje_asistencia_clase(self):
        lista_porcentajes_asistencia=[]
        for asistencia in self.asistencias():
            existe_materia = False
            for lista in lista_porcentajes_asistencia:
                if asistencia.Nclase == lista.Nclase:
                    existe_materia = True
                    if asistencia.asistio:
                        lista.frecuencia_asistio=lista.frecuencia_asistio+1
                        lista.porcentaje=(lista.frecuencia_asistio/(lista.frecuencia_asistio+lista.frecuencia_no_asistio))*100
                    else:
                        lista.frecuencia_no_asistio=lista.frecuencia_no_asistio+1
                        lista.porcentaje = (lista.frecuencia_asistio / (lista.frecuencia_asistio + lista.frecuencia_no_asistio)) * 100

            if existe_materia == False:
                if asistencia.asistio:
                    lista_porcentajes_asistencia.append(porcentaje_asistencia(asistencia.Nclase , asistencia.materia , 1 , 0 , 100 ))
                else:
                    lista_porcentajes_asistencia.append(porcentaje_asistencia(asistencia.Nclase, asistencia.materia, 0, 1, 0))
        return lista_porcentajes_asistencia


















    def generar_reporte(self):
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        habitos=self.print_habitos().split(sep="\n")
        asistencia=self.print_porcentaje_asistencia_clase().split(sep="\n")

        canvas = canvas.Canvas("reporte.pdf", pagesize= letter)
        canvas.setLineWidth(.3)
        canvas.setFont('Helvetica', 12)

        canvas.drawString(30, 770, habitos[0])
        canvas.drawImage("habitos.jpg",  70, 480, width=440, height=280)

        canvas.line(0, 480, 580, 480)

        canvas.drawString(30, 460, asistencia[0])
        canvas.drawImage("porcentaje_asistencia_clase.png", 70, 170, width=440, height=280)

        #canvas.drawString(30, 750, habitos[0])
        #canvas.drawString(30, 735, 'RICARDOGEEK.COM')
        #canvas.drawString(500, 750, "27/10/2016")
        #canvas.line(480, 747, 580, 747)

        #canvas.drawString(275, 725, 'ESTIMADO:')
        #canvas.drawString(500, 725, "<NOMBRE>")
        #canvas.line(378, 723, 580, 723)

        #canvas.drawString(30, 703, 'ETIQUETA:')
        #canvas.line(120, 700, 580, 700)
        #canvas.drawString(120, 703, "<ASUNTO DE LA CARTA GENERICO>")

        canvas.save()

