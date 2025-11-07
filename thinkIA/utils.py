# utils.py
import tkinter as tk
from tkinter import messagebox
import logging

def show_info(msg):
    messagebox.showinfo("Informação", msg)

def show_error(msg):
    messagebox.showerror("Erro", msg)

def confirm(msg):
    return messagebox.askyesno("Confirmação", msg)

def setup_logging():
    logging.basicConfig(filename="app.log", level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
