"""
Ponto de entrada principal do Jogo da Velha com IA
"""

from jogo.motor import JogoDaVelha

def main():
    """Função principal do programa"""
    jogo = JogoDaVelha()
    jogo.jogar()

if __name__ == "__main__":
    main()