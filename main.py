import tkinter as tk
from tkinter import filedialog, ttk
import pandas as pd

# Variável global para armazenar o DataFrame
df = None

def carregar_arquivo():
    global df


def exibir_dataframe(data_frame):
    # Lógica simplificada: Apenas imprime as primeiras linhas no console
    # Em um app real, você usaria um Treeview ou uma biblioteca como pandastable
    print("\n--- Primeiras 5 linhas do DataFrame ---")
    print(data_frame.head())
    # ... (código para Treeview/pandastable iria aqui)
    print("--------------------------------------\n")


# --- Configuração do Tkinter ---
janela = tk.Tk()
janela.title("Gerenciamento de notas")

label_nome = tk.Label(janela, text="Nome do Aluno:", font=('Arial', 12), width=20, anchor='W')
nome_insert = tk.Entry(janela, width=50, font=('Arial', 12))

label_nome.pack(pady=10)
nome_insert.pack(pady=20, padx=10) 


# Inicia o loop principal do Tkinter
janela.mainloop()