"""
Implementação do agente QLearning para jogar Jogo da Velha
"""

import random
import pickle
from collections import defaultdict

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.9, epsilon_decay=0.995, epsilon_min=0.1):
        """
        Inicializa o agente de Q-Learning
        
        Args:
            alpha (float): Taxa de aprendizado
            gamma (float): Fator de desconto
            epsilon (float): Taxa de exploração inicial
            epsilon_decay (float): Taxa de decaimento do epsilon
            epsilon_min (float): Valor mínimo do epsilon
        """
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
    def get_state_key(self, tabuleiro):
        """
        Converte o tabuleiro em uma string para usar como chave
        
        Args:
            tabuleiro (list): Matriz 3x3 representando o tabuleiro
            
        Returns:
            str: Representação string do estado do tabuleiro
        """
        return ''.join([''.join(linha) for linha in tabuleiro])
    
    def get_valid_actions(self, tabuleiro):
        """
        Retorna lista de ações válidas (posições vazias)
        
        Args:
            tabuleiro (list): Matriz 3x3 representando o tabuleiro
            
        Returns:
            list: Lista de tuplas (linha, coluna) das posições vazias
        """
        actions = []
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == ' ':
                    actions.append((i, j))
        return actions
    
    def choose_action(self, tabuleiro, training=True):
        """
        Escolhe uma ação usando estratégia epsilon-greedy
        
        Args:
            tabuleiro (list): Estado atual do tabuleiro
            training (bool): Se True, usa exploração; se False, usa apenas exploração
            
        Returns:
            tuple: (linha, coluna) da ação escolhida ou None se não há ações válidas
        """
        valid_actions = self.get_valid_actions(tabuleiro)
        if not valid_actions:
            return None
        
        state_key = self.get_state_key(tabuleiro)
        
        # Durante o treinamento, usa epsilon-greedy
        if training and random.random() < self.epsilon:
            return random.choice(valid_actions)
        
        # Escolhe a melhor ação conhecida
        best_action = None
        best_value = float('-inf')
        
        for action in valid_actions:
            q_value = self.q_table[state_key][action]
            if q_value > best_value:
                best_value = q_value
                best_action = action
        
        return best_action if best_action else random.choice(valid_actions)
    
    def update_q_value(self, state, action, reward, next_state):
        """
        Atualiza o valor Q usando a equação de Bellman
        
        Args:
            state (list): Estado atual do tabuleiro
            action (tuple): Ação tomada (linha, coluna)
            reward (float): Recompensa recebida
            next_state (list): Próximo estado do tabuleiro
        """
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        
        # Encontra o melhor valor Q do próximo estado
        next_valid_actions = self.get_valid_actions(next_state)
        max_next_q = 0
        if next_valid_actions:
            max_next_q = max([self.q_table[next_state_key][a] for a in next_valid_actions])
        
        # Atualiza Q-value usando a equação de Bellman
        current_q = self.q_table[state_key][action]
        self.q_table[state_key][action] = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
    
    def decay_epsilon(self):
        """Diminui epsilon gradualmente durante o treinamento"""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def save_model(self, filename):
        """
        Salva o Q-table treinado em arquivo
        
        Args:
            filename (str): Caminho do arquivo para salvar
        """
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.q_table), f)
    
    def load_model(self, filename):
        """
        Carrega um Q-table treinado de arquivo
        
        Args:
            filename (str): Caminho do arquivo para carregar
            
        Returns:
            bool: True se carregado com sucesso, False caso contrário
        """
        try:
            with open(filename, 'rb') as f:
                loaded_table = pickle.load(f)
                self.q_table = defaultdict(lambda: defaultdict(float), loaded_table)
            return True
        except FileNotFoundError:
            return False
    
    def get_stats(self):
        """
        Retorna estatísticas do agente
        
        Returns:
            dict: Dicionário com estatísticas do agente
        """
        return {
            'num_states': len(self.q_table),
            'epsilon': self.epsilon,
            'alpha': self.alpha,
            'gamma': self.gamma
        }