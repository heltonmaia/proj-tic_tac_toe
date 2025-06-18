import os
import random
import time
import pickle
from collections import defaultdict

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.9, epsilon_decay=0.995, epsilon_min=0.1):
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.alpha = alpha  # Taxa de aprendizado
        self.gamma = gamma  # Fator de desconto
        self.epsilon = epsilon  # Taxa de exploração
        self.epsilon_decay = epsilon_decay
        self.epsilon_min = epsilon_min
        
    def get_state_key(self, tabuleiro):
        """Converte o tabuleiro em uma string para usar como chave"""
        return ''.join([''.join(linha) for linha in tabuleiro])
    
    def get_valid_actions(self, tabuleiro):
        """Retorna lista de ações válidas (posições vazias)"""
        actions = []
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == ' ':
                    actions.append((i, j))
        return actions
    
    def choose_action(self, tabuleiro, training=True):
        """Escolhe uma ação usando epsilon-greedy"""
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
        """Atualiza o valor Q usando a equação de Bellman"""
        state_key = self.get_state_key(state)
        next_state_key = self.get_state_key(next_state)
        
        # Encontra o melhor valor Q do próximo estado
        next_valid_actions = self.get_valid_actions(next_state)
        max_next_q = 0
        if next_valid_actions:
            max_next_q = max([self.q_table[next_state_key][a] for a in next_valid_actions])
        
        # Atualiza Q-value
        current_q = self.q_table[state_key][action]
        self.q_table[state_key][action] = current_q + self.alpha * (reward + self.gamma * max_next_q - current_q)
    
    def decay_epsilon(self):
        """Diminui epsilon gradualmente"""
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def save_model(self, filename):
        """Salva o Q-table treinado"""
        with open(filename, 'wb') as f:
            pickle.dump(dict(self.q_table), f)
    
    def load_model(self, filename):
        """Carrega um Q-table treinado"""
        try:
            with open(filename, 'rb') as f:
                loaded_table = pickle.load(f)
                self.q_table = defaultdict(lambda: defaultdict(float), loaded_table)
            return True
        except FileNotFoundError:
            return False

