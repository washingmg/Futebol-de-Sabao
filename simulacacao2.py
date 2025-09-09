import threading
import time

class FutebolSabao:
    def __init__(self, num_jogadores):
        self.num_jogadores = num_jogadores
        self.bola_lock = threading.Lock()
        self.placar_timeA = 0
        self.placar_timeB = 0
        self.bola_posse = 0  # 0 = Joãozinho (time A)
        self.historico_toques = []  # armazena (id_jogador, time)
        self.jogo_ativo = True
        
    def jogador(self, id_jogador, time_jogador):
        """Função que representa cada jogador thread"""
        while self.jogo_ativo:
            with self.bola_lock:
                # Só pode tocar se for a vez dele e o jogo estiver ativo
                if self.bola_posse == id_jogador and self.jogo_ativo:
                    # Jogador toca na bola
                    self.historico_toques.append((id_jogador, time_jogador))
                    
                    # Verifica se é gol por 5 consecutivos
                    gol_5_consecutivos = self.verificar_gol_5_consecutivos()
                    # Verifica se é gol por tabelinha
                    gol_tabelinha = self.verificar_gol_tabelinha()
                    
                    time_do_gol = None
                    tipo_gol = ""
                    
                    if gol_5_consecutivos:
                        time_do_gol = time_jogador
                        tipo_gol = "5 toques consecutivos"
                    elif gol_tabelinha:
                        time_do_gol = time_jogador
                        tipo_gol = "tabelinha"
                    
                    # Se houve gol, marca e limpa histórico
                    if time_do_gol:
                        self.marcar_gol(tipo_gol, time_do_gol)
                        self.historico_toques = []  # Limpa histórico após gol
                    
                    # Passa a bola para o próximo jogador
                    self.bola_posse = (id_jogador + 1) % self.num_jogadores
    
    def verificar_gol_5_consecutivos(self):
        """Verifica se houve 5 toques consecutivos do mesmo time"""
        if len(self.historico_toques) < 5:
            return False
        
        # Pega os últimos 5 toques
        ultimos_5 = self.historico_toques[-5:]
        times_ultimos_5 = [time for _, time in ultimos_5]
        
        # Verifica se todos são do mesmo time
        primeiro_time = times_ultimos_5[0]
        return all(time == primeiro_time for time in times_ultimos_5)
    
    def verificar_gol_tabelinha(self):
        """Verifica se houve tabelinha (2 jogadores do mesmo time alternando 3 vezes)"""
        if len(self.historico_toques) < 6:
            return False
        
        # Pega os últimos 6 toques
        ultimos_6 = self.historico_toques[-6:]
        times_ultimos_6 = [time for _, time in ultimos_6]
        
        # Verifica o padrão de alternância entre dois times iguais
        # Exemplo: A, B, A, B, A, B onde A e B são do mesmo time
        time_A = times_ultimos_6[0]
        time_B = times_ultimos_6[1]
        
        # Primeiro verifica se A e B são do mesmo time
        if time_A != time_B:
            return False
        
        # Verifica o padrão alternado: A, B, A, B, A, B
        for i in range(6):
            if i % 2 == 0:  # posições pares (0, 2, 4)
                if times_ultimos_6[i] != time_A:
                    return False
            else:  # posições ímpares (1, 3, 5)
                if times_ultimos_6[i] != time_B:
                    return False
        
        return True
    
    def marcar_gol(self, tipo_gol, time):
        """Marca um gol e imprime o placar"""
        if time == "A":
            self.placar_timeA += 1
        else:
            self.placar_timeB += 1
        
        print(f"⚽ GOL DO TIME {time}! ({tipo_gol})")
        print(f"Placar: Time A {self.placar_timeA} × {self.placar_timeB} Time B")
        print("-" * 40)
        
        # Verifica se o jogo acabou (diferença de 500 gols)
        diferenca = abs(self.placar_timeA - self.placar_timeB)
        if diferenca >= 500:
            self.jogo_ativo = False
            print("🎉 FIM DE JOGO!")
            if self.placar_timeA > self.placar_timeB:
                print(f"Time A venceu por {self.placar_timeA} × {self.placar_timeB}")
            else:
                print(f"Time B venceu por {self.placar_timeB} × {self.placar_timeA}")
            print("=" * 50)

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
        time_jogador = "A" if i % 2 == 0 else "B"
        thread = threading.Thread(target=jogo.jogador, args=(i, time_jogador))
        thread.daemon = True
        threads.append(thread)
        thread.start()
    
    # Mantém o programa rodando até o fim do jogo
    try:
        while jogo.jogo_ativo:
            pass  # Loop vazio para manter o programa rodando sem delays
    
    except KeyboardInterrupt:
        print("\nJogo interrompido pelo usuário!")
        jogo.jogo_ativo = False

if __name__ == "__main__":
    main()