import tkinter as tk
import sys
from tkinter import filedialog, ttk, messagebox
import pandas as pd

print(sys.executable)

# --- Configuração do Tkinter ---
janela = tk.Tk()
janela.title("Gerenciamento de notas")

campos = ["Nome", "Idade", "Curso", "Nota Final"]
entries = []

for campo in campos:
    tk.Label(janela, text=f"{campo}:", font=('Arial', 8)).pack(anchor='w', padx=10, pady=(10, 0))
    entry = tk.Entry(janela, width=55, font=('Arial', 12), highlightthickness=1, highlightbackground="grey", highlightcolor="black")
    entry.pack(anchor='w', padx=10, pady=5)
    entries.append(entry)

todos_dados = []  # Lista para armazenar todos os dados

def salvar_dados():
    valores = [entry.get() for entry in entries]   # Pega valores dos Entry
    tabela.insert("", tk.END, values=valores)      # Insere na tabela
    todos_dados.append(valores)                    # Guarda na lista todos_dados para filtrar
    for entry in entries:
        entry.delete(0, tk.END)                    # Limpa os campos

# --- Função para filtrar ---
def aplicar_filtro(event=None):
    tipo = filtro_var.get()  # pega a opção selecionada no combobox
    tabela.delete(*tabela.get_children())  # limpa a tabela
    for item in todos_dados:
        try:
            nota = float(item[3])
        except ValueError:
            continue
        if tipo == "Notas Baixas" and nota <= 5:
            tabela.insert("", tk.END, values=item)
        elif tipo == "Notas Regulares" and 5 < nota <= 6.9:
            tabela.insert("", tk.END, values=item)
        elif tipo == "Notas Boas" and nota >= 7:
            tabela.insert("", tk.END, values=item)
        elif tipo == "Todas":
            tabela.insert("", tk.END, values=item)

def exportar_csv_filtrado():
    # Pega apenas os itens atualmente exibidos na tabela
    linhas = []
    for row_id in tabela.get_children():
        linhas.append(tabela.item(row_id)['values'])

    if not linhas:
        tk.messagebox.showwarning("Aviso", "Não há dados para exportar!")
        return

    arquivo = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivos CSV", "*.csv")],
        title="Salvar tabela filtrada como CSV"
    )
    if arquivo:
        # Cria DataFrame apenas com os dados filtrados
        df = pd.DataFrame(linhas, columns=["Nome", "Idade", "Curso", "Nota Final"])
        df.to_csv(arquivo, index=False, encoding='utf-8')
        tk.messagebox.showinfo("Exportar CSV", f"Tabela filtrada exportada com sucesso para:\n{arquivo}")

def importar_tabela():
    arquivo = filedialog.askopenfilename(
        # Mantenha a filtragem de tipos de arquivo na caixa de diálogo
        filetypes=[("Arquivos CSV", "*.csv"), ("Arquivos Excel", "*.xlsx *.xls")],
        title="Abrir tabela"
    )
    if not arquivo:
        return # usuário cancelou

    try:
        caminho_baixo = arquivo.lower()
        
        # 1. Tenta ler CSV
        if caminho_baixo.endswith(".csv"):
            df = pd.read_csv(arquivo) 

        else:
            tk.messagebox.showwarning("Aviso", "Formato de arquivo não suportado.")
            return

        # Limpa e popula a tabela
        tabela.delete(*tabela.get_children())
        todos_dados.clear()

        # Insere os dados na tabela e na lista todos_dados
        for _, row in df.iterrows():
            # Certifique-se que os nomes das colunas (keys) estão corretos
            valores = [row["Nome"], row["Idade"], row["Curso"], row["Nota Final"]]
            tabela.insert("", tk.END, values=valores)
            todos_dados.append(valores)

        tk.messagebox.showinfo("Importar Tabela", f"Tabela importada com sucesso de:\n{arquivo}")

    except KeyError:
        # Se o arquivo não tiver as colunas esperadas
        tk.messagebox.showerror("Erro", "O arquivo importado não possui as colunas necessárias (Nome, Idade, Curso, Nota Final).")
    except Exception as e:
        tk.messagebox.showerror("Erro", f"Não foi possível importar o arquivo:\n{e}")

# --- Botões ---
# Cria um frame para alinhar horizontalmente
frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)  # coloca o frame na janela principal

# Botão salvar
btn_salvar = tk.Button(frame_botoes, text="Salvar", command=salvar_dados, 
                    bg="#4CAF50", 
                    fg="white", 
                    activebackground="#45a049", 
                    activeforeground="white",
                    font=("Arial", 10, "bold"),
                    padx=8, pady=3,               # padding interno
                    bd=0,                            # remove borda padrão
                    relief="flat")                   # estilo da borda

btn_salvar.pack(side="left", padx=5)  # lado esquerdo do frame, com espaçamento


btn_exportar = tk.Button(frame_botoes, text="Exportar CSV", command=exportar_csv_filtrado,
                    bg="#652EAD", 
                    fg="white", 
                    activebackground="#7B53AF", 
                    activeforeground="white",
                    font=("Arial", 10, "bold"),
                    padx=8, pady=3,               # padding interno
                    bd=0,                            # remove borda padrão
                    relief="flat")
btn_exportar.pack(side="left", padx=5)

btn_importar = tk.Button(frame_botoes, text="Importar Tabela", command=importar_tabela,
                    bg="#284DC9", 
                    fg="white", 
                    activebackground="#5C75C9", 
                    activeforeground="white",
                    font=("Arial", 10, "bold"),
                    padx=8, pady=3,               # padding interno
                    bd=0,                            # remove borda padrão
                    relief="flat")
btn_importar.pack(side="left", padx=5)

# Combobox de filtro
filtro_var = tk.StringVar()
filtro_combobox = ttk.Combobox(frame_botoes, textvariable=filtro_var, state="readonly")
filtro_combobox['values'] = ["Todas", "Notas Baixas", "Notas Regulares", "Notas Boas"]
filtro_combobox.current(0)
filtro_combobox.bind("<<ComboboxSelected>>", aplicar_filtro)
filtro_combobox.pack(side="left", padx=5)  # lado esquerdo do frame, com espaçamento


# --- Tabela ---
colunas = ("nome", "idade", "curso", "nota")
tabela = ttk.Treeview(janela, columns=colunas, show="headings")

# Cabeçalhos
tabela.heading("nome", text="Nome")
tabela.heading("idade", text="Idade")
tabela.heading("curso", text="Curso")
tabela.heading("nota", text="Nota Final")

# Largura das colunas
tabela.column("nome", width=150)
tabela.column("idade", width=80, anchor='center')
tabela.column("curso", width=150, anchor='center')
tabela.column("nota", width=100, anchor='center')

# Scroll
scrollbar = ttk.Scrollbar(janela, orient="vertical", command=tabela.yview)
tabela.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tabela.pack(padx=10, pady=10)



janela.mainloop()