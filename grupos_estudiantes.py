import clases_auxiliares as ca


def hallar_conexiones_comun_estudiantes(estudiante, lista_estudiantes):
    lista_conexiones_comun_estudiantes=[]
    for est in lista_estudiantes:
        if est.id != estudiante.id:
            lista_aux=hallar_conexion_comun(estudiante , est)
            if len(lista_aux) > 0:
                lista_conexiones_comun_estudiantes.append(ca.conexiones_comun_por_estudiante(est.id , lista_aux , est.tiempo_conectado , estudiante.tiempo_conectado))
    lista_conexiones_comun_estudiantes = sorted(lista_conexiones_comun_estudiantes, key=lambda objeto: objeto.tiempo_total , reverse=True)
    return lista_conexiones_comun_estudiantes


def hallar_conexion_comun(estudiante1 , estudiante2):
    lista_conexiones_comun= []
    for c1 in estudiante1.conexiones:
        for c2 in estudiante2.conexiones:
            hay_conexion_comun=False
            if c1.place == c2.place and c1.fecha_inicio.year == c2.fecha_inicio.year and c1.fecha_inicio.month == c2.fecha_inicio.month and c1.dia_semana == c2.dia_semana and c1.fecha_inicio.day == c2.fecha_inicio.day:
                if c1.fecha_inicio >= c2.fecha_inicio and c1.fecha_inicio <= c2.fecha_fin:
                    inicio=c1.fecha_inicio
                    if c1.fecha_fin <= c2.fecha_fin:
                        fin=c1.fecha_fin
                    elif c1.fecha_fin >= c2.fecha_fin:
                        fin =c2.fecha_fin
                    hay_conexion_comun=True
                if c2.fecha_inicio >= c1.fecha_inicio and c2.fecha_inicio <= c1.fecha_fin:
                    inicio=c2.fecha_inicio
                    if c1.fecha_fin <= c2.fecha_fin:
                        fin = c1.fecha_fin
                    elif c1.fecha_fin >= c2.fecha_fin:
                        fin = c2.fecha_fin
                    hay_conexion_comun = True
            if hay_conexion_comun:
                duracion= fin - inicio
                if duracion==0:
                    duracion=5
                lista_conexiones_comun.append(ca.conexion_comun(inicio, fin, duracion, c1, c2))
    return lista_conexiones_comun

def print_conexion_comun(cm):
    print_conexion(cm.conexion1)
    print_conexion(cm.conexion2)
    print("     ",cm.inicio,cm.fin,cm.duracion)


def print_conexion(conexion):
    print("     ",conexion.id_estudiante, conexion.dia_semana, conexion.fecha_inicio, conexion.fecha_fin, conexion.ap_group,
          conexion.client_device_type, conexion.place, conexion.duracion, conexion.uso, conexion.N_registros)









def encontrar_compañeros(self, lista_estudiantes):
        lista_materias_comun=[]
        for i in lista_estudiantes:
            lista_materias = []
            hay_comun=False
            if self.id != i.id:
                for m in self.materias:
                    for ml in i.materias:
                        if m.Nclase == ml.Nclase:
                            if lista_materias.count(m) ==0:
                                hay_comun=True
                                lista_materias.append(m)
                if hay_comun:
                    lista_materias_comun.append(materias_comun(i.id ,lista_materias ))
        return lista_materias_comun

def encontrar_compañeros_clase(self , lista_estudiantes):
        print("--------------------------------compañeros de clase estudiante " , self.id)
        for i in self.encontrar_compañeros(lista_estudiantes):
            print("id estudiante:" , i.id_estudiante,
                  "clases en comun:", i.cantidad )
            for j in i.lista_materias:
                for x in j.clases:
                    print("     ",j.Nclase , j.nombre , x.dia , x.hora_inicio , x.hora_fin , x.aula )



def encontrar_sitios_comun(self , lista_estudiantes):
        print("------------------------------sitios en comun con el  estudiante " , self.id)
        for i in self.encontrar_sitios(lista_estudiantes):
            print("id estudiante:" , i.id_estudiante,
                  "sitios en comun:", i.cantidad )
            for j in i.lista_conexiones:
                print("     " , j.ano , j.mes , j.dia , j.dia_semana , j.hora , j.ap)

def encontrar_posibles_amigos(self, lista_estudiantes):
        lista_posibles_amigos=[]
        for sitios in self.encontrar_sitios(lista_estudiantes):
            aux =posible_amigo()
            aux.id_estudiante=sitios.id_estudiante
            aux.sitios_comun=sitios
            aux.afinidad=sitios.cantidad*2
            lista_posibles_amigos.append(aux)

        for materias in self.encontrar_compañeros(lista_estudiantes):
            esta=False
            for amigos in lista_posibles_amigos:
                if materias.id_estudiante == amigos.id_estudiante:
                    amigos.materias_comun=materias
                    amigos.afinidad=amigos.afinidad+amigos.materias_comun.cantidad
                    esta=True
            if esta==False:
                aux = posible_amigo()
                aux.id_estudiante = materias.id_estudiante
                aux.materias_comun = materias
                aux.afinidad = materias.cantidad
                lista_posibles_amigos.append(aux)

        lista_posibles_amigos=sorted(lista_posibles_amigos, key=lambda objeto: objeto.afinidad , reverse=True)

        for i in lista_posibles_amigos:
            print("----------------------------------------------------------------------------estudiante:", i.id_estudiante , "     puntos de afinidad :", i.afinidad)

            if i.sitios_comun != "null":
                print("------------sitios en comun")
                print("id_estudiante:" , i.sitios_comun.id_estudiante,
                      "sitios en comun :",i.sitios_comun.cantidad)
                for j in i.sitios_comun.lista_conexiones:
                    print("     ", j.ano, j.mes, j.dia, j.dia_semana, j.hora, j.ap)

            if i.materias_comun != "null":
                print("------------materias en comun")
                print("id_estudiante:" , i.materias_comun.id_estudiante,
                      "materias en comun:" , i.materias_comun.cantidad)
                for j in i.materias_comun.lista_materias:
                    for x in j.clases:
                        print("     ", j.Nclase, j.nombre, x.dia, x.hora_inicio, x.hora_fin, x.aula)