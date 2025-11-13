import tkinter as tk
from tkinter import ttk, messagebox
import logging
import os

# Imports dos outros módulos do projeto
from views.dashboard_view import Dashboard
from views.clientes_view import ListaClientes
from views.pedidos_view import PedidoForm
from views.relatorios_view import Relatorios

from .db_init import init_db
from .db import execute
from .views.relatorios_view import Relatorios

  # Certifique-se de ter o arquivo db_init.py

# Configuração do log
if not os.path.exists("logs"):
    os.makedirs("logs")
logging.basicConfig(filename="logs/app.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Inicializa banco de dados
init_db()

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistema ThinkIA")
        self.geometry("800x600")

        self.create_menu()
        self.show_dashboard()

    def create_menu(self):
        menubar = tk.Menu(self)

        menu_clientes = tk.Menu(menubar, tearoff=0)
        menu_clientes.add_command(label="Listar Clientes", command=self.show_clientes)
        menubar.add_cascade(label="Clientes", menu=menu_clientes)

        menu_pedidos = tk.Menu(menubar, tearoff=0)
        menu_pedidos.add_
