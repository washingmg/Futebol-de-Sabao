# Futebol de Sabão (Simulação com Threads)

## Descrição
Joãozinho e seus amigos adoram Futebol de Sabão. Cada amigo de Joãozinho é representado por **uma thread**.  
A bola sempre começa com Joãozinho, e **cada jogador só pode dar 1 toque na bola**.

### Regras do jogo
- Se **5 jogadores do mesmo time** tocarem na bola consecutivamente, **um gol acontece**.  
- Se **2 jogadores do mesmo time** trocarem passes **3 vezes alternadamente**, também é **gol**.  
- A partida **só acaba quando um time fizer 500 gols a mais que o outro**.  
- Após cada gol, o programa deve imprimir o **placar** e indicar o **tipo de gol** (por 5 toques ou por tabelinha).  
- Dois jogadores **nunca podem tocar na bola ao mesmo tempo** (controle de exclusão mútua).  
- O número total de jogadores deve ser:
  - **par**
  - **maior que 4**
  - e **informado pelo usuário** no início do programa.

## Execução
1. Compile e execute o programa.
2. Informe o número de jogadores (par e maior que 4).
3. Acompanhe a simulação do jogo no terminal com os gols e placares sendo exibidos.

---
