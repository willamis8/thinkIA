import tkinter as tk
from tkinter import messagebox
import os

class Historico(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Histórico de Ações")
        self.geometry("600x400")

        self.text = tk.Text(self)
        self.text.pack(fill="both", expand=True)

        tk.Button(self, text="Limpar Histórico", command=self.limpar).pack(pady=5)
        self.carregar()

    def carregar(self):
        if os.path.exists("logs/app.log"):
            with open("logs/app.log", encoding="utf-8") as f:
                self.text.delete("1.0", tk.END)
                self.text.insert(tk.END, f.read())

    def limpar(self):
        if messagebox.askyesno("Confirmação", "Deseja limpar o histórico?"):
            open("logs/app.log", "w").close()
            self.carregar()
