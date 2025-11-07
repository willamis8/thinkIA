# views/clientes_view.py
import tkinter as tk
from tkinter import messagebox
import re
from db import execute

class ClienteForm(tk.Toplevel):
    def __init__(self, master=None, cliente=None, on_save=None):
        super().__init__(master)
        self.title("Cadastro de Cliente")
        self.geometry("350x250")
        self.resizable(False, False)

        self.cliente = cliente
        self.on_save = on_save
        self.dirty = False  # prevenção de fechamento sem salvar

        tk.Label(self, text="Nome *").pack(anchor="w", padx=10, pady=(10,0))
        self.nome_var = tk.StringVar(value=cliente["nome"] if cliente else "")
        tk.Entry(self, textvariable=self.nome_var).pack(fill="x", padx=10)

        tk.Label(self, text="E-mail").pack(anchor="w", padx=10, pady=(10,0))
        self.email_var = tk.StringVar(value=cliente["email"] if cliente else "")
        tk.Entry(self, textvariable=self.email_var).pack(fill="x", padx=10)

        tk.Label(self, text="Telefone").pack(anchor="w", padx=10, pady=(10,0))
        self.tel_var = tk.StringVar(value=cliente["telefone"] if cliente else "")
        tk.Entry(self, textvariable=self.tel_var).pack(fill="x", padx=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)
        tk.Button(btn_frame, text="Salvar", command=self.salvar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Cancelar", command=self.cancelar).pack(side="left", padx=5)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def validar(self):
        nome = self.nome_var.get().strip()
        email = self.email_var.get().strip()
        telefone = self.tel_var.get().strip()

        if not nome:
            messagebox.showwarning("Validação", "O nome é obrigatório.")
            return False
        if email and not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showwarning("Validação", "E-mail inválido.")
            return False
        if telefone and not re.match(r"^\d{8,15}$", telefone):
            messagebox.showwarning("Validação", "Telefone deve ter 8–15 dígitos.")
            return False
        return True

    def salvar(self):
        if not self.validar():
            return

        data = (self.nome_var.get(), self.email_var.get(), self.tel_var.get())
        if self.cliente:
            execute("UPDATE clientes SET nome=?, email=?, telefone=? WHERE id=?",
                    data + (self.cliente["id"],), commit=True)
        else:
            execute("INSERT INTO clientes (nome, email, telefone) VALUES (?, ?, ?)",
                    data, commit=True)

        messagebox.showinfo("Sucesso", "Cliente salvo com sucesso!")
        if self.on_save:
            self.on_save()
        self.destroy()

    def cancelar(self):
        if messagebox.askyesno("Cancelar", "Deseja descartar as alterações?"):
            self.destroy()

    def on_close(self):
        self.cancelar()
import tkinter as tk
from tkinter import ttk, messagebox
from db import execute
from views.clientes_view import ClienteForm

class ListaClientes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        search_frame = tk.Frame(self)
        search_frame.pack(fill="x", pady=5)
        tk.Label(search_frame, text="Buscar:").pack(side="left", padx=5)
        self.search_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_var).pack(side="left", fill="x", expand=True)
        tk.Button(search_frame, text="OK", command=self.load_data).pack(side="left", padx=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", pady=5)
        tk.Button(btn_frame, text="Novo", command=self.novo).pack(side="left")
        tk.Button(btn_frame, text="Editar", command=self.editar).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Excluir", command=self.excluir).pack(side="left", padx=5)

        self.tree = ttk.Treeview(self, columns=("id","nome","email","telefone"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
        self.tree.pack(fill="both", expand=True)

    def load_data(self):
        termo = f"%{self.search_var.get()}%"
        rows = execute(
            "SELECT * FROM clientes WHERE nome LIKE ? OR email LIKE ? ORDER BY nome",
            (termo, termo), fetchall=True
        )
        self.tree.delete(*self.tree.get_children())
        for r in rows or []:
            self.tree.insert("", "end", values=(r["id"], r["nome"], r["email"], r["telefone"]))

    def get_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Seleção", "Selecione um cliente.")
            return None
        item = self.tree.item(sel[0])
        return dict(zip(self.tree["columns"], item["values"]))

    def novo(self):
        ClienteForm(self, on_save=self.load_data)

    def editar(self):
        cliente = self.get_selected()
        if cliente:
            ClienteForm(self, cliente=cliente, on_save=self.load_data)

    def excluir(self):
        cliente = self.get_selected()
        if not cliente:
            return
        if messagebox.askyesno("Excluir", f"Deseja excluir {cliente['nome']}?"):
            execute("DELETE FROM clientes WHERE id=?", (cliente["id"],), commit=True)
            self.load_data()
