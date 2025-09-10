# ⚽ Futebol de Sabão (Simulação com Threads)  
### Trabalho acadêmico desenvolvido na disciplina de **Sistemas Operacionais (SO)**, no curso de **Ciência da Computação**, com o objetivo de aplicar conceitos de **concorrência, sincronização e exclusão mútua** através da utilização de **threads** em Python.  
---
## 👨‍🎓 Autores  
Este projeto foi desenvolvido pelos discentes:  
- [Jhony Wictor do Nascimento Santos](https://github.com/jhonywsantos), [Lucas Rosendo de Farias](https://github.com/LucaRosendo), [Washington Medeiros Mazzone Gaia](https://github.com/washingmg)  
---
## 📖 Descrição do Problema  
A proposta do trabalho é simular uma partida de **Futebol de Sabão**, na qual cada jogador é representado por uma **thread** independente.  
O fluxo de execução é controlado por mecanismos de sincronização, garantindo que a posse da bola seja exclusiva e que as regras de jogo sejam corretamente aplicadas.  

A bola inicia com **Joãozinho (jogador 0)**, e a cada jogada é passada aleatoriamente para outro jogador, respeitando as regras de **gol por 5 toques consecutivos** ou **tabelinha entre dois jogadores do mesmo time**.  

A simulação só termina quando **um dos times alcança uma diferença mínima de 500 gols em relação ao adversário**.  
---
## 📝 Regras da Simulação  
1. Cada jogador é representado por **uma thread**.  
2. Apenas **um jogador pode ter a posse da bola por vez** (controle de exclusão mútua).  
3. O número de jogadores deve ser obrigatoriamente:  
   - **par**  
   - **maior que 4**  
   - **informado pelo usuário no início da execução**.  
4. Critérios para a ocorrência de gols:  
   - **Gol por 5 TOQUES**: quando 5 jogadores consecutivos do mesmo time tocam na bola.  
   - **Gol por TABELINHA**: quando 2 jogadores do mesmo time alternam passes **3 vezes consecutivas**.  
5. Após cada gol, o programa deve registrar no terminal:  
   - O **time que marcou**.  
   - O **tipo de gol** (5 TOQUES ou TABELINHA).  
   - O **placar atualizado**.  
6. A partida encerra automaticamente quando a diferença entre os placares atinge **500 gols**.  
---
## ⚙️ Estrutura do Código  
- **Classe `Jogo`**  
  - Gerencia os jogadores, placar e condições de término da partida.  
  - Utiliza listas para armazenar o histórico de toques e verificar padrões de gol.  
  - Faz uso de `threading.Lock` para garantir exclusão mútua e `threading.Semaphore` para controle da posse da bola.  

- **Classe `Jogador`**  
  - Cada instância representa uma thread associada a um jogador.  
  - Aguarda sua vez de jogar através de um semáforo individual.  
  - Executa o método de registrar o toque e repassa a bola a outro jogador.  

- **Função `main()`**  
  - Solicita ao usuário o número de jogadores.  
  - Inicializa o objeto `Jogo` e cria as threads correspondentes.  
  - Aguarda o término da partida exibindo o **placar final**.  
---

## 🧠 Conceitos Envolvidos  
Este trabalho explora, de forma prática, alguns dos principais conceitos da disciplina de **Sistemas Operacionais**:  
- **Concorrência**:  
  A execução simultânea de múltiplas threads (jogadores) que compartilham recursos em comum (a bola).  
- **Exclusão Mútua**:  
  Garante que apenas um jogador tenha acesso à bola por vez. Isso é implementado com o uso de **locks (`threading.Lock`)**.  
- **Semáforos (`threading.Semaphore`)**:  
  Utilizados para controlar a vez de cada jogador. Cada thread aguarda sua liberação para executar, simulando a passagem da bola de forma controlada.  
- **Sincronização**:  
  Essencial para coordenar as jogadas e evitar condições de corrida (quando duas threads poderiam tentar acessar a bola simultaneamente).  
- **Histórico de Estados**:  
  O armazenamento dos últimos toques é um mecanismo para analisar padrões (5 toques ou tabelinha) e decidir quando um gol ocorre, simulando regras mais complexas do que um simples acesso compartilhado.  
---

## 🕹️ Execução  
1. **Certifique-se de ter o Python 3 instalado** em seu ambiente.  
2. Salve o código em um arquivo `futebol_sabao.py`.  
3. No terminal, execute:  
   ```
   python futebol_sabao.py
   ```
4. Informe o número de jogadores (deve ser par e maior que 4).
5. Acompanhe a simulação diretamente no terminal.

## 📊 Exemplo de Saída
```
GOL DO TIME 1! Tipo: 5 TOQUES
Placar: TIME 0 [3] x [4] TIME 1

GOL DO TIME 0! Tipo: TABELINHA
Placar: TIME 0 [4] x [4] TIME 1
```

## 📈 Estatísticas Finais
O código também armazena a quantidade de gols por tipo:
- Gols de 5 TOQUES.
- Gols de TABELINHA.
Esses valores podem ser exibidos ao final da execução, caso seja necessário para análise estatística da simulação.

