import threading
import random

class Jogo:
    def __init__(self, n_jogadores):
        self.n_jogadores = n_jogadores
        self.times = [0, 0]  # placar
        self.fim = False

        # Controle da posse da bola
        self.jogadores = []
        self.bola = 0  # começa com Joãozinho (jogador 0)
        self.semaforos = [threading.Semaphore(0) for _ in range(n_jogadores)]
        self.semaforos[self.bola].release()  # libera Joãozinho

        # Histórico de toques
        self.ultimos_toques = []
        self.lock = threading.Lock()

    def registrar_toque(self, jogador_id, time):
        with self.lock:
            # Guarda o toque
            self.ultimos_toques.append((jogador_id, time))
            if len(self.ultimos_toques) > 10:
                self.ultimos_toques.pop(0)

            # Verifica gol
            gol = self.verificar_gol()
            if gol:
                self.times[time] += 1
                print(f"⚽ GOL DO TIME {time}! Tipo: {gol}")
                print(f"Placar: TIME 0 [{self.times[0]}] x [{self.times[1]}] TIME 1\n")

                # Condição de fim
                if abs(self.times[0] - self.times[1]) >= 500:
                    self.fim = True
                    # libera todos os semáforos para encerrar as threads
                    for sem in self.semaforos:
                        sem.release()
                    return

            # Passa a bola para o próximo jogador aleatório
            if not self.fim:
                proximo = random.randint(0, self.n_jogadores - 1)
                self.bola = proximo
                self.semaforos[proximo].release()

    def verificar_gol(self):
        # Regra 1: 5 toques consecutivos do mesmo time
        if len(self.ultimos_toques) >= 5:
            ultimos_5 = self.ultimos_toques[-5:]
            if all(t[1] == ultimos_5[0][1] for t in ultimos_5):
                return "5 TOQUES"

        # Regra 2: Tabelinha entre dois jogadores do mesmo time alternando 3 vezes
        if len(self.ultimos_toques) >= 6:
            ultimos_6 = self.ultimos_toques[-6:]
            jogadores = [j for j, _ in ultimos_6]
            times = [t for _, t in ultimos_6]
            if len(set(jogadores)) == 2 and len(set(times)) == 1:
                padrao = [jogadores[0], jogadores[1]] * 3
                if jogadores == padrao:
                    return "TABELINHA"

        return None


class Jogador(threading.Thread):
    def __init__(self, id, time, jogo):
        super().__init__()
        self.id = id
        self.time = time
        self.jogo = jogo

    def run(self):
        while True:
            self.jogo.semaforos[self.id].acquire()
            if self.jogo.fim:
                break
            self.jogo.registrar_toque(self.id, self.time)


def main():
    while True:
        n = int(input("Digite o número de jogadores (par e > 4): "))
        if n > 4 and n % 2 == 0:
            break
        print("Valor inválido! Tente novamente.")

    jogo = Jogo(n)
    for i in range(n):
        jogador = Jogador(i, i % 2, jogo)
        jogo.jogadores.append(jogador)
        jogador.start()

    for j in jogo.jogadores:
        j.join()

    print("🏁 Fim de jogo!")
    print(f"Placar final: TIME 0 [{jogo.times[0]}] x [{jogo.times[1]}] TIME 1")


if __name__ == "__main__":
    main()
