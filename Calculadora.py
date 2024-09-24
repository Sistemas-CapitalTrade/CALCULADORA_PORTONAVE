import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk

def evaluate_expression(event=None):
    try:
        result = str(eval(expression.get()))
        expression.set(result)
    except Exception as e:
        messagebox.showerror("Error", str(e))
        expression.set("")

def clear_expression(event=None):
    expression.set("")

def append_to_expression(value):
    current_val = expression.get()
    expression.set(current_val + value)

app = tk.Tk()
app.title("Calculadora - Capital Trade")
app.configure(bg="#002060")  # Fundo da calculadora em preto

# Definindo o caminho do ícone
icon_path = "C:/Users/rafael.souza.CAPITAL/OneDrive - CAPITAL TRADE/Área de Trabalho/Documentos/BI/CONTROLE DE DI/ÍCONES/ícone2.ico"

# Carregando o ícone
icon = tk.PhotoImage(file=icon_path)

# Definindo o ícone da janela
app.iconphoto(False, icon)

expression = tk.StringVar()

# Melhorando a estética do campo de entrada
entry = tk.Entry(app, textvariable=expression, font=("Arial", 24), bg="#1f1f1f", fg="white", borderwidth=2, relief="flat")
entry.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=12, pady=12)

# Estilo dos botões
button_colors = {
    "num": {"bg": "#002060", "fg": "white"},  # Cinza escuro para números
    "op": {"bg": "#002060", "fg": "white"},   # Cinza escuro para operadores
    "action": {"bg": "#002060", "fg": "orange"} # Cinza escuro para ações especiais
}

buttons = [
    ('0', lambda: append_to_expression('0'), 'num'), ('1', lambda: append_to_expression('1'), 'num'), ('2', lambda: append_to_expression('2'), 'num'),
    ('3', lambda: append_to_expression('3'), 'num'), ('4', lambda: append_to_expression('4'), 'num'), ('5', lambda: append_to_expression('5'), 'num'),
    ('6', lambda: append_to_expression('6'), 'num'), ('7', lambda: append_to_expression('7'), 'num'), ('8', lambda: append_to_expression('8'), 'num'),
    ('9', lambda: append_to_expression('9'), 'num'), ('+', lambda: append_to_expression('+'), 'op'), ('-', lambda: append_to_expression('-'), 'op'),
    ('*', lambda: append_to_expression('*'), 'op'), ('/', lambda: append_to_expression('/'), 'op'),
    ('(', lambda: append_to_expression('('), 'op'), (')', lambda: append_to_expression(')'), 'op'),
    ('C', clear_expression, 'action'), ('=', evaluate_expression, 'action'), ('Exp', lambda: append_to_expression('Exp'), 'action'),
    ('Enter', evaluate_expression, 'action')
]

for i, (text, action, style_key) in enumerate(buttons):
    style = button_colors[style_key]
    button = tk.Button(app, text=text, command=action, bg=style['bg'], fg=style['fg'], font=("Arial", 18), borderwidth=0, highlightthickness=0)
    button.grid(row=i // 4 + 1, column=i % 4, sticky="nsew", padx=4, pady=4)

app.bind("<Return>", evaluate_expression)
app.bind("<Escape>", clear_expression)

# Configuração de redimensionamento
app.rowconfigure(0, weight=1)
for x in range(1, 6):
    app.rowconfigure(x, weight=1)
    for y in range(4):
        app.columnconfigure(y, weight=1)

app.mainloop()