# main.py
import tkinter as tk
from db import init_db
from views.clientes_view import ListaClientes
from views.pedidos_view import PedidoForm
from utils import setup_logging

def main():
    setup_logging()
    init_db()

    root = tk.Tk()
    root.title("Gerenciador de Clientes e Pedidos")
    root.geometry("800x500")

    menu = tk.Menu(root)
    root.config(menu=menu)

    cadastro = tk.Menu(menu, tearoff=0)
    cadastro.add_command(label="Clientes", command=lambda: ListaClientes(root))
    cadastro.add_command(label="Novo Pedido", command=lambda: PedidoForm(root))
    menu.add_cascade(label="Cadastros", menu=cadastro)

    tk.Label(root, text="Bem-vindo ao sistema de Clientes e Pedidos", font=("Arial", 14)).pack(pady=50)
    root.mainloop()

if __name__ == "__main__":
    main()
