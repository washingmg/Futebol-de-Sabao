import threading
import random
from collections import deque
from enum import Enum
from typing import Deque, Tuple, Optional, Dict, List

# -----------------------------------------------------------------------------
# Seção 1: Constantes e Configurações do Jogo
# -----------------------------------------------------------------------------

NUMERO_MINIMO_JOGADORES: int = 4
DIFERENCA_DE_GOLS_VITORIA: int = 500
TAMANHO_HISTORICO_TOQUES: int = 10
TOQUES_CONSECUTIVOS_GOL: int = 5
TOQUES_TABELINHA: int = 6
NOME_TIME_0: str = "TIME 0"
NOME_TIME_1: str = "TIME 1"

class TipoDeGol(Enum):
    """
    Enum para representar os tipos de gol de forma segura e explícita.
    """
    CINCO_TOQUES = "5 TOQUES"
    TABELINHA = "TABELINHA"

# Define um tipo para representar um toque: (id_jogador, id_time)
Toque = Tuple[int, int]

# -----------------------------------------------------------------------------
# Seção 2: Componentes de Lógica de Negócio
# -----------------------------------------------------------------------------

class Placar:
    """
    Responsável exclusivamente por gerenciar o placar e as estatísticas do jogo.
    """
    def __init__(self, nome_time_0: str, nome_time_1: str) -> None:
        self.pontos: list[int] = [0, 0]
        self.contagem_gols: Dict[TipoDeGol, int] = {
            TipoDeGol.CINCO_TOQUES: 0,
            TipoDeGol.TABELINHA: 0,
        }
        self.nomes_times = (nome_time_0, nome_time_1)

    def adicionar_gol(self, time: int, tipo_gol: TipoDeGol) -> None:
        """Registra um novo gol para o time especificado."""
        if time in [0, 1]:
            self.pontos[time] += 1
            self.contagem_gols[tipo_gol] += 1

    def get_diferenca_gols(self) -> int:
        """Retorna a diferença absoluta de gols entre os times."""
        return abs(self.pontos[0] - self.pontos[1])

    def exibir_placar_atual(self) -> str:
        """Retorna uma string formatada do placar atual."""
        return (
            f"Placar: {self.nomes_times[0]} [{self.pontos[0]}] x "
            f"[{self.pontos[1]}] {self.nomes_times[1]}"
        )

    def exibir_estatisticas_finais(self) -> str:
        """Retorna uma string formatada com as estatísticas finais do jogo."""
        return (
            f"Placar final: {self.nomes_times[0]} [{self.pontos[0]}] x "
            f"[{self.pontos[1]}] {self.nomes_times[1]}\n"
            f"Gols de {TipoDeGol.CINCO_TOQUES.value}: {self.contagem_gols[TipoDeGol.CINCO_TOQUES]}\n"
            f"Gols de {TipoDeGol.TABELINHA.value}: {self.contagem_gols[TipoDeGol.TABELINHA]}"
        )

