"""
Motor principal do jogo - Lógica de controle e fluxo do Jogo da Velha
"""

import random
import time
import os

from agente.qlearning import QLearningAgent
from jogo.tabuleiro import Tabuleiro

class JogoDaVelha:
    """Classe principal que controla a lógica do Jogo da Velha"""
    
    def __init__(self):
        self.tabuleiro = Tabuleiro()
        self.jogador_atual = 'X'
        self.modo_jogo = None
        self.agente_ia = QLearningAgent()
        self.modelo_salvo = "modelos/qlearning_model.pkl"
        
        # Criar diretório de modelos se não existir
        os.makedirs("modelos", exist_ok=True)
    
    def verificar_vitoria(self):
        """
        Verifica se há um vencedor no jogo
        
        Returns:
            str or None: Símbolo do vencedor ('X' ou 'O') ou None se não há vencedor
        """
        matriz = self.tabuleiro.matriz
        
        # Verificar linhas
        for linha in matriz:
            if linha[0] == linha[1] == linha[2] != ' ':
                return linha[0]
        
        # Verificar colunas
        for col in range(3):
            if matriz[0][col] == matriz[1][col] == matriz[2][col] != ' ':
                return matriz[0][col]
        
        # Verificar diagonais
        if matriz[0][0] == matriz[1][1] == matriz[2][2] != ' ':
            return matriz[0][0]
        
        if matriz[0][2] == matriz[1][1] == matriz[2][0] != ' ':
            return matriz[0][2]
        
        return None
    
    def trocar_jogador(self):
        """Alterna entre os jogadores X e O"""
        self.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'
    
    def reiniciar_jogo(self):
        """Reinicia o jogo para um novo round"""
        self.tabuleiro.limpar()
        self.jogador_atual = 'X'
    
    def jogada_computador_aleatoria(self):
        """
        Faz uma jogada aleatória para o computador
        
        Returns:
            tuple: (linha, coluna) da jogada ou (None, None) se não há jogadas possíveis
        """
        posicoes_vazias = self.tabuleiro.obter_posicoes_vazias()
        if posicoes_vazias:
            linha, coluna = random.choice(posicoes_vazias)
            return linha, coluna
        return None, None
    
    def jogada_ia(self):
        """
        Faz uma jogada usando o agente IA treinado
        
        Returns:
            tuple: (linha, coluna) da jogada ou (None, None) se não há jogadas possíveis
        """
        acao = self.agente_ia.choose_action(self.tabuleiro.matriz, training=False)
        if acao:
            return acao[0], acao[1]
        return None, None
    
    def calcular_recompensa(self, vencedor, jogador):
        """
        Calcula a recompensa para o aprendizado por reforço
        
        Args:
            vencedor (str or None): Símbolo do vencedor ou None para empate
            jogador (str): Símbolo do jogador para calcular recompensa
            
        Returns:
            float: Recompensa calculada (1 para vitória, 0 para empate, -1 para derrota)
        """
        if vencedor == jogador:
            return 1  # Vitória
        elif vencedor is None:
            return 0  # Empate
        else:
            return -1  # Derrota
    
    def treinar_ia(self, num_episodios=10000):
        """
        Treina a IA usando self-play com Q-Learning
        
        Args:
            num_episodios (int): Número de episódios de treinamento
        """
        vitorias_x = 0
        vitorias_o = 0
        empates = 0
        
        for episodio in range(1, num_episodios + 1):
            self.reiniciar_jogo()
            estados_jogadas = []  # Para armazenar (estado, ação, jogador)
            
            while True:
                # Salva o estado atual
                estado_atual = self.tabuleiro.copiar_matriz()
                
                # IA escolhe uma ação
                acao = self.agente_ia.choose_action(self.tabuleiro.matriz, training=True)
                if acao is None:
                    break
                
                # Armazena a jogada
                estados_jogadas.append((estado_atual, acao, self.jogador_atual))
                
                # Executa a ação
                self.tabuleiro.fazer_jogada(acao[0], acao[1], self.jogador_atual)
                
                # Verifica se o jogo acabou
                vencedor = self.verificar_vitoria()
                if vencedor or self.tabuleiro.esta_cheio():
                    # Atualiza contadores
                    if vencedor == 'X':
                        vitorias_x += 1
                    elif vencedor == 'O':
                        vitorias_o += 1
                    else:
                        empates += 1
                    
                    # Atualiza Q-values para todas as jogadas do episódio
                    for i, (estado, jogada, jogador) in enumerate(estados_jogadas):
                        recompensa = self.calcular_recompensa(vencedor, jogador)
                        
                        # Estado seguinte (estado atual do tabuleiro)
                        proximo_estado = self.tabuleiro.copiar_matriz()
                        
                        self.agente_ia.update_q_value(estado, jogada, recompensa, proximo_estado)
                    
                    break
                
                self.trocar_jogador()
            
            # Decay epsilon
            self.agente_ia.decay_epsilon()
            
            # Mostra progresso
            self.tabuleiro.exibir_tela_treinamento(
                episodio, num_episodios, self.agente_ia.epsilon,
                vitorias_x, vitorias_o, empates
            )
            
            if episodio % 1000 == 0:
                vitorias_x = vitorias_o = empates = 0
        
        # Salva o modelo treinado
        self.agente_ia.save_model(self.modelo_salvo)
        print()
        print("🎉 Treinamento concluído com sucesso!")
        print(f"💾 Modelo salvo em: {self.modelo_salvo}")
        print(f"🧠 Q-table contém {len(self.agente_ia.q_table):,} estados aprendidos")
        print("─" * 56)
        input("✨ Pressione Enter para continuar...")
    
    def escolher_modo_jogo(self):
        """Menu para escolher o modo de jogo"""
        while True:
            self.tabuleiro.exibir_menu_principal()
            
            try:
                escolha = input("\nDigite sua escolha (1-5): ").strip()
                
                if escolha == '1':
                    self.modo_jogo = 'humano'
                    return
                elif escolha == '2':
                    self.modo_jogo = 'computador'
                    return
                elif escolha == '3':
                    # Tenta carregar o modelo treinado
                    if self.agente_ia.load_model(self.modelo_salvo):
                        print(f"✅ Modelo carregado de {self.modelo_salvo}")
                        time.sleep(1)
                        self.modo_jogo = 'ia'
                        return
                    else:
                        print(f"❌ Modelo não encontrado! Treine a IA primeiro (opção 5)")
                        input("Pressione Enter para continuar...")
                        continue
                elif escolha == '4':
                    # Verifica se tem IA treinada para o modo assistir
                    if self.agente_ia.load_model(self.modelo_salvo):
                        print(f"✅ IA carregada para modo assistir")
                        time.sleep(1)
                        self.modo_jogo = 'assistir'
                        return
                    else:
                        print(f"❌ IA não treinada! Treine primeiro (opção 5) para assistir IA vs Computador")
                        input("Pressione Enter para continuar...")
                        continue
                elif escolha == '5':
                    self.treinar_ia()
                    # Após treinar, pergunta se quer jogar contra a IA
                    print("\n🎮 Quer testar a IA treinada agora?")
                    resposta = input("Digite 's' para jogar ou Enter para voltar ao menu: ").lower().strip()
                    if resposta == 's':
                        print("🎮 Carregando jogo contra IA...")
                        time.sleep(1)
                        self.reiniciar_jogo()
                        self.modo_jogo = 'ia'
                        return
                    continue  # Volta ao menu
                else:
                    print("❌ Digite apenas números de 1 a 5")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\nJogo encerrado. Até logo! 👋")
                exit()
            except ValueError:
                print("❌ Digite apenas números!")
                time.sleep(1)
    
    def processar_jogada_humana(self):
        """
        Processa a entrada do jogador humano
        
        Returns:
            tuple: (sucesso, linha, coluna, mensagem)
        """
        try:
            entrada = input().strip().lower()
            
            if entrada == 'q':
                return False, None, None, "quit"
            
            if ' ' not in entrada:
                return False, None, None, "❌ Digite linha e coluna separados por espaço (ex: 1 2)"
            
            linha, coluna = map(int, entrada.split())
            
            if linha < 0 or linha > 2 or coluna < 0 or coluna > 2:
                return False, None, None, "❌ Coordenadas inválidas! Use valores entre 0 e 2"
            
            if not self.tabuleiro.posicao_vazia(linha, coluna):
                return False, None, None, "❌ Posição já ocupada! Tente outra"
            
            return True, linha, coluna, f"✅ Jogada realizada na posição ({linha}, {coluna})"
            
        except ValueError:
            return False, None, None, "❌ Digite apenas números separados por espaço!"
        except KeyboardInterrupt:
            return False, None, None, "interrupt"
    
    def executar_jogada_automatica(self):
        """
        Executa jogada automática (computador ou IA)
        
        Returns:
            tuple: (linha, coluna, mensagem)
        """
        time.sleep(1.5)  # Pausa para simular "pensamento"
        
        if self.modo_jogo == 'ia':
            linha, coluna = self.jogada_ia()
            tipo_jogador = "🤖 IA"
        elif self.modo_jogo == 'assistir':
            if self.jogador_atual == 'X':
                # X é sempre computador aleatório no modo assistir
                linha, coluna = self.jogada_computador_aleatoria()
                tipo_jogador = "🎲 Computador Random"
            else:
                # O é sempre IA no modo assistir
                linha, coluna = self.jogada_ia()
                tipo_jogador = "🤖 IA Treinada"
        else:
            linha, coluna = self.jogada_computador_aleatoria()
            tipo_jogador = "🤖 Computador"
        
        if linha is not None:
            mensagem = f"{tipo_jogador} jogou na posição ({linha}, {coluna})"
            if self.modo_jogo != 'assistir':
                mensagem = f"{tipo_jogador} jogou na posição ({linha}, {coluna})"
            else:
                mensagem = f"{tipo_jogador} ({self.jogador_atual}) jogou na posição ({linha}, {coluna})"
        else:
            mensagem = f"❌ Erro na jogada do {tipo_jogador}"
            
        return linha, coluna, mensagem
    
    def perguntar_novo_jogo(self):
        """
        Pergunta se o usuário quer jogar novamente
        
        Returns:
            bool: True se quer jogar novamente, False caso contrário
        """
        while True:
            resposta = input("\nDeseja jogar novamente? (s/n): ").lower().strip()
            if resposta == 's':
                return True
            elif resposta == 'n':
                from utils.limpar_tela import limpar_tela
                limpar_tela()
                print("Obrigado por jogar! Até logo! 👋")
                return False
            else:
                print("Digite 's' para sim ou 'n' para não.")
    
    def jogar(self):
        """Método principal que controla o fluxo do jogo"""
        self.escolher_modo_jogo()

        # Mensagens iniciais por modo
        mensagens_iniciais = {
            'computador': "🎯 Você é ❌, computador é ⭕. Você começa!",
            'ia': "🎯 Você é ❌, IA é ⭕. Você começa!",
            'humano': "🎯 Jogador ❌ começa!",
            'assistir': "👀 Assistindo: 🎲 Computador Random vs 🤖 IA Treinada"
        }

        if self.modo_jogo in mensagens_iniciais:
            print(mensagens_iniciais[self.modo_jogo])
            time.sleep(2)

        while True:
            self.tabuleiro.exibir(self.modo_jogo, self.jogador_atual)

            if self.modo_jogo in ['computador', 'ia', 'assistir'] and self.jogador_atual == 'O':
                linha, coluna, mensagem = self.executar_jogada_automatica()
            elif self.modo_jogo == 'assistir' and self.jogador_atual == 'X':
                linha, coluna, mensagem = self.executar_jogada_automatica()
            else:
                sucesso, linha, coluna, mensagem = self.processar_jogada_humana()
                if not sucesso and mensagem == "quit":
                    print("👋 Jogo encerrado pelo jogador.")
                    break
                elif not sucesso and mensagem == "interrupt":
                    print("⛔ Interrompido.")
                    break
                elif not sucesso:
                    print(mensagem)
                    time.sleep(1)
                    continue

            if linha is not None and coluna is not None:
                self.tabuleiro.fazer_jogada(linha, coluna, self.jogador_atual)

            vencedor = self.verificar_vitoria()
            if vencedor or self.tabuleiro.esta_cheio():
                self.tabuleiro.exibir(self.modo_jogo, self.jogador_atual, f"🎉 Vitória de {vencedor}!" if vencedor else "🤝 Empate!")
                if not self.perguntar_novo_jogo():
                    break
                self.reiniciar_jogo()
                continue

            self.trocar_jogador()
