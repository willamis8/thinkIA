# views/pedidos_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from db import execute

class PedidoForm(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Novo Pedido")
        self.geometry("600x400")

        tk.Label(self, text="Cliente:").pack(anchor="w", padx=10, pady=(10,0))
        self.clientes = execute("SELECT id, nome FROM clientes ORDER BY nome", fetchall=True)
        self.cliente_var = tk.StringVar()
        nomes = [c["nome"] for c in self.clientes]
        self.cliente_cb = ttk.Combobox(self, values=nomes, textvariable=self.cliente_var)
        self.cliente_cb.pack(fill="x", padx=10)

        tk.Label(self, text="Data:").pack(anchor="w", padx=10, pady=(10,0))
        self.data_var = tk.StringVar(value=str(date.today()))
        tk.Entry(self, textvariable=self.data_var).pack(fill="x", padx=10)

        # tabela de itens
        cols = ("produto","quantidade","preco_unit")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", height=5)
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btns = tk.Frame(self)
        btns.pack()
        tk.Button(btns, text="Adicionar Item", command=self.add_item).pack(side="left", padx=5)
        tk.Button(btns, text="Remover Item", command=self.del_item).pack(side="left", padx=5)

        self.total_var = tk.StringVar(value="0.00")
        tk.Label(self, text="Total:").pack(anchor="e", padx=10)
        tk.Label(self, textvariable=self.total_var, font=("Arial",12,"bold")).pack(anchor="e", padx=10)

        tk.Button(self, text="Salvar Pedido", command=self.salvar).pack(pady=10)

    def add_item(self):
        item_win = tk.Toplevel(self)
        item_win.title("Adicionar Item")
        tk.Label(item_win, text="Produto:").pack()
        produto = tk.Entry(item_win)
        produto.pack()
        tk.Label(item_win, text="Quantidade:").pack()
        qtd = tk.Entry(item_win)
        qtd.pack()
        tk.Label(item_win, text="Preço unitário:").pack()
        preco = tk.Entry(item_win)
        preco.pack()

        def confirmar():
            try:
                q = int(qtd.get())
                p = float(preco.get())
                total = float(self.total_var.get()) + q*p
                self.total_var.set(f"{total:.2f}")
                self.tree.insert("", "end", values=(produto.get(), q, p))
                item_win.destroy()
            except ValueError:
                messagebox.showerror("Erro", "Valores inválidos.")

        tk.Button(item_win, text="OK", command=confirmar).pack()

    def del_item(self):
        sel = self.tree.selection()
        for s in sel:
            vals = self.tree.item(s)["values"]
            total = float(self.total_var.get()) - vals[1]*vals[2]
            self.total_var.set(f"{total:.2f}")
            self.tree.delete(s)

    def salvar(self):
        nome = self.cliente_var.get()
        cliente = next((c for c in self.clientes if c["nome"] == nome), None)
        if not cliente:
            messagebox.showwarning("Validação", "Selecione um cliente.")
            return
        data = self.data_var.get()
        total = float(self.total_var.get())

        conn = execute("BEGIN")  # inicia transação manualmente
        try:
            execute("INSERT INTO pedidos (cliente_id, data, total) VALUES (?, ?, ?)",
                    (cliente["id"], data, total), commit=True)
            pedido = execute("SELECT last_insert_rowid() as id", fetchone=True)
            for i in self.tree.get_children():
                prod, qtd, preco = self.tree.item(i)["values"]
                execute("""INSERT INTO itens_pedido (pedido_id, produto, quantidade, preco_unit)
                           VALUES (?, ?, ?, ?)""",
                        (pedido["id"], prod, qtd, preco), commit=True)
            messagebox.showinfo("Sucesso", "Pedido salvo com sucesso!")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao salvar pedido: {e}")