class MotorDeRegras:
    """
    Componente sem estado que encapsula a lógica de verificação de gols.
    """
    def analisar_jogada_para_gol(self, historico_toques: Deque[Toque]) -> Optional[TipoDeGol]:
        """
        Analisa o histórico de toques para determinar se um gol foi marcado.
        """
        gol_tabelinha = self._verificar_tabelinha(historico_toques)
        if gol_tabelinha:
            return gol_tabelinha

        gol_cinco_toques = self._verificar_cinco_toques(historico_toques)
        if gol_cinco_toques:
            return gol_cinco_toques

        return None

    def _verificar_cinco_toques(self, historico_toques: Deque[Toque]) -> Optional[TipoDeGol]:
        """Regra 1: 5 toques consecutivos do mesmo time."""
        if len(historico_toques) < TOQUES_CONSECUTIVOS_GOL:
            return None

        ultimos_cinco = list(historico_toques)[-TOQUES_CONSECUTIVOS_GOL:]
        primeiro_time = ultimos_cinco[0][1]

        if all(time == primeiro_time for _, time in ultimos_cinco):
            return TipoDeGol.CINCO_TOQUES
        return None

    def _verificar_tabelinha(self, historico_toques: Deque[Toque]) -> Optional[TipoDeGol]:
        """Regra 2: Tabelinha entre dois jogadores do mesmo time."""
        if len(historico_toques) < TOQUES_TABELINHA:
            return None

        ultimos_seis = list(historico_toques)[-TOQUES_TABELINHA:]
        jogadores = [j for j, _ in ultimos_seis]
        times = [t for _, t in ultimos_seis]

        if len(set(times)) != 1 or len(set(jogadores)) != 2:
            return None
        
        jogador_a, jogador_b = list(set(jogadores))
        
        padrao_esperado_1 = [jogador_a, jogador_b] * (TOQUES_TABELINHA // 2)
        padrao_esperado_2 = [jogador_b, jogador_a] * (TOQUES_TABELINHA // 2)
        
        if jogadores == padrao_esperado_1 or jogadores == padrao_esperado_2:
            return TipoDeGol.TABELINHA
            
        return None

# -----------------------------------------------------------------------------
# Seção 3: Orquestração do Jogo e Concorrência
# -----------------------------------------------------------------------------

class Jogo:
    """
    Classe orquestradora que gerencia o estado do jogo e as threads.
    """
    def __init__(self, numero_de_jogadores: int):
        self.numero_de_jogadores = numero_de_jogadores
        self.placar = Placar(NOME_TIME_0, NOME_TIME_1)
        self.motor_regras = MotorDeRegras()
        
        self.jogo_terminou = threading.Event()
        self.historico_toques: deque = deque(maxlen=TAMANHO_HISTORICO_TOQUES)
        
        self.lock_estado_jogo = threading.Lock()
        #self.semaforos_jogadores = []
        self.semaforos_jogadores = [threading.Semaphore(0) for _ in range(numero_de_jogadores)]
        
        self.semaforos_jogadores[0].release() # Joãozinho (jogador 0) começa
    def registrar_toque(self, id_jogador: int, time: int) -> None:
        """Processa o toque de um jogador dentro de uma seção crítica."""
        with self.lock_estado_jogo:
            if self.jogo_terminou.is_set():
                return

            self.historico_toques.append((id_jogador, time))
            tipo_gol = self.motor_regras.analisar_jogada_para_gol(self.historico_toques)
            
            if tipo_gol:
                self.placar.adicionar_gol(time, tipo_gol)
                print(f"GOL DO {self.placar.nomes_times[time]}! Tipo: {tipo_gol.value}")
                print(f"{self.placar.exibir_placar_atual()}\n")

                if self.placar.get_diferenca_gols() >= DIFERENCA_DE_GOLS_VITORIA:
                    self.finalizar_jogo()
                    return
            
            proximo_jogador = random.randint(0, self.numero_de_jogadores - 1)
            self.semaforos_jogadores[proximo_jogador].release()

    def finalizar_jogo(self) -> None:
        """Sinaliza o fim do jogo e libera todas as threads."""
        print("Fim de jogo!!")
        self.jogo_terminou.set()
        for semaforo in self.semaforos_jogadores:
            semaforo.release()

class Jogador(threading.Thread):
    """Representa um jogador como uma thread."""
    def __init__(self, id_jogador: int, time: int, jogo: Jogo):
        super().__init__(name=f"Jogador-{id_jogador}")
        self.id_jogador = id_jogador
        self.time = time
        self.jogo = jogo

    def run(self) -> None:
        """O ciclo de vida da thread do jogador."""
        while not self.jogo.jogo_terminou.is_set():
            self.jogo.semaforos_jogadores[self.id_jogador].acquire()
            
            if self.jogo.jogo_terminou.is_set():
                break
                
            self.jogo.registrar_toque(self.id_jogador, self.time)

# -----------------------------------------------------------------------------
# Seção 4: Ponto de Entrada da Aplicação
# -----------------------------------------------------------------------------

def obter_numero_de_jogadores() -> int:
    """Solicita ao usuário o número de jogadores e valida a entrada."""
    while True:
        try:
            n = int(input(f"Digite o número de jogadores (par e > {NUMERO_MINIMO_JOGADORES}): "))
            if n > NUMERO_MINIMO_JOGADORES and n % 2 == 0:
                return n
            print(f"Valor inválido! O número deve ser par e maior que {NUMERO_MINIMO_JOGADORES}.")
        except ValueError:
            print("Entrada inválida! Por favor, digite um número inteiro.")

def main() -> None:
    """Função principal que inicializa e executa o jogo."""
    numero_jogadores = obter_numero_de_jogadores()
    
    jogo = Jogo(numero_jogadores)
    #threads_jogadores: List[Jogador] = [] 
    threads_jogadores: List[Jogador] = []
    for i in range(numero_jogadores):
        time_jogador = i % 2
        jogador = Jogador(i, time_jogador, jogo)
        threads_jogadores.append(jogador)
        jogador.start()

    for thread in threads_jogadores:
        thread.join()

    print(jogo.placar.exibir_estatisticas_finais())

if __name__ == "__main__":
    main()