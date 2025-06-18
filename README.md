# 🎮 Jogo da Velha com IA (Q-Learning)

Um projeto de **Jogo da Velha** em Python com uma **Inteligência Artificial** baseada em Q-Learning. A IA é capaz de aprender jogando contra si mesma e enfrentar humanos!

---

## 📁 Estrutura do Projeto

```

jogo\_da\_velha\_ia/
├── main.py                    # Ponto de entrada do jogo
├── agente/
│   └── qlearning.py           # Implementação do agente Q-Learning
├── jogo/
│   ├── tabuleiro.py           # Exibição e controle visual do tabuleiro
│   └── motor.py               # Lógica principal do jogo
├── modelos/
│   └── qlearning\_model.pkl    # Modelo treinado (gerado após treino)
├── utils/
│   └── limpar\_tela.py         # Função para limpar terminal
└── README.md                  # Este arquivo

````

---

## 🚀 Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/jogo-da-velha-ia.git
cd jogo-da-velha-ia
````

2. Execute o jogo:

```bash
python main.py
```

---

## 🕹️ Modos de Jogo Disponíveis

* `1️⃣` Dois jogadores humanos
* `2️⃣` Humano vs Computador Aleatório
* `3️⃣` Humano vs IA (Q-Learning)
* `4️⃣` Modo Assistir: Computador vs IA
* `5️⃣` Treinar a IA

---

## 🧠 Sobre a Inteligência Artificial

O agente usa **Q-Learning**, um algoritmo de aprendizado por reforço:

* Armazena os estados do jogo e recompensas em uma **Q-table**
* Aprende por tentativa e erro jogando contra si mesmo
* Após o treinamento, o modelo é salvo em `modelos/qlearning_model.pkl`

---

## 📦 Requisitos

* Python 3.6 ou superior
* Nenhuma dependência externa (apenas bibliotecas padrão)

---

## 📸 Exemplo da Interface

```
╔══════════════════════════════════════════════════════╗
║                🎮 JOGO DA VELHA COM IA 🤖            ║
╚══════════════════════════════════════════════════════╝

👤 Humano (X) vs 🤖 IA Treinada (O)

    0   1   2
  +---+---+---+
0 |   |   |   |
  +---+---+---+
1 |   |   |   |
  +---+---+---+
2 |   |   |   |
  +---+---+---+

📝 Digite: linha coluna (ex: 1 2) ou 'q' para sair
```

---

## 🧑‍💻 Contribuições

Contribuições são bem-vindas! Abra uma *Issue* ou envie um *Pull Request*.

---

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais detalhes.

---
