# 🧠 Entendendo o Q-Learning no Jogo da Velha

Este documento explica a lógica matemática e prática por trás da IA usada neste projeto de Jogo da Velha com Q-Learning.

---

## 🤖 O que é Q-Learning?

**Q-Learning** é um algoritmo de aprendizado por reforço que permite a um agente aprender uma política ótima de ações com base em tentativas, erros e recompensas.

---

## 🧮 A Equação de Atualização

A fórmula usada para atualizar os valores Q é:

\\[
Q(s, a) \\leftarrow Q(s, a) + \\alpha \\left[ r + \\gamma \\max_{a'} Q(s', a') - Q(s, a) \\right]
\\]

Onde:

- `s` → estado atual
- `a` → ação executada
- `r` → recompensa recebida após ação
- `s'` → próximo estado
- `α` (alpha) → taxa de aprendizado
- `γ` (gamma) → fator de desconto do futuro
- `max Q(s', a')` → melhor valor estimado da próxima jogada

---

## 🧠 Como isso é aplicado no jogo

### Estados (`s`)
São representações do tabuleiro, como uma string `'XOX O X O'`.

### Ações (`a`)
São coordenadas disponíveis no tabuleiro, como `(0, 2)`.

### Recompensas (`r`)
- Vitória: `+1`
- Derrota: `-1`
- Empate: `0`

---

## 🎲 Exploração vs Exploração

A IA usa **ε-greedy** para decidir entre:

- **Explorar** jogadas novas: com probabilidade `ε`
- **Explorar** jogadas aprendidas: com probabilidade `1 - ε`

O valor de `ε` decai com o tempo:

```python
epsilon *= epsilon_decay  # até atingir epsilon_min
```
