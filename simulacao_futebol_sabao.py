import threading
import random
import time

# Classe Jogador (Thread)
class Jogador(threading.Thread):
    def __init__(self, id, time, jogo):
        super().__init__()
        self.id = id
        self.time = time
        self.jogo = jogo

    def run(self):
        while not self.jogo.fim:
            with self.jogo.condicao:
                while self.jogo.bola != self.id and not self.jogo.fim:
                    self.jogo.condicao.wait()
                if self.jogo.fim:
                    break

                proximo = random.choice(self.jogo.jogadores_ids)
                while proximo == self.id:  # não pode passar pra si mesmo
                    proximo = random.choice(self.jogo.jogadores_ids)

                self.jogo.registrar_toque(self.id, self.time, proximo)
                self.jogo.bola = proximo
                self.jogo.condicao.notify_all()


# Classe Jogo
class Jogo:
    def __init__(self, n_jogadores):
        self.n_jogadores = n_jogadores
        self.jogadores_ids = list(range(n_jogadores))
        self.condicao = threading.Condition()
        self.bola = 0
        self.times = {i: (1 if i % 2 == 0 else 2) for i in self.jogadores_ids}
        self.toques_consecutivos = []
        self.tabelinha = []
        self.placar = {1: 0, 2: 0}
        self.fim = False

    def registrar_toque(self, jogador, time, proximo):
        print(f"Jogador {jogador} (Time {time}) passou para Jogador {proximo} (Time {self.times[proximo]})")
        print(f"Placar em tempo real: Time 1 [{self.placar[1]}] x [{self.placar[2]}] Time 2\n")

        # Verifica regra dos 5 toques consecutivos
        if not self.toques_consecutivos or self.toques_consecutivos[-1] == time:
            self.toques_consecutivos.append(time)
        else:
            self.toques_consecutivos = [time]
        if len(self.toques_consecutivos) >= 5:
            self.gol(time, "5 toques consecutivos")
            self.toques_consecutivos = []

        # Verifica regra da tabelinha (2 jogadores do mesmo time alternando 3x)
        if len(self.tabelinha) >= 1 and self.tabelinha[-1][1] == time:
            if self.tabelinha[-1][0] != jogador:
                self.tabelinha.append((jogador, time))
            else:
                self.tabelinha = [(jogador, time)]
        else:
            self.tabelinha = [(jogador, time)]

        if len(self.tabelinha) >= 6:  
            self.gol(time, "tabelinha")
            self.tabelinha = []

        # Condição de fim de jogo
        if abs(self.placar[1] - self.placar[2]) >= 500:
            self.fim = True

    def gol(self, time, tipo):
        self.placar[time] += 1
        print(f"\n⚽ GOL do Time {time} ({tipo})!")
        print(f"Placar atualizado: Time 1 [{self.placar[1]}] x [{self.placar[2]}] Time 2\n")


# Execução principal
if __name__ == "__main__":
    n = int(input("Digite o número de jogadores (par > 4): "))
    if n <= 4 or n % 2 != 0:
        print("Número inválido! Tem que ser par e > 4.")
        exit()

    jogo = Jogo(n)
    jogadores = [Jogador(i, jogo.times[i], jogo) for i in jogo.jogadores_ids]

    for j in jogadores:
        j.start()

    # Bola começa com Joãozinho
    with jogo.condicao:
        jogo.condicao.notify_all()

    for j in jogadores:
        j.join()

    # Placar final
    print("\nFim de jogo!")
    print(f"Placar final: Time 1 [{jogo.placar[1]}] x [{jogo.placar[2]}] Time 2")
