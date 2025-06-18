"""
Módulo responsável pela exibição e manipulação visual do tabuleiro
"""

from utils.limpar_tela import limpar_tela

class Tabuleiro:
    """Classe responsável pela exibição do tabuleiro do jogo"""
    
    def __init__(self):
        self.matriz = [[' ' for _ in range(3)] for _ in range(3)]
    
    def limpar(self):
        """Reinicia o tabuleiro com todas as posições vazias"""
        self.matriz = [[' ' for _ in range(3)] for _ in range(3)]
    
    def fazer_jogada(self, linha, coluna, jogador):
        """
        Faz uma jogada no tabuleiro
        
        Args:
            linha (int): Linha da jogada (0-2)
            coluna (int): Coluna da jogada (0-2)
            jogador (str): Símbolo do jogador ('X' ou 'O')
            
        Returns:
            bool: True se a jogada foi válida, False caso contrário
        """
        if 0 <= linha <= 2 and 0 <= coluna <= 2 and self.matriz[linha][coluna] == ' ':
            self.matriz[linha][coluna] = jogador
            return True
        return False
    
    def posicao_vazia(self, linha, coluna):
        """
        Verifica se uma posição está vazia
        
        Args:
            linha (int): Linha a verificar
            coluna (int): Coluna a verificar
            
        Returns:
            bool: True se a posição está vazia, False caso contrário
        """
        return self.matriz[linha][coluna] == ' '
    
    def obter_posicoes_vazias(self):
        """
        Retorna todas as posições vazias do tabuleiro
        
        Returns:
            list: Lista de tuplas (linha, coluna) das posições vazias
        """
        posicoes = []
        for i in range(3):
            for j in range(3):
                if self.matriz[i][j] == ' ':
                    posicoes.append((i, j))
        return posicoes
    
    def esta_cheio(self):
        """
        Verifica se o tabuleiro está completamente preenchido
        
        Returns:
            bool: True se não há posições vazias, False caso contrário
        """
        for linha in self.matriz:
            if ' ' in linha:
                return False
        return True
    
    def copiar_matriz(self):
        """
        Retorna uma cópia da matriz do tabuleiro
        
        Returns:
            list: Cópia da matriz 3x3 do tabuleiro
        """
        return [linha[:] for linha in self.matriz]
    
    def exibir(self, modo_jogo, jogador_atual, mensagem=""):
        """
        Exibe o tabuleiro na tela com informações do jogo
        
        Args:
            modo_jogo (str): Modo atual do jogo
            jogador_atual (str): Jogador atual ('X' ou 'O')
            mensagem (str): Mensagem adicional para exibir
        """
        limpar_tela()

        print("╔══════════════════════════════════════════════════════╗")
        print("║                🎮 JOGO DA VELHA COM IA 🤖            ║")
        print("╚══════════════════════════════════════════════════════╝")

        modo_texto = {
            'humano': "👥 Dois Jogadores",
            'computador': "👤 Humano (X) vs 🎲 Computador Random (O)",
            'ia': "👤 Humano (X) vs 🤖 IA Treinada (O)",
            'assistir': "🎲 Computador Random (X) vs 🤖 IA Treinada (O)",
            'treino': "🧠 Modo: Treinamento da IA"
        }
        print(f"\n{modo_texto.get(modo_jogo, 'Modo: Desconhecido')}\n")

        # Cabeçalho do tabuleiro
        print("    0   1   2")
        print("  +---+---+---+")

        # Linhas do tabuleiro
        for i in range(3):
            linha = f"{i} |"
            for j in range(3):
                valor = self.matriz[i][j] if self.matriz[i][j] != ' ' else ' '
                linha += f" {valor} |"
            print(linha)
            print("  +---+---+---+")

        print("\n📍 Legenda: X = jogador 1, O = jogador 2 ou IA")

        if mensagem:
            print(f"\n💬 {mensagem}")

        print()
        
        # Informações específicas por modo
        if modo_jogo in ['computador', 'ia'] and jogador_atual == 'O':
            tipo_oponente = "🤖 IA Treinada" if modo_jogo == 'ia' else "🎲 Computador Random"
            print(f"🎯 Vez do {tipo_oponente} ({jogador_atual}) - Pensando...")
            print("⏳ Aguarde...")
        elif modo_jogo == 'assistir':
            jogador_nome = "🎲 Computador Random" if jogador_atual == 'X' else "🤖 IA Treinada"
            print(f"🎯 Vez do {jogador_nome} ({jogador_atual}) - Pensando...")
            print("⏳ Pressione Ctrl+C para sair")
        elif modo_jogo != 'treino':
            print(f"🎯 Vez do jogador {jogador_atual}")
            print("📝 Digite: linha coluna (ex: 1 2) ou 'q' para sair")

        print("─" * 56)
    
    def exibir_menu_principal(self):
        """Exibe o menu principal do jogo"""
        limpar_tela()
        print("╔══════════════════════════════════════════════════════╗")
        print("║                🎮 JOGO DA VELHA COM IA 🤖             ║")
        print("╚══════════════════════════════════════════════════════╝")
        print()
        print("🎯 Escolha o modo de jogo:")
        print()
        print("  1️⃣  - 👥 Dois jogadores")
        print("  2️⃣  - 👤 Humano vs 🎲 Computador (aleatório)")
        print("  3️⃣  - 👤 Humano vs 🤖 IA Treinada")
        print("  4️⃣  - 👀 Assistir: 🎲 Computador Random vs 🤖 IA")
        print("  5️⃣  - 🧠 Treinar a IA")
        print()
        print("─" * 56)
    
    def exibir_tela_treinamento(self, episodio, total_episodios, epsilon, vitorias_x, vitorias_o, empates):
        """
        Exibe o progresso do treinamento
        
        Args:
            episodio (int): Episódio atual
            total_episodios (int): Total de episódios
            epsilon (float): Valor atual do epsilon
            vitorias_x (int): Número de vitórias do X
            vitorias_o (int): Número de vitórias do O
            empates (int): Número de empates
        """
        if episodio == 1:
            limpar_tela()
            print("╔══════════════════════════════════════════════════════╗")
            print("║                🧠 TREINAMENTO DA IA 🤖                ║")
            print("╚══════════════════════════════════════════════════════╝")
            print()
            print(f"🚀 Iniciando treinamento com {total_episodios:,} episódios...")
            print("⏳ Isso pode levar alguns segundos...")
            print()
            print("📊 Progresso do treinamento:")
            print("─" * 56)
        
        if episodio % 1000 == 0:
            progresso = episodio / total_episodios * 100
            barra = "█" * int(progresso / 2) + "░" * (50 - int(progresso / 2))
            
            print(f"📈 Episódio {episodio:,}/{total_episodios:,} [{barra}] {progresso:.1f}%")
            print(f"🎯 Epsilon: {epsilon:.3f}")
            print(f"📊 Últimos 1000: ❌{vitorias_x:3d} ⭕{vitorias_o:3d} 🤝{empates:3d}")
            print("─" * 56)