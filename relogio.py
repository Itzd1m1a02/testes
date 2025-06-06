"""
Arquivo Python com estrutura complexa para testar a geração de diagramas.
Tema: Sistema de Gerenciamento de um Zoológico Galáctico.
"""

from __future__ import annotations
from typing import List, Dict, Optional
from enum import Enum, auto

# Usando Enum para tipos de dados categóricos
class Dieta(Enum):
    CARNIVORO = auto()
    HERBIVORO = auto()
    OMNIVORO = auto()
    FOTOSSINTETICO = auto()

# Classe base para a maioria dos objetos do sistema
class EntidadeCosmica:
    """Classe base para qualquer objeto identificável no universo."""
    def __init__(self, nome: str, idade_estelar: float):
        self.nome = nome
        self.idade_estelar = idade_estelar
        self._id_entidade = hash(nome + str(idade_estelar)) # Atributo "privado"

    def get_info(self) -> str:
        """Retorna uma descrição básica da entidade."""
        return f"Entidade '{self.nome}' (ID: {self._id_entidade}) com {self.idade_estelar} mega-anos."

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(nome={self.nome})>"


# Exemplo de Herança: Planeta herda de EntidadeCosmica
class Planeta(EntidadeCosmica):
    """Representa um planeta em um sistema estelar."""
    def __init__(self, nome: str, idade_estelar: float, tipo: str, luas: int):
        super().__init__(nome, idade_estelar)
        self.tipo = tipo # Ex: "Rochoso", "Gigante Gasoso"
        self.luas: List[str] = []
        for i in range(luas):
            self.luas.append(f"{nome}-Lua-{i+1}")

    def get_info(self) -> str:
        """Sobrescreve o método da classe pai para adicionar mais detalhes."""
        info_base = super().get_info()
        return f"{info_base}\n -> Planeta do tipo '{self.tipo}' com {len(self.luas)} luas."


# Exemplo de Composição: Especie contém um objeto Planeta
class EspecieAlien:
    """Define uma espécie alienígena e suas características."""
    def __init__(self, nome_cientifico: str, planeta_origem: Planeta, dieta: Dieta):
        self.nome_cientifico = nome_cientifico
        self.planeta_origem = planeta_origem # Composição: uma espécie TEM UM planeta de origem
        self.dieta = dieta
        self.codigo_genetico = self._gerar_codigo_genetico()

    def _gerar_codigo_genetico(self) -> str:
        """Método privado para gerar um código genético aleatório."""
        base_hash = hash(self.nome_cientifico + self.planeta_origem.nome)
        return f"GEN-{abs(base_hash)}"

    def e_perigoso(self) -> bool:
        """Determina se a espécie é perigosa com base na dieta."""
        return self.dieta == Dieta.CARNIVORO


# Outro exemplo de Herança: Inabitante herda de EntidadeCosmica
class Inabitante(EntidadeCosmica):
    """Representa um ser individual de uma espécie."""
    def __init__(self, nome: str, idade_estelar: float, especie: EspecieAlien):
        super().__init__(nome, idade_estelar)
        self.especie = especie # Composição: um inabitante É DE UMA espécie

    def get_info(self) -> str:
        info_base = super().get_info()
        info_especie = f"Espécie: {self.especie.nome_cientifico} | Dieta: {self.especie.dieta.name}"
        return f"{info_base}\n -> {info_especie}"


