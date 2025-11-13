# db.py
import sqlite3
import logging
 
DB_NAME = "app.db"

def get_connection():
    """Retorna uma conexão SQLite com row_factory para dict-like access."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Cria as tabelas se não existirem."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.executescript("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT,
            telefone TEXT
        );

        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            total REAL NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        );

        CREATE TABLE IF NOT EXISTS itens_pedido (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pedido_id INTEGER NOT NULL,
            produto TEXT NOT NULL,
            quantidade INTEGER NOT NULL,
            preco_unit REAL NOT NULL,
            FOREIGN KEY (pedido_id) REFERENCES pedidos(id)
        );
        """)
        conn.commit()
    except sqlite3.Error as e:
        logging.exception(f"Erro ao inicializar banco: {e}")
    finally:
        conn.close()

def execute(query, params=(), fetchone=False, fetchall=False, commit=False):
    """Executa um comando SQL parametrizado com tratamento de erros."""
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(query, params)
        if commit:
            conn.commit()
        if fetchone:
            return cur.fetchone()
        if fetchall:
            return cur.fetchall()
    except sqlite3.Error as e:
        logging.exception(f"Erro SQL: {e} | Query: {query} | Params: {params}")
        return None
    finally:
        conn.close()
