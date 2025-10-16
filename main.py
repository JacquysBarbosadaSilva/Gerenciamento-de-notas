import tkinter as tk
import sys
from tkinter import filedialog, ttk, messagebox
import pandas as pd

print(sys.executable)

janela = tk.Tk()
janela.title("Gerenciamento de notas")

campos = ["Nome", "Idade", "Curso", "Nota Final"]
entries = []

for campo in campos:
    tk.Label(janela, text=f"{campo}:", font=('Arial', 8)).pack(anchor='w', padx=10, pady=(10, 0))
    entry = tk.Entry(janela, width=65, font=('Arial', 12), highlightthickness=1, highlightbackground="grey", highlightcolor="black")
    entry.pack(anchor='w', padx=10, pady=5)
    entries.append(entry)

todos_dados = [] 

def salvar_dados():
    valores = [entry.get() for entry in entries]   
    tabela.insert("", tk.END, values=valores)   
    todos_dados.append(valores)                   
    for entry in entries:
        entry.delete(0, tk.END) 


def aplicar_filtro(event=None):
    tipo = filtro_var.get() 
    tabela.delete(*tabela.get_children())  
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
        df = pd.DataFrame(linhas, columns=["Nome", "Idade", "Curso", "Nota Final"])
        df.to_csv(arquivo, index=False, encoding='utf-8')
        tk.messagebox.showinfo("Exportar CSV", f"Tabela filtrada exportada com sucesso para:\n{arquivo}")

def exportar_xlsx_filtrado():
    linhas = []
    for row_id in tabela.get_children():
        linhas.append(tabela.item(row_id)['values'])

    if not linhas:
        tk.messagebox.showwarning("Aviso", "Não há dados para exportar!")
        return

    arquivo = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Arquivos Excel", "*.xlsx")],
        title="Salvar tabela filtrada como Excel"
    )

    if arquivo:
        df = pd.DataFrame(linhas, columns=["Nome", "Idade", "Curso", "Nota Final"])
        try:
            df.to_excel(arquivo, index=False, engine='openpyxl')
            tk.messagebox.showinfo("Exportar XLSX", f"Tabela exportada com sucesso para:\n{arquivo}")
        except Exception as e:
            tk.messagebox.showerror("Erro", f"Falha ao exportar para XLSX:\n{e}")


def importar_tabela():
    arquivo = filedialog.askopenfilename(
        filetypes=[("Arquivos CSV", "*.csv"), ("Arquivos Excel", "*.xlsx *.xls")],
        title="Abrir tabela"
    )
    if not arquivo:
        return

    try:
        caminho_baixo = arquivo.lower()
        if caminho_baixo.endswith(".csv"):
            df = pd.read_csv(arquivo)
        elif caminho_baixo.endswith((".xlsx", ".xls")):
            df = pd.read_excel(arquivo)
        else:
            tk.messagebox.showwarning("Aviso", "Formato de arquivo não suportado.")
            return

        tabela.delete(*tabela.get_children())
        todos_dados.clear()

        for _, row in df.iterrows():
            valores = [row["Nome"], row["Idade"], row["Curso"], row["Nota Final"]]
            tabela.insert("", tk.END, values=valores)
            todos_dados.append(valores)

        tk.messagebox.showinfo("Importar Tabela", f"Tabela importada com sucesso de:\n{arquivo}")

    except KeyError:
        tk.messagebox.showerror("Erro", "O arquivo importado não possui as colunas necessárias (Nome, Idade, Curso, Nota Final).")
    except Exception as e:
        tk.messagebox.showerror("Erro", f"Não foi possível importar o arquivo:\n{e}")

frame_botoes = tk.Frame(janela)
frame_botoes.pack(pady=10)

btn_salvar = tk.Button(frame_botoes, text="Salvar", command=salvar_dados, 
                    bg="#4CAF50", fg="white", activebackground="#45a049", 
                    activeforeground="white", font=("Arial", 10, "bold"),
                    padx=8, pady=3, bd=0, relief="flat")
btn_salvar.pack(side="left", padx=5)  

btn_exportar_csv = tk.Button(frame_botoes, text="Exportar CSV", command=exportar_csv_filtrado,
                    bg="#652EAD", fg="white", activebackground="#7B53AF", 
                    activeforeground="white", font=("Arial", 10, "bold"),
                    padx=8, pady=3, bd=0, relief="flat")
btn_exportar_csv.pack(side="left", padx=5)

btn_exportar_xlsx = tk.Button(frame_botoes, text="Exportar XLSX", command=exportar_xlsx_filtrado,
                    bg="#009688", fg="white", activebackground="#26a69a", 
                    activeforeground="white", font=("Arial", 10, "bold"),
                    padx=8, pady=3, bd=0, relief="flat")
btn_exportar_xlsx.pack(side="left", padx=5)

btn_importar = tk.Button(frame_botoes, text="Importar Tabela", command=importar_tabela,
                    bg="#284DC9", fg="white", activebackground="#5C75C9", 
                    activeforeground="white", font=("Arial", 10, "bold"),
                    padx=8, pady=3, bd=0, relief="flat")
btn_importar.pack(side="left", padx=5)

filtro_var = tk.StringVar()
filtro_combobox = ttk.Combobox(frame_botoes, textvariable=filtro_var, state="readonly")
filtro_combobox['values'] = ["Todas", "Notas Baixas", "Notas Regulares", "Notas Boas"]
filtro_combobox.current(0)
filtro_combobox.bind("<<ComboboxSelected>>", aplicar_filtro)
filtro_combobox.pack(side="left", padx=5) 

colunas = ("nome", "idade", "curso", "nota")
tabela = ttk.Treeview(janela, columns=colunas, show="headings")

tabela.heading("nome", text="Nome")
tabela.heading("idade", text="Idade")
tabela.heading("curso", text="Curso")
tabela.heading("nota", text="Nota Final")

tabela.column("nome", width=150)
tabela.column("idade", width=80, anchor='center')
tabela.column("curso", width=150, anchor='center')
tabela.column("nota", width=100, anchor='center')

scrollbar = ttk.Scrollbar(janela, orient="vertical", command=tabela.yview)
tabela.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tabela.pack(padx=10, pady=10)

janela.mainloop()
