# relogio.py

class Tempo:
    def __init__(self, horas, minutos, segundos):
        self.horas = horas
        self.minutos = minutos
        self.segundos = segundos

    def avancar_segundo(self):
        self.segundos += 1
        if self.segundos >= 60:
            self.segundos = 0
            self.minutos += 1
            if self.minutos >= 60:
                self.minutos = 0
                self.horas += 1
                if self.horas >= 24:
                    self.horas = 0

    def obter_tempo(self):
        return f"{self.horas:02d}:{self.minutos:02d}:{self.segundos:02d}"

class Alarme:
    def __init__(self, tempo_alarme, mensagem):
        self.tempo_alarme = tempo_alarme # Exemplo de composição (implícita)
        self.mensagem = mensagem
        self.__ativo = False # Atributo privado

    def ativar(self):
        self.__ativo = True

    def desativar(self):
        self.__ativo = False

    def _verificar(self, tempo_atual): # Método protegido
        if self.__ativo and tempo_atual == self.tempo_alarme.obter_tempo():
            print(f"ALERTA! {self.mensagem}")
            return True
        return False

class Relogio(Tempo, Alarme): # Herança múltipla
    _zona_horaria = "GMT" # Atributo de classe protegido

    def __init__(self, horas, minutos, segundos, tempo_alarme, mensagem):
        Tempo.__init__(self, horas, minutos, segundos)
        Alarme.__init__(self, tempo_alarme, mensagem)
        self.data_atual = "2025-06-06" # Outro atributo de instância

    def tick(self):
        self.avancar_segundo() # Chama método herdado de Tempo
        self._verificar(self.obter_tempo()) # Chama método herdado de Alarme

    def configurar_zona_horaria(self, zona):
        Relogio._zona_horaria = zona # Modifica atributo de classe