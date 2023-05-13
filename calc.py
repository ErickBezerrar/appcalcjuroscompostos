import tkinter as tk
from tkinter import ttk
import ttkthemes as ttkthemes
from tkinter import messagebox

class InvestimentoGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Cálculo de Juros Compostos")
        self.master.geometry("920x600")
        self.master.resizable(True, True)

        style = ttk.Style(self.master)
        style.configure(".", anchor="w")
        style.configure("TEntry", padding=5, relief="flat")
        style.configure("TLabel", padding=5)

        # Aqui definimos o estilo do tema
        style = ttkthemes.ThemedStyle(self.master)
        style.set_theme("equilux")


        frame = ttk.Frame(self.master, padding=10)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text="Valor Inicial:").grid(column=0, row=0, sticky="w")
        self.valor_presente = ttk.Entry(frame)
        self.valor_presente.grid(column=1, row=0)

        ttk.Label(frame, text="Taxa de Juros:").grid(column=0, row=1, sticky="w")
        self.taxa_juros = ttk.Entry(frame)
        self.taxa_juros.grid(column=1, row=1)

        ttk.Label(frame, text="Período (anos):").grid(column=0, row=2, sticky="w")
        self.periodo_anos = ttk.Entry(frame)
        self.periodo_anos.grid(column=1, row=2)

        ttk.Label(frame, text="Aporte Mensal:").grid(column=0, row=3, sticky="w")
        self.aporte_mensal = ttk.Entry(frame)
        self.aporte_mensal.grid(column=1, row=3)

        ttk.Label(frame, text="Valor Futuro:").grid(column=0, row=4, sticky="w")
        self.valor_futuro = ttk.Label(frame, text="")
        self.valor_futuro.grid(column=1, row=4)

        ttk.Button(frame, text="Calcular", command=self.calcular).grid(column=0, row=5, pady=10, padx=11, sticky="e", columnspan=1)
        ttk.Button(frame, text="Limpar Tabela", command=self.limpar_tabela).grid(column=1, row=5, pady=10, padx=11, sticky="w", columnspan=1)

        columns = ("Ano", "Valor Inicial(Ano)", "Aportes(Anual)", "Juros", "Dividendos(Mensais)", "Valor Final(Ano)")
        self.tree = ttk.Treeview(frame, show="headings", columns=columns, height=18)
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, width=150, anchor="w")
        self.tree.grid(column=0, row=7, columnspan=2)


    def limpar_tabela(self):
        self.tree.delete(*self.tree.get_children())

    def limpar(self):
        self.valor_inicial_entry.delete(0, tk.END)
        self.adicao_mensal_entry.delete(0, tk.END)
        self.taxa_juros_entry.delete(0, tk.END)
        self.tempo_ano_entry.delete(0, tk.END)
        self.tree.delete(*self.tree.get_children())
        


    def calcular(self):
        # Limpa a tabela
        for i in self.tree.get_children():
            self.tree.delete(i)

        try:
            valor_presente = float(self.valor_presente.get().replace(",", "."))
            taxa_juros = float(self.taxa_juros.get().replace(",", "."))
            periodo_anos = int(self.periodo_anos.get())
            aporte_mensal = float(self.aporte_mensal.get().replace(",", "."))
        except ValueError:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")
            return

        if taxa_juros <= 0 or periodo_anos <= 0 or aporte_mensal < 0:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos corretamente.")
            return

        valores = []
        valor_atual = valor_presente
        for i in range(1, periodo_anos+1):
            juros_ano = 0
            for mes in range(12):
                juros_mes = (valor_atual + aporte_mensal * mes) * (taxa_juros / 100 / 12)
                juros_ano += juros_mes
                valor_atual += aporte_mensal + juros_mes

            dividendos_ano = juros_ano / 12  # Novo cálculo dos dividendos mensais

            valores.append((i, "{:.2f}".format(valor_presente), "{:.2f}".format(aporte_mensal * 12), "{:.2f}".format(juros_ano), "{:.2f}".format(dividendos_ano), "{:.2f}".format(valor_atual)))
            valor_presente = valor_atual

        for v in valores:
            self.tree.insert("", "end", values=v)
        self.valor_futuro.config(text="{:.2f}".format(valor_atual))

root = tk.Tk()
app = InvestimentoGUI(root)
root.mainloop()