class JogoDaVelha:
    def __init__(self):
        self.tabuleiro = [[' ' for _ in range(3)] for _ in range(3)]
        self.jogador_atual = 'X'
        self.modo_jogo = None
        self.jogador_humano = 'X'
        self.agente_ia = QLearningAgent()
        self.modelo_salvo = "qlearning_model.pkl"
    
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    # Substitua a sua função exibir_tela_jogo por esta:
    def exibir_tela_jogo(self, mensagem=""):
        self.limpar_tela()

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
        print(f"\n{modo_texto.get(self.modo_jogo, 'Modo: Desconhecido')}\n")

        # Cabeçalho
        print("    0   1   2")
        print("  +---+---+---+")

        for i in range(3):
            linha = f"{i} |"
            for j in range(3):
                valor = self.tabuleiro[i][j] if self.tabuleiro[i][j] != ' ' else ' '
                linha += f" {valor} |"
            print(linha)
            print("  +---+---+---+")

        print("\n📍 Legenda: X = jogador 1, O = jogador 2 ou IA")

        if mensagem:
            print(f"\n💬 {mensagem}")

        print()
        if self.modo_jogo in ['computador', 'ia'] and self.jogador_atual == 'O':
            tipo_oponente = "🤖 IA Treinada" if self.modo_jogo == 'ia' else "🎲 Computador Random"
            print(f"🎯 Vez do {tipo_oponente} ({self.jogador_atual}) - Pensando...")
            print("⏳ Aguarde...")
        elif self.modo_jogo == 'assistir':
            jogador_nome = "🎲 Computador Random" if self.jogador_atual == 'X' else "🤖 IA Treinada"
            print(f"🎯 Vez do {jogador_nome} ({self.jogador_atual}) - Pensando...")
            print("⏳ Pressione Ctrl+C para sair")
        elif self.modo_jogo != 'treino':
            print(f"🎯 Vez do jogador {self.jogador_atual}")
            print("📝 Digite: linha coluna (ex: 1 2) ou 'q' para sair")

        print("─" * 56)

    
    def fazer_jogada(self, linha, coluna):
        if self.tabuleiro[linha][coluna] == ' ':
            self.tabuleiro[linha][coluna] = self.jogador_atual
            return True
        return False
    
    def verificar_vitoria(self):
        # Verificar linhas
        for linha in self.tabuleiro:
            if linha[0] == linha[1] == linha[2] != ' ':
                return linha[0]
        
        # Verificar colunas
        for col in range(3):
            if self.tabuleiro[0][col] == self.tabuleiro[1][col] == self.tabuleiro[2][col] != ' ':
                return self.tabuleiro[0][col]
        
        # Verificar diagonais
        if self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] != ' ':
            return self.tabuleiro[0][0]
        
        if self.tabuleiro[0][2] == self.tabuleiro[1][1] == self.tabuleiro[2][0] != ' ':
            return self.tabuleiro[0][2]
        
        return None
    
    def tabuleiro_cheio(self):
        for linha in self.tabuleiro:
            if ' ' in linha:
                return False
        return True
    
    def trocar_jogador(self):
        self.jogador_atual = 'O' if self.jogador_atual == 'X' else 'X'
    
    def reiniciar_jogo(self):
        self.tabuleiro = [[' ' for _ in range(3)] for _ in range(3)]
        self.jogador_atual = 'X'
    
    def obter_posicoes_vazias(self):
        posicoes = []
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[i][j] == ' ':
                    posicoes.append((i, j))
        return posicoes
    
    def jogada_computador_aleatoria(self):
        posicoes_vazias = self.obter_posicoes_vazias()
        if posicoes_vazias:
            linha, coluna = random.choice(posicoes_vazias)
            return linha, coluna
        return None, None
    
    def jogada_ia(self):
        """Faz uma jogada usando o agente IA treinado"""
        acao = self.agente_ia.choose_action(self.tabuleiro, training=False)
        if acao:
            return acao[0], acao[1]
        return None, None
    
    def calcular_recompensa(self, vencedor, jogador):
        """Calcula a recompensa para o aprendizado"""
        if vencedor == jogador:
            return 1  # Vitória
        elif vencedor is None:
            return 0  # Empate
        else:
            return -1  # Derrota
    
    def treinar_ia(self, num_episodios=10000):
        """Treina a IA usando self-play"""
        self.limpar_tela()
        print("╔══════════════════════════════════════════════════════╗")
        print("║                🧠 TREINAMENTO DA IA 🤖                ║")
        print("╚══════════════════════════════════════════════════════╝")
        print()
        print(f"🚀 Iniciando treinamento com {num_episodios:,} episódios...")
        print("⏳ Isso pode levar alguns segundos...")
        print()
        print("📊 Progresso do treinamento:")
        print("─" * 56)
        
        vitorias_x = 0
        vitorias_o = 0
        empates = 0
        
        for episodio in range(num_episodios):
            self.reiniciar_jogo()
            estados_jogadas = []  # Para armazenar (estado, ação, jogador)
            
            while True:
                # Salva o estado atual
                estado_atual = [linha[:] for linha in self.tabuleiro]
                
                # IA escolhe uma ação
                acao = self.agente_ia.choose_action(self.tabuleiro, training=True)
                if acao is None:
                    break
                
                # Armazena a jogada
                estados_jogadas.append((estado_atual, acao, self.jogador_atual))
                
                # Executa a ação
                self.fazer_jogada(acao[0], acao[1])
                
                # Verifica se o jogo acabou
                vencedor = self.verificar_vitoria()
                if vencedor or self.tabuleiro_cheio():
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
                        proximo_estado = [linha[:] for linha in self.tabuleiro]
                        
                        self.agente_ia.update_q_value(estado, jogada, recompensa, proximo_estado)
                    
                    break
                
                self.trocar_jogador()
            
            # Decay epsilon
            self.agente_ia.decay_epsilon()
            
            # Mostra progresso
            if (episodio + 1) % 1000 == 0:
                progresso = (episodio + 1) / num_episodios * 100
                barra = "█" * int(progresso / 2) + "░" * (50 - int(progresso / 2))
                
                print(f"📈 Episódio {episodio + 1:,}/{num_episodios:,} [{barra}] {progresso:.1f}%")
                print(f"🎯 Epsilon: {self.agente_ia.epsilon:.3f}")
                print(f"📊 Últimos 1000: ❌{vitorias_x:3d} ⭕{vitorias_o:3d} 🤝{empates:3d}")
                print("─" * 56)
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
        while True:
            self.limpar_tela()
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
    
    def jogar(self):
        self.escolher_modo_jogo()
        
        # Mensagens iniciais por modo
        mensagens_iniciais = {
            'computador': "🎯 Você é ❌, computador é ⭕. Você começa!",
            'ia': "🎯 Você é ❌, IA é ⭕. Você começa! Boa sorte! 🍀",
            'assistir': "👀 Modo assistir iniciado! Preparando confronto...",
            'humano': "🎯 Jogador ❌ começa!"
        }
        
        mensagem = mensagens_iniciais.get(self.modo_jogo, "")
        
        while True:
            self.exibir_tela_jogo(mensagem)
            mensagem = ""  # Limpar mensagem após exibir
            
            # Verificar se é jogada do computador/IA
            jogada_automatica = False
            
            if self.modo_jogo == 'assistir':
                jogada_automatica = True
            elif self.modo_jogo in ['computador', 'ia'] and self.jogador_atual == 'O':
                jogada_automatica = True
            
            if jogada_automatica:
                # Jogada automática (computador ou IA)
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
                    self.fazer_jogada(linha, coluna)
                    if self.modo_jogo == 'assistir':
                        mensagem = f"{tipo_jogador} ({self.jogador_atual}) jogou na posição ({linha}, {coluna})"
                    else:
                        mensagem = f"{tipo_jogador} jogou na posição ({linha}, {coluna})"
                else:
                    mensagem = f"❌ Erro na jogada do {tipo_jogador}"
                    
            else:
                # Jogada do humano
                try:
                    entrada = input().strip().lower()
                    
                    if entrada == 'q':
                        self.limpar_tela()
                        print("Jogo encerrado. Até logo! 👋")
                        break
                    
                    if ' ' not in entrada:
                        mensagem = "❌ Digite linha e coluna separados por espaço (ex: 1 2)"
                        continue
                    
                    linha, coluna = map(int, entrada.split())
                    
                    if linha < 0 or linha > 2 or coluna < 0 or coluna > 2:
                        mensagem = "❌ Coordenadas inválidas! Use valores entre 0 e 2"
                        continue
                    
                    if not self.fazer_jogada(linha, coluna):
                        mensagem = "❌ Posição já ocupada! Tente outra"
                        continue
                    
                    mensagem = f"✅ Jogada realizada na posição ({linha}, {coluna})"
                    
                except ValueError:
                    mensagem = "❌ Digite apenas números separados por espaço!"
                    continue
                except KeyboardInterrupt:
                    self.limpar_tela()
                    print("\nJogo interrompido. Até logo! 👋")
                    break
            
            # Verificar resultado do jogo
            vencedor = self.verificar_vitoria()
            if vencedor:
                if self.modo_jogo == 'ia':
                    if vencedor == 'X':
                        resultado = "🎉 Você venceu contra a IA! Incrível! 🎉"
                    else:
                        resultado = "🤖 IA venceu! Ela aprendeu bem! 🤖"
                elif self.modo_jogo == 'computador':
                    if vencedor == 'X':
                        resultado = "🎉 Você venceu! Parabéns! 🎉"
                    else:
                        resultado = "🤖 Computador venceu! Tente novamente! 🤖"
                elif self.modo_jogo == 'assistir':
                    if vencedor == 'X':
                        resultado = "🎲 Computador Random (X) venceu! 🎲"
                    else:
                        resultado = "🤖 IA Treinada (O) venceu! 🤖"
                else:
                    resultado = f"🎉 Jogador {vencedor} venceu! 🎉"
                
                self.exibir_tela_jogo(resultado)
                if self.perguntar_novo_jogo():
                    self.reiniciar_jogo()
                    mensagem = "Novo jogo iniciado!"
                    continue
                else:
                    break
            
            if self.tabuleiro_cheio():
                self.exibir_tela_jogo("🤝 Empate! 🤝")
                if self.perguntar_novo_jogo():
                    self.reiniciar_jogo()
                    mensagem = "Novo jogo iniciado!"
                    continue
                else:
                    break
            
            self.trocar_jogador()
    
    def perguntar_novo_jogo(self):
        while True:
            resposta = input("\nDeseja jogar novamente? (s/n): ").lower().strip()
            if resposta == 's':
                return True
            elif resposta == 'n':
                self.limpar_tela()
                print("Obrigado por jogar! Até logo! 👋")
                return False
            else:
                print("Digite 's' para sim ou 'n' para não.")

    def testar_sistema(self):
        """Função para testar se o sistema está funcionando"""
        print("🔧 Testando o sistema...")
        
        # Testa criação do agente
        print("✅ Agente QLearning criado")
        
        # Testa uma jogada
        self.reiniciar_jogo()
        acao = self.agente_ia.choose_action(self.tabuleiro)
        print(f"✅ IA pode escolher ações: {acao}")
        
        # Testa salvamento
        self.agente_ia.save_model("teste.pkl")
        print("✅ Salvamento funciona")
        
        # Testa carregamento
        novo_agente = QLearningAgent()
        if novo_agente.load_model("teste.pkl"):
            print("✅ Carregamento funciona")
        
        # Remove arquivo de teste
        try:
            os.remove("teste.pkl")
        except:
            pass
            
        print("🎮 Sistema funcionando corretamente!")
        input("Pressione Enter para continuar...")

# Para iniciar o jogo, execute:
if __name__ == "__main__":
    jogo = JogoDaVelha()
    # jogo.testar_sistema()  # Descomente para testar
    jogo.jogar()
