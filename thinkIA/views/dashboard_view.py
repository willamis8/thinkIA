import tkinter as tk
from tkinter import messagebox
from views.db import execute

class Dashboard(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Dashboard")
        self.geometry("400x250")
        self.resizable(False, False)

        self.total_clientes = tk.StringVar()
        self.total_pedidos = tk.StringVar()
        self.ticket_medio = tk.StringVar()

        tk.Label(self, text="📊 Dashboard", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self, text="Total de Clientes:").pack()
        tk.Label(self, textvariable=self.total_clientes, font=("Arial", 12, "bold")).pack()

        tk.Label(self, text="Total de Pedidos (mês):").pack(pady=(10,0))
        tk.Label(self, textvariable=self.total_pedidos, font=("Arial", 12, "bold")).pack()

        tk.Label(self, text="Ticket Médio:").pack(pady=(10,0))
        tk.Label(self, textvariable=self.ticket_medio, font=("Arial", 12, "bold")).pack()

        tk.Button(self, text="Atualizar", command=self.atualizar).pack(pady=10)
        self.atualizar()

    def atualizar(self):
        try:
            total_clientes = execute("SELECT COUNT(*) as n FROM clientes", fetchone=True)["n"]
            total_pedidos = execute("""
                SELECT COUNT(*) as n FROM pedidos
                WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
            """, fetchone=True)["n"]
            media = execute("SELECT AVG(total) as m FROM pedidos", fetchone=True)["m"]
            self.total_clientes.set(total_clientes)
            self.total_pedidos.set(total_pedidos)
            self.ticket_medio.set(f"R$ {media or 0:.2f}")
            messagebox.showinfo("Atualizado", "Dados atualizados com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar: {e}")
