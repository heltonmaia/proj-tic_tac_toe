import os
import random
import time

class JogoDaVelha:
    def __init__(self):
        self.tabuleiro = [[' ' for _ in range(3)] for _ in range(3)]
        self.jogador_atual = 'X'
        self.modo_jogo = None  # 'humano' ou 'computador' ou 'assistir'
        self.jogador_humano = 'X'  # Sempre X para o humano
    
    def limpar_tela(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def exibir_tela_jogo(self, mensagem=""):
        self.limpar_tela()
        print("=== JOGO DA VELHA ===")
        if self.modo_jogo == 'computador':
            print("Modo: Humano (X) vs Computador (O)")
        elif self.modo_jogo == 'assistir':
            print("Modo: Assistir - Computador X vs Computador O")
        else:
            print("Modo: Dois Jogadores")
        print("   0   1   2")
        for i in range(3):
            print(f"{i}  {self.tabuleiro[i][0]} | {self.tabuleiro[i][1]} | {self.tabuleiro[i][2]}")
            if i < 2:
                print("  -----------")
        
        if mensagem:
            print(f"\n{mensagem}")
        
        if self.modo_jogo == 'computador' and self.jogador_atual == 'O':
            print(f"\nVez do Computador (O) - Pensando...")
        elif self.modo_jogo == 'assistir':
            print(f"\nVez do Computador {self.jogador_atual} - Pensando...")
            print("Pressione Ctrl+C para sair")
        else:
            print(f"\nVez do jogador {self.jogador_atual}")
            print("Digite a linha e coluna separando por espaço (0-2) ou 'q' para sair:")
    
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
    
    def jogada_computador(self):
        posicoes_vazias = self.obter_posicoes_vazias()
        if posicoes_vazias:
            linha, coluna = random.choice(posicoes_vazias)
            return linha, coluna
        return None, None
    
    def escolher_modo_jogo(self):
        self.limpar_tela()
        print("=== JOGO DA VELHA ===")
        print("\nEscolha o modo de jogo:")
        print("1 - Dois jogadores")
        print("2 - Humano vs Computador")
        print("3 - Assistir: Computador vs Computador")
        
        while True:
            try:
                escolha = input("\nDigite sua escolha (1, 2 ou 3): ").strip()
                if escolha == '1':
                    self.modo_jogo = 'humano'
                    return
                elif escolha == '2':
                    self.modo_jogo = 'computador'
                    return
                elif escolha == '3':
                    self.modo_jogo = 'assistir'
                    return
                else:
                    print("❌ Digite apenas 1, 2 ou 3")
            except KeyboardInterrupt:
                print("\nJogo encerrado. Até logo! 👋")
                exit()
    
    def jogar(self):
        self.escolher_modo_jogo()
        
        if self.modo_jogo == 'computador':
            mensagem = "Você é X, computador é O. Você começa!"
        elif self.modo_jogo == 'assistir':
            mensagem = "Modo assistir iniciado! Computadores jogando..."
        else:
            mensagem = "Jogador X começa!"
        
        while True:
            self.exibir_tela_jogo(mensagem)
            mensagem = ""  # Limpar mensagem após exibir
            
            # Verificar se é jogada do computador
            jogada_computador = False
            
            if self.modo_jogo == 'assistir':
                # No modo assistir, ambos os jogadores são computador
                jogada_computador = True
            elif self.modo_jogo == 'computador' and self.jogador_atual == 'O':
                # No modo humano vs computador, apenas O é computador
                jogada_computador = True
            
            if jogada_computador:
                # Jogada do computador
                time.sleep(1.5)  # Pausa para simular "pensamento"
                linha, coluna = self.jogada_computador()
                if linha is not None:
                    self.fazer_jogada(linha, coluna)
                    if self.modo_jogo == 'assistir':
                        mensagem = f"🤖 Computador {self.jogador_atual} jogou na posição ({linha}, {coluna})"
                    else:
                        mensagem = f"🤖 Computador jogou na posição ({linha}, {coluna})"
                else:
                    mensagem = "❌ Erro na jogada do computador"
                    
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
                if self.modo_jogo == 'computador':
                    if vencedor == 'X':
                        resultado = "🎉 Você venceu! Parabéns! 🎉"
                    else:
                        resultado = "🤖 Computador venceu! Tente novamente! 🤖"
                elif self.modo_jogo == 'assistir':
                    resultado = f"🎉 Computador {vencedor} venceu! 🎉"
                else:
                    resultado = f"🎉 Jogador {vencedor} venceu! 🎉"
                
                self.exibir_tela_jogo(resultado)
                if self.perguntar_novo_jogo():
                    self.reiniciar_jogo()
                    if self.modo_jogo == 'computador':
                        mensagem = "Novo jogo! Você começa!"
                    elif self.modo_jogo == 'assistir':
                        mensagem = "Novo jogo! Computadores jogando..."
                    else:
                        mensagem = "Novo jogo iniciado! Jogador X começa!"
                    continue
                else:
                    break
            
            if self.tabuleiro_cheio():
                self.exibir_tela_jogo("🤝 Empate! 🤝")
                if self.perguntar_novo_jogo():
                    self.reiniciar_jogo()
                    if self.modo_jogo == 'computador':
                        mensagem = "Novo jogo! Você começa!"
                    elif self.modo_jogo == 'assistir':
                        mensagem = "Novo jogo! Computadores jogando..."
                    else:
                        mensagem = "Novo jogo iniciado! Jogador X começa!"
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

# Para iniciar o jogo, execute:
if __name__ == "__main__":
    jogo = JogoDaVelha()
    jogo.jogar()