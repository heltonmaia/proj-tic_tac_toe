# utils/limpar_tela.py

import os

def limpar_tela():
    """Limpa o terminal, compatível com Windows e Unix"""
    os.system('cls' if os.name == 'nt' else 'clear')
