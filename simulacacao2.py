import threading
import time
import random

class FutebolSabao:
    def __init__(self, num_jogadores):
        self.num_jogadores = num_jogadores
        self.bola_lock = threading.Lock()
        self.ultimo_time = None
        self.contagem_consecutiva = 0
        self.contagem_alternada = 0
        self.placar_timeA = 0
        self.placar_timeB = 0
        self.bola_posse = 0  # 0 = Joãozinho (time A)
        self.historico_toques = []
        self.jogo_ativo = True
        
    def jogador(self, id_jogador, time):
        """Função que representa cada jogador thread"""
        while self.jogo_ativo:
            with self.bola_lock:
                # Só pode tocar se for a vez dele e o jogo estiver ativo
                if self.bola_posse == id_jogador and self.jogo_ativo:
                    # Jogador toca na bola
                    self.historico_toques.append((id_jogador, time))
                    
                    # Verifica se é gol por 5 consecutivos
                    if self.verificar_gol_5_consecutivos():
                        self.marcar_gol("5 toques consecutivos", time)
                    
                    # Verifica se é gol por tabelinha (2 alternados 3 vezes)
                    elif self.verificar_gol_tabelinha():
                        # Descobre qual time fez o gol (o último que tocou)
                        self.marcar_gol("tabelinha", time)
                    
                    # Passa a bola para o próximo jogador
                    self.bola_posse = (id_jogador + 1) % self.num_jogadores
                    
                    # Pequena pausa para não sobrecarregar
                    time.sleep(0.01)
    
    def verificar_gol_5_consecutivos(self):
        """Verifica se houve 5 toques consecutivos do mesmo time"""
        if len(self.historico_toques) < 5:
            return False
        
        # Pega os últimos 5 toques
        ultimos_5 = self.historico_toques[-5:]
        times_ultimos_5 = [time for _, time in ultimos_5]
        
        # Verifica se todos são do mesmo time
        primeiro_time = times_ultimos_5[0]
        if all(time == primeiro_time for time in times_ultimos_5):
            return True
        
        return False
    
    def verificar_gol_tabelinha(self):
        """Verifica se houve tabelinha (2 jogadores do mesmo time alternando 3 vezes)"""
        if len(self.historico_toques) < 6:
            return False
        
        # Pega os últimos 6 toques (3 ciclos de 2)
        ultimos_6 = self.historico_toques[-6:]
        jogadores_ultimos_6 = [jogador for jogador, _ in ultimos_6]
        times_ultimos_6 = [time for _, time in ultimos_6]
        
        # Verifica o padrão de alternância: A,B,A,B,A,B ou B,A,B,A,B,A
        # onde A e B são do mesmo time (mas jogadores diferentes)
        
        # Padrão 1: jogador par, ímpar, par, ímpar, par, ímpar (mesmo time)
        if (jogadores_ultimos_6[0] % 2 == 0 and 
            jogadores_ultimos_6[1] % 2 == 1 and
            jogadores_ultimos_6[2] % 2 == 0 and
            jogadores_ultimos_6[3] % 2 == 1 and
            jogadores_ultimos_6[4] % 2 == 0 and
            jogadores_ultimos_6[5] % 2 == 1 and
            times_ultimos_6[0] == times_ultimos_6[2] == times_ultimos_6[4] and
            times_ultimos_6[1] == times_ultimos_6[3] == times_ultimos_6[5] and
            times_ultimos_6[0] == times_ultimos_6[1]):
            return True
        
        # Padrão 2: jogador ímpar, par, ímpar, par, ímpar, par (mesmo time)
        if (jogadores_ultimos_6[0] % 2 == 1 and 
            jogadores_ultimos_6[1] % 2 == 0 and
            jogadores_ultimos_6[2] % 2 == 1 and
            jogadores_ultimos_6[3] % 2 == 0 and
            jogadores_ultimos_6[4] % 2 == 1 and
            jogadores_ultimos_6[5] % 2 == 0 and
            times_ultimos_6[0] == times_ultimos_6[2] == times_ultimos_6[4] and
            times_ultimos_6[1] == times_ultimos_6[3] == times_ultimos_6[5] and
            times_ultimos_6[0] == times_ultimos_6[1]):
            return True
        
        return False
    
    def marcar_gol(self, tipo_gol, time):
        """Marca um gol e imprime o placar"""
        if time == "A":
            self.placar_timeA += 1
        else:
            self.placar_timeB += 1
        
        print(f"⚽ GOL DO TIME {time}! ({tipo_gol})")
        print(f"Placar: Time A {self.placar_timeA} × {self.placar_timeB} Time B")
        print("-" * 40)
        
        # Limpa o histórico para evitar gol em cadeia
        self.historico_toques = []
        
        # Verifica se o jogo acabou (diferença de 500 gols)
        diferenca = abs(self.placar_timeA - self.placar_timeB)
        if diferenca >= 500:
            self.jogo_ativo = False
            print("🎉 FIM DE JOGO!")
            if self.placar_timeA > self.placar_timeB:
                print(f"Time A venceu por {self.placar_timeA} × {self.placar_timeB}")
            else:
                print(f"Time B venceu por {self.placar_timeB} × {self.placar_timeA}")

def main():
    """Função principal do programa"""
    print("=" * 50)
    print("       FUTEBOL DE SABÃO - SIMULADOR")
    print("=" * 50)
    
    # Solicita número de jogadores
    while True:
        try:
            num_jogadores = int(input("Digite o número total de jogadores (par e maior que 4): "))
            if num_jogadores <= 4:
                print("Erro: O número deve ser maior que 4!")
            elif num_jogadores % 2 != 0:
                print("Erro: O número deve ser par!")
            else:
                break
        except ValueError:
            print("Erro: Digite um número válido!")
    
    print(f"\nIniciando jogo com {num_jogadores} jogadores...")
    print("Joãozinho é o jogador 0 (Time A)")
    print("=" * 50)
    
    # Cria a instância do jogo
    jogo = FutebolSabao(num_jogadores)
    
    # Cria as threads dos jogadores
    threads = []
    for i in range(num_jogadores):
        # Define o time: pares são Time A, ímpares são Time B
        time = "A" if i % 2 == 0 else "B"
        thread = threading.Thread(target=jogo.jogador, args=(i, time))
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    # Mantém o programa rodando até o fim do jogo
    try:
        while jogo.jogo_ativo:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nJogo interrompido pelo usuário!")
        jogo.jogo_ativo = False

if __name__ == "__main__":
    main()