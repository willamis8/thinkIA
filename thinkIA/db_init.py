import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "database.db")

def init_db():
    """Cria o banco de dados e tabelas, caso ainda não existam."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Tabela de clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT
        )
    """)

    # Tabela de pedidos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER,
            data TEXT,
            total REAL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    """)

    # Tabela de itens do pedido
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER,
            produto TEXT,
            quantidade INTEGER,
            preco REAL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos (id)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Banco de dados inicializado com sucesso!")

