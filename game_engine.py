import numpy as np
from typing import List, Tuple, Optional, Union

class GameEngine:
    """Motor do jogo da velha - lógica pura sem interface"""
    
    def __init__(self):
        self.reset_game()
    
    def reset_game(self):
        """Reinicia o jogo"""
        self.board = np.zeros((3, 3), dtype=int)  # 0=vazio, 1=X, 2=O
        self.current_player = 1  # X sempre começa
        self.game_over = False
        self.winner = None
        self.move_history = []
    
    def get_state_representation(self) -> tuple:
        """Retorna representação do estado para Q-Learning"""
        return tuple(self.board.flatten())
    
    def get_state_string(self) -> str:
        """Retorna estado como string legível"""
        symbols = {0: ' ', 1: 'X', 2: 'O'}
        return ''.join([symbols[cell] for cell in self.board.flatten()])
    
    def get_valid_moves(self) -> List[Tuple[int, int]]:
        """Retorna lista de jogadas válidas (linha, coluna)"""
        moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i, j] == 0:
                    moves.append((i, j))
        return moves
    
    def get_valid_moves_flat(self) -> List[int]:
        """Retorna jogadas válidas como índices 0-8"""
        moves = []
        for i in range(9):
            row, col = i // 3, i % 3
            if self.board[row, col] == 0:
                moves.append(i)
        return moves
    
    def make_move(self, row: int, col: int) -> bool:
        """
        Faz uma jogada
        Returns: True se jogada válida, False caso contrário
        """
        if self.game_over or self.board[row, col] != 0:
            return False
        
        self.board[row, col] = self.current_player
        self.move_history.append((row, col, self.current_player))
        
        # Verificar fim de jogo
        self._check_game_end()
        
        if not self.game_over:
            self.current_player = 2 if self.current_player == 1 else 1
        
        return True
    
    def make_move_flat(self, position: int) -> bool:
        """Faz jogada usando índice 0-8"""
        row, col = position // 3, position % 3
        return self.make_move(row, col)
    
    def _check_game_end(self):
        """Verifica se o jogo terminou"""
        # Verificar vitória
        winner = self._check_winner()
        if winner:
            self.game_over = True
            self.winner = winner
            return
        
        # Verificar empate
        if len(self.get_valid_moves()) == 0:
            self.game_over = True
            self.winner = 0  # Empate
    
    def _check_winner(self) -> Optional[int]:
        """
        Verifica se há um vencedor
        Returns: 1 (X), 2 (O), ou None
        """
        # Verificar linhas
        for row in self.board:
            if row[0] == row[1] == row[2] != 0:
                return row[0]
        
        # Verificar colunas
        for col in range(3):
            if self.board[0, col] == self.board[1, col] == self.board[2, col] != 0:
                return self.board[0, col]
        
        # Verificar diagonais
        if self.board[0, 0] == self.board[1, 1] == self.board[2, 2] != 0:
            return self.board[0, 0]
        
        if self.board[0, 2] == self.board[1, 1] == self.board[2, 0] != 0:
            return self.board[0, 2]
        
        return None
    
    def is_terminal_state(self) -> bool:
        """Verifica se é estado terminal"""
        return self.game_over
    
    def get_result(self, player: int) -> str:
        """
        Retorna resultado do jogo para um jogador específico
        Returns: 'win', 'lose', 'draw', 'ongoing'
        """
        if not self.game_over:
            return 'ongoing'
        
        if self.winner == 0:
            return 'draw'
        elif self.winner == player:
            return 'win'
        else:
            return 'lose'
    
    def get_reward(self, player: int) -> float:
        """
        Calcula recompensa para um jogador
        """
        result = self.get_result(player)
        
        if result == 'win':
            return 1.0
        elif result == 'lose':
            return -1.0
        elif result == 'draw':
            return 0.5
        else:
            return -0.01  # Pequena penalidade por jogada (incentiva jogos rápidos)
    
    def copy(self) -> 'GameEngine':
        """Cria cópia do estado atual do jogo"""
        new_game = GameEngine()
        new_game.board = self.board.copy()
        new_game.current_player = self.current_player
        new_game.game_over = self.game_over
        new_game.winner = self.winner
        new_game.move_history = self.move_history.copy()
        return new_game
    
    def display_board(self) -> str:
        """Retorna representação visual do tabuleiro"""
        symbols = {0: ' ', 1: 'X', 2: 'O'}
        lines = []
        lines.append("   0   1   2")
        for i in range(3):
            row_str = f"{i}  {symbols[self.board[i,0]]} | {symbols[self.board[i,1]]} | {symbols[self.board[i,2]]}"
            lines.append(row_str)
            if i < 2:
                lines.append("  -----------")
        return '\n'.join(lines)
    
    def get_symmetries(self) -> List[np.ndarray]:
        """
        Retorna todas as simetrias do tabuleiro atual
        (rotações e reflexões) para otimização do Q-Learning
        """
        symmetries = []
        board = self.board
        
        # Rotações
        for k in range(4):
            symmetries.append(np.rot90(board, k))
        
        # Reflexões das rotações
        for k in range(4):
            symmetries.append(np.fliplr(np.rot90(board, k)))
        
        return symmetries
    
    def state_to_canonical(self) -> tuple:
        """
        Converte estado atual para forma canônica
        (menor representação lexicográfica entre todas as simetrias)
        """
        symmetries = self.get_symmetries()
        canonical = min([tuple(sym.flatten()) for sym in symmetries])
        return canonical