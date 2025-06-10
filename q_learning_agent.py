import numpy as np
import random
import pickle
import os
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
from src.game_engine import GameEngine

class QLearningAgent:
    """Agente Q-Learning para Jogo da Velha"""
    
    def __init__(self, 
                 learning_rate: float = 0.1,
                 discount_factor: float = 0.95,
                 epsilon: float = 1.0,
                 epsilon_decay: float = 0.995,
                 epsilon_min: float = 0.01,
                 player_number: int = 1,
                 use_symmetries: bool = True):
        
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        self.player_number = player_number
        self.use_symmetries = use_symmetries
        
        # Q-table: defaultdict para inicializar automaticamente com zeros
        self.q_table = defaultdict(lambda: np.zeros(9))
        
        # Estatísticas de treinamento
        self.training_stats = {
            'games_played': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'total_reward': 0.0,
            'epsilon_history': [],
            'q_table_size_history': []
        }
        
        # Histórico da partida atual para update
        self.current_episode = []
    
    def get_state_key(self, game: GameEngine) -> tuple:
        """Converte estado do jogo em chave para Q-table"""
        if self.use_symmetries:
            return game.state_to_canonical()
        else:
            return game.get_state_representation()
    
    def get_action(self, game: GameEngine, training: bool = True) -> int:
        """
        Escolhe ação usando epsilon-greedy policy
        Returns: posição (0-8) para jogar
        """
        valid_moves = game.get_valid_moves_flat()
        
        if not valid_moves:
            return None
        
        state_key = self.get_state_key(game)
        
        # Epsilon-greedy exploration
        if training and random.random() < self.epsilon:
            # Exploração: ação aleatória
            action = random.choice(valid_moves)
        else:
            # Exploração: melhor ação conhecida
            q_values = self.q_table[state_key]
            
            # Filtrar apenas ações válidas
            valid_q_values = [(q_values[move], move) for move in valid_moves]
            
            # Escolher ação com maior Q-value
            # Em caso de empate, escolher aleatoriamente
            max_q = max(valid_q_values)[0]
            best_moves = [move for q_val, move in valid_q_values if q_val == max_q]
            action = random.choice(best_moves)
        
        return action
    
    def update_q_table(self, state: tuple, action: int, reward: float, next_state: tuple, done: bool):
        """Atualiza Q-table usando equação de Bellman"""
        current_q = self.q_table[state][action]
        
        if done:
            # Estado terminal: não há próximo estado
            target_q = reward
        else:
            # Q-learning: max Q-value do próximo estado
            next_q_values = self.q_table[next_state]
            max_next_q = np.max(next_q_values) if len(next_q_values) > 0 else 0
            target_q = reward + self.discount_factor * max_next_q
        
        # Atualização Q-learning
        self.q_table[state][action] = current_q + self.learning_rate * (target_q - current_q)
    
    def start_episode(self):
        """Inicia novo episódio de treinamento"""
        self.current_episode = []
    
    def record_step(self, state: tuple, action: int, reward: float, next_state: tuple, done: bool):
        """Registra passo do episódio atual"""
        self.current_episode.append({
            'state': state,
            'action': action,
            'reward': reward,
            'next_state': next_state,
            'done': done
        })
    
    def end_episode(self, final_reward: float):
        """
        Finaliza episódio e atualiza Q-table
        Usa reward shaping para melhor aprendizado
        """
        # Atualizar estatísticas
        self.training_stats['games_played'] += 1
        self.training_stats['total_reward'] += final_reward
        
        if final_reward > 0.8:  # Vitória
            self.training_stats['wins'] += 1
        elif final_reward < -0.8:  # Derrota
            self.training_stats['losses'] += 1
        else:  # Empate
            self.training_stats['draws'] += 1
        
        # Backward pass para atualizar Q-values
        for i, step in enumerate(self.current_episode):
            # Recompensa com discount baseado na posição no episódio
            discounted_final_reward = final_reward * (self.discount_factor ** (len(self.current_episode) - i - 1))
            
            # Combinar recompensa imediata com recompensa final
            total_reward = step['reward'] + 0.1 * discounted_final_reward
            
            self.update_q_table(
                step['state'],
                step['action'],
                total_reward,
                step['next_state'],
                step['done']
            )
        
        # Decay epsilon
        self.decay_epsilon()
        
        # Registrar estatísticas
        self.training_stats['epsilon_history'].append(self.epsilon)
        self.training_stats['q_table_size_history'].append(len(self.q_table))
    
    def decay_epsilon(self):
        """Reduz epsilon (menos exploração com o tempo)"""
        self.epsilon = max(self.epsilon_min, self.epsilon * self.epsilon_decay)
    
    def set_epsilon(self, epsilon: float):
        """Define epsilon manualmente"""
        self.epsilon = max(self.epsilon_min, min(1.0, epsilon))
    
    def get_policy_strength(self, game: GameEngine) -> float:
        """
        Retorna 'força' da política atual no estado dado
        (diferença entre melhor e segunda melhor ação)
        """
        state_key = self.get_state_key(game)
        q_values = self.q_table[state_key]
        valid_moves = game.get_valid_moves_flat()
        
        if len(valid_moves) < 2:
            return 1.0
        
        valid_q_values = [q_values[move] for move in valid_moves]
        valid_q_values.sort(reverse=True)
        
        return valid_q_values[0] - valid_q_values[1]
    
    def get_win_rate(self) -> float:
        """Retorna taxa de vitória atual"""
        games = self.training_stats['games_played']
        if games == 0:
            return 0.0
        return self.training_stats['wins'] / games
    
    def get_stats_summary(self) -> dict:
        """Retorna resumo das estatísticas"""
        games = self.training_stats['games_played']
        if games == 0:
            return {'games': 0}
        
        return {
            'games_played': games,
            'win_rate': self.training_stats['wins'] / games,
            'loss_rate': self.training_stats['losses'] / games,
            'draw_rate': self.training_stats['draws'] / games,
            'avg_reward': self.training_stats['total_reward'] / games,
            'current_epsilon': self.epsilon,
            'q_table_size': len(self.q_table)
        }
    
    def save_agent(self, filepath: str):
        """Salva agente treinado em arquivo"""
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        agent_data = {
            'q_table': dict(self.q_table),  # Converter defaultdict para dict
            'training_stats': self.training_stats,
            'hyperparameters': {
                'learning_rate': self.learning_rate,
                'discount_factor': self.discount_factor,
                'epsilon': self.epsilon,
                'epsilon_decay': self.epsilon_decay,
                'epsilon_min': self.epsilon_min,
                'player_number': self.player_number,
                'use_symmetries': self.use_symmetries
            }
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(agent_data, f)
        
        print(f"Agente salvo em: {filepath}")
    
    def load_agent(self, filepath: str):
        """Carrega agente de arquivo"""
        with open(filepath, 'rb') as f:
            agent_data = pickle.load(f)
        
        # Restaurar Q-table
        self.q_table = defaultdict(lambda: np.zeros(9))
        self.q_table.update(agent_data['q_table'])
        
        # Restaurar estatísticas
        self.training_stats = agent_data['training_stats']
        
        # Restaurar hiperparâmetros
        params = agent_data['hyperparameters']
        self.learning_rate = params['learning_rate']
        self.discount_factor = params['discount_factor']
        self.epsilon = params['epsilon']
        self.epsilon_decay = params['epsilon_decay']
        self.epsilon_min = params['epsilon_min']
        self.player_number = params['player_number']
        self.use_symmetries = params['use_symmetries']
        
        print(f"Agente carregado de: {filepath}")
        print(f"Jogos treinados: {self.training_stats['games_played']}")
        print(f"Q-table size: {len(self.q_table)}")
    
    def reset_stats(self):
        """Reseta estatísticas de treinamento"""
        self.training_stats = {
            'games_played': 0,
            'wins': 0,
            'losses': 0,
            'draws': 0,
            'total_reward': 0.0,
            'epsilon_history': [],
            'q_table_size_history': []
        }
    
    def print_q_values_sample(self, n_states: int = 5):
        """Imprime amostra de Q-values para debug"""
        print(f"\n=== Amostra Q-Values (primeiros {n_states} estados) ===")
        for i, (state, q_values) in enumerate(list(self.q_table.items())[:n_states]):
            print(f"Estado {i+1}: {state}")
            print(f"Q-values: {q_values}")
            print(f"Melhor ação: {np.argmax(q_values)} (Q={np.max(q_values):.3f})")
            print("-" * 40)