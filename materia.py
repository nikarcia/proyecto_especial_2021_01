class materia:
    Nclase = ""
    nombre = ""
    semestre = ""
    clases=[]
    def __init__(self, Nclase, nombre, semestre, clases):
        self.Nclase = Nclase
        self.nombre = nombre
        self.clases = clases
        self.semestre = semestre

class clase:
    aula=""
    dia = ""
    hora_inicio = ""
    hora_fin = ""
    def __init__(self,aula, dia, hora_inicio, hora_fin):
        self.aula = aula
        self.dia = dia
        self.hora_inicio = hora_inicio
        self.hora_fin = hora_fin