# Classe principal que gerencia as outras (Agregação)
class ZoologicoGalactico:
    """Gerencia todos os aspectos do zoológico, incluindo jaulas e inabitantes."""
    def __init__(self, nome_zoo: str):
        self.nome_zoo = nome_zoo
        # Agregação: o zoológico TEM um dicionário de Jaulas
        self.jaulas: Dict[int, Jaula] = {}
        self._proximo_id_jaula = 1

    def adicionar_jaula(self, ambiente: str) -> Jaula:
        """Cria e adiciona uma nova jaula ao zoológico."""
        nova_jaula = Jaula(id_jaula=self._proximo_id_jaula, tipo_ambiente=ambiente)
        self.jaulas[self._proximo_id_jaula] = nova_jaula
        self._proximo_id_jaula += 1
        print(f"Jaula {nova_jaula.id_jaula} ({ambiente}) adicionada ao {self.nome_zoo}.")
        return nova_jaula

    def adicionar_inabitante_a_jaula(self, inabitante: Inabitante, id_jaula: int) -> bool:
        """Aloca um inabitante a uma jaula específica."""
        if id_jaula not in self.jaulas:
            print(f"Erro: Jaula com ID {id_jaula} não existe.")
            return False
        
        jaula_alvo = self.jaulas[id_jaula]
        jaula_alvo.adicionar_ocupante(inabitante)
        return True

    def relatorio_geral(self):
        """Imprime um relatório completo do estado do zoológico."""
        print("\n" + "="*40)
        print(f"Relatório do Zoológico Galáctico: '{self.nome_zoo}'")
        print("="*40)
        if not self.jaulas:
            print("Zoológico está vazio.")
            return
            
        for id_jaula, jaula in self.jaulas.items():
            print(f"\n--- Jaula ID: {id_jaula} | Ambiente: {jaula.tipo_ambiente} ---")
            if not jaula.ocupantes:
                print(" > Vazia")
            else:
                for ocupante in jaula.ocupantes:
                    print(f" > Ocupante: {ocupante.nome} ({ocupante.especie.nome_cientifico})")
        print("="*40)


class Jaula:
    """Representa uma jaula ou habitat dentro do zoológico."""
    def __init__(self, id_jaula: int, tipo_ambiente: str):
        self.id_jaula = id_jaula
        self.tipo_ambiente = tipo_ambiente # Ex: "Aquático", "Desértico", "Gravidade Zero"
        self.ocupantes: List[Inabitante] = [] # Agregação: uma jaula TEM uma lista de Inabitantes

    def adicionar_ocupante(self, ocupante: Inabitante):
        """Adiciona um novo inabitante à jaula."""
        print(f"Alocando '{ocupante.nome}' à jaula {self.id_jaula}.")
        self.ocupantes.append(ocupante)


# Função principal para demonstrar o uso das classes
if __name__ == "__main__":
    # 1. Criar Planetas
    tatooine = Planeta(nome="Tatooine", idade_estelar=4.2, tipo="Desértico", luas=3)
    krypton = Planeta(nome="Krypton", idade_estelar=6.5, tipo="Cristalino", luas=1)

    # 2. Criar Espécies
    especie_jawa = EspecieAlien(nome_cientifico="Jawa sandcrawlerus", planeta_origem=tatooine, dieta=Dieta.OMNIVORO)
    especie_kryptoniana = EspecieAlien(nome_cientifico="Kryptonian solaris", planeta_origem=krypton, dieta=Dieta.FOTOSSINTETICO)

    # 3. Criar Inabitantes
    dath_jawa = Inabitante(nome="Dath", idade_estelar=0.05, especie=especie_jawa)
    kal_el = Inabitante(nome="Kal-El", idade_estelar=0.03, especie=especie_kryptoniana)

    # 4. Montar o Zoológico
    meu_zoo = ZoologicoGalactico(nome_zoo="Maravilhas Interestelares de Dimitri")
    jaula1 = meu_zoo.adicionar_jaula("Desértico com Cavernas")
    jaula2 = meu_zoo.adicionar_jaula("Solário de Espectro Amarelo")

    # 5. Popular o Zoológico
    meu_zoo.adicionar_inabitante_a_jaula(dath_jawa, jaula1.id_jaula)
    meu_zoo.adicionar_inabitante_a_jaula(kal_el, jaula2.id_jaula)
    
    # 6. Gerar Relatório
    meu_zoo.relatorio_geral()
