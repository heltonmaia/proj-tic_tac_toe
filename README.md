# Estrutura do Projeto Q-Learning - Jogo da Velha

```
jogo_velha_ai/
│
├── main.py                    # Jogo original (seu código atual)
├── train_agent.py            # Script principal de treinamento
├── test_agent.py             # Script para testar agente treinado
├── requirements.txt          # Dependências do projeto
│
├── src/
│   ├── __init__.py
│   ├── game_engine.py        # Motor do jogo (lógica separada)
│   ├── q_learning_agent.py   # Implementação do agente Q-Learning
│   ├── opponents.py          # Diferentes tipos de oponentes
│   ├── trainer.py           # Gerenciador de treinamento
│   └── utils.py             # Funções utilitárias
│
├── data/
│   ├── q_tables/            # Q-tables salvas
│   │   ├── agent_fase1.pkl
│   │   ├── agent_fase2.pkl
│   │   └── agent_final.pkl
│   └── logs/                # Logs de treinamento
│       ├── training_fase1.log
│       ├── training_fase2.log
│       └── training_fase3.log
│
├── results/
│   ├── plots/               # Gráficos de performance
│   └── metrics/             # Métricas de avaliação
│
└── config/
    └── training_config.yaml # Configurações de treinamento
```

## Arquivos Principais:

### 1. **game_engine.py**
- Lógica pura do jogo (sem interface)
- Métodos para verificar vitória, empate, jogadas válidas
- Representação de estado otimizada

### 2. **q_learning_agent.py**
- Implementação completa do Q-Learning
- Métodos para salvar/carregar Q-table
- Decay do epsilon automático

### 3. **opponents.py**
- OpponenteAleatorio
- OpponenteDefensivo  
- OpponenteAgressivo
- OpponenteMinimax
- OpponenteAdaptativo (muda estratégia baseado em fase)

### 4. **trainer.py**
- Gerencia as 3 fases de treinamento
- Coleta métricas de performance
- Salva checkpoints automáticos
- Gera logs detalhados

### 5. **train_agent.py**
- Script principal que orquestra todo o treinamento
- Configura as fases
- Chama avaliações periódicas

## Fluxo de Treinamento:

```
Fase 1 (0-10k)    → Salva checkpoint → Avaliação
    ↓
Fase 2 (10k-30k)  → Salva checkpoint → Avaliação  
    ↓
Fase 3 (30k-50k)  → Salva modelo final → Avaliação final
```

## Como Usar:

```bash
# Instalar dependências
pip install -r requirements.txt

# Treinar agente (processo completo)
python train_agent.py

# Testar agente treinado
python test_agent.py

# Jogar contra agente treinado
python main.py --mode vs_ai
```

## Configuração YAML:

```yaml
training:
  fase1:
    episodios: 10000
    epsilon_start: 1.0
    epsilon_end: 0.3
    oponente: "aleatorio"
    
  fase2:
    episodios: 20000
    epsilon_start: 0.3
    epsilon_end: 0.1
    oponente: "misto_defensivo"
    
  fase3:
    episodios: 20000
    epsilon_start: 0.1
    epsilon_end: 0.01
    oponente: "misto_avancado"

agent:
  learning_rate: 0.1
  discount_factor: 0.95
  
logging:
  save_interval: 1000
  eval_interval: 5000
```