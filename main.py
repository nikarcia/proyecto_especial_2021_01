import DB
import grupos_estudiantes as ge

if __name__ == '__main__':
    lista_estudiantes = DB.generar_lista_estudiantes("01/01/2020" , "01/05/2020")

    for i in lista_estudiantes:
        i.conexiones_comun_por_estudiante = ge.hallar_conexiones_comun_estudiantes(i , lista_estudiantes)


    estudiante=lista_estudiantes[0]
    #estudiante.print_conexiones_comun()


    #estudiante.print_tiempo_total_tiempo_por_amigo()

    #estudiante.print_tiempo_amigos_tiempo_por_amigo()
    estudiante.print_tiempo_uso_tiempo_por_amigo()
    #estudiante.print_tiempo_dia_tiempo_por_amigo()
    #estudiante.print_tiempo_place_tiempo_por_amigo()

    #estudiante.print_conexiones_comun()


    #print(estudiante.tiempo_conectado)
    #print(estudiante.tiempo_conectado_con_otros)

    #estudiante.print_registros()
    #estudiante.print_conexiones()

    #estudiante.print_frecuenciaXuso()
    #estudiante.print_frecuenciaXplace()
    #estudiante.print_frecuenciaXdia_semana()
    #estudiante.print_frecuenciaXap_group()
    #estudiante.print_frecuenciaXclient_device_type()



