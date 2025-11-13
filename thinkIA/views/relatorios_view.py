import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3, csv, logging, os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "database.db")  # ajuste se necessário

class Relatorios(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Relatórios de Pedidos")
        self.geometry("700x500")

        tk.Label(self, text="Cliente:").pack(anchor="w", padx=10)

        # Conecta ao banco e busca clientes
        clientes = self.executar("SELECT id, nome FROM clientes", fetchall=True)
        self.cliente_map = {c[1]: c[0] for c in clientes}
        self.cliente_var = tk.StringVar()
        ttk.Combobox(self, textvariable=self.cliente_var, values=list(self.cliente_map.keys())).pack(fill="x", padx=10)

        # Treeview
        self.tree = ttk.Treeview(self, columns=("cliente", "data", "itens", "total"), show="headings")
        for c in self.tree["columns"]:
            self.tree.heading(c, text=c.capitalize())
        self.tree.pack(fill="both", expand=True, pady=10)

        # Botões
        tk.Button(self, text="Filtrar", command=self.filtrar).pack()
        frame_btns = tk.Frame(self)
        frame_btns.pack(pady=10)
        tk.Button(frame_btns, text="Exportar CSV", command=self.exportar_csv).pack(side="left", padx=10)
        tk.Button(frame_btns, text="Exportar PDF", command=self.exportar_pdf).pack(side="left")

    def executar(self, query, params=(), fetchall=False):
        """Executa comandos SQL simples"""
        try:
            conn = sqlite3.connect(DB_PATH)
            cur = conn.cursor()
            cur.execute(query, params)
            if fetchall:
                data = cur.fetchall()
            else:
                data = cur.fetchone()
            conn.close()
            return data
        except Exception as e:
            logging.exception(e)
            messagebox.showerror("Erro no Banco", str(e))
            return []

    def filtrar(self):
        cid = self.cliente_map.get(self.cliente_var.get())
        query = """
            SELECT c.nome, p.data, GROUP_CONCAT(i.produto, ', '), p.total
            FROM pedidos p
            JOIN clientes c ON p.cliente_id = c.id
            LEFT JOIN itens_pedido i ON i.pedido_id = p.id
            WHERE (? IS NULL OR c.id = ?)
            GROUP BY p.id
            ORDER BY p.data DESC
        """
        rows = self.executar(query, (cid, cid), fetchall=True)

        self.tree.delete(*self.tree.get_children())
        for r in rows or []:
            cliente, data, itens, total = r
            self.tree.insert("", "end", values=(cliente, data, itens, f"R$ {total:.2f}" if total else "R$ 0.00"))

    def exportar_csv(self):
        try:
            path = filedialog.asksaveasfilename(defaultextension=".csv")
            if not path:
                return
            with open(path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["Cliente", "Data", "Itens", "Total"])
                for i in self.tree.get_children():
                    writer.writerow(self.tree.item(i)["values"])
            messagebox.showinfo("Exportado", f"CSV salvo em {path}")
        except Exception as e:
            logging.exception(e)
            messagebox.showerror("Erro", str(e))

    def exportar_pdf(self):
        try:
            path = filedialog.asksaveasfilename(defaultextension=".pdf")
            if not path:
                return
            c = canvas.Canvas(path, pagesize=A4)
            y = 800
            for i in self.tree.get_children():
                line = " | ".join(map(str, self.tree.item(i)["values"]))
                c.drawString(50, y, line)
                y -= 20
            c.save()
            messagebox.showinfo("Exportado", f"PDF salvo em {path}")
        except Exception as e:
            logging.exception(e)
            messagebox.showerror("Erro", str(e))
