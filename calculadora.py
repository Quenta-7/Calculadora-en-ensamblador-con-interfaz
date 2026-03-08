import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import os

# 1. Carga de la Librería Compartida (.so)
lib_path = os.path.abspath("./build/libcalc.so")
try:
    calc = ctypes.CDLL(lib_path)
except OSError:
    print(f"Error: No se encontró la librería en {lib_path}. Asegúrate de compilar el proyecto primero.")
    exit()

class CalculadoraPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora UNSAAC - Backend Ensamblador")
        self.root.geometry("380x600")
        self.root.configure(bg="#f5f5f5")

        # Variables de estado
        self.expresion = ""
        self.operando1 = None
        self.operacion_actual = None

        # --- ENCABEZADO ---
        header = tk.Frame(root, bg="white", pady=10)
        header.pack(fill="x")
        tk.Label(header, text="Calculadora", font=("Arial", 16, "bold"), bg="white").pack()
        tk.Label(header, text="Backend: Ensamblador x86-64 (NASM)", font=("Arial", 9), bg="white", fg="#777").pack()

        # --- PANTALLA DE VISUALIZACIÓN (DISPLAY) ---
        self.display_frame = tk.Frame(root, bg="#d4e6d5", height=110, bd=0)
        self.display_frame.pack(fill="x", padx=15, pady=15)
        self.display_frame.pack_propagate(False)

        self.lbl_op_secundaria = tk.Label(self.display_frame, text="", font=("Arial", 11), bg="#d4e6d5", fg="#555", anchor="e")
        self.lbl_op_secundaria.pack(fill="x", padx=15, pady=(15, 0))

        self.lbl_main = tk.Label(self.display_frame, text="0", font=("Arial", 28, "bold"), bg="#d4e6d5", fg="#1a1a1a", anchor="e")
        self.lbl_main.pack(fill="x", padx=15)

        # --- SISTEMA DE PESTAÑAS ---
        style = ttk.Style()
        style.theme_use('default')
        style.configure("TNotebook", background="#f5f5f5", borderwidth=0)
        style.configure("TNotebook.Tab", font=("Arial", 10), padding=[12, 4], background="#e0e0e0")
        style.map("TNotebook.Tab", background=[("selected", "white")], foreground=[("selected", "#2e7d32")])

        self.tabs = ttk.Notebook(root)
        self.tabs.pack(fill="both", expand=True, padx=10)

        # Crear frames para cada pestaña
        self.tab_arit = tk.Frame(self.tabs, bg="white")
        self.tab_log = tk.Frame(self.tabs, bg="white")
        self.tab_conv = tk.Frame(self.tabs, bg="white")

        self.tabs.add(self.tab_arit, text="Aritmética")
        self.tabs.add(self.tab_log, text="Lógica")
        self.tabs.add(self.tab_conv, text="Conversión")

        self.setup_aritmetica()
        self.setup_logica()
        self.setup_conversion()

    # --- PESTAÑA 1: ARITMÉTICA (Basado en arithmetic.asm) ---
    def setup_aritmetica(self):
        tk.Label(self.tab_arit, text="Operandos: 0 – 99", font=("Arial", 8), bg="white", fg="gray").pack(pady=5)
        grid_frame = tk.Frame(self.tab_arit, bg="white")
        grid_frame.pack(pady=5)

        btns = [
            ('7', 0, 0), ('8', 0, 1), ('9', 0, 2), ('÷', 0, 3, "#ff9500"),
            ('4', 1, 0), ('5', 1, 1), ('6', 1, 2), ('×', 1, 3, "#ff9500"),
            ('1', 2, 0), ('2', 2, 1), ('3', 2, 2), ('-', 2, 3, "#ff9500"),
            ('C', 3, 0, "#eb4d4b"), ('0', 3, 1), ('=', 3, 2, "#4caf50"), ('+', 3, 3, "#ff9500")
        ]

        for b in btns:
            self.crear_boton(grid_frame, b, self.click_aritmetico)

    # --- PESTAÑA 2: LÓGICA (Basado en logical.asm) ---
    def setup_logica(self):
        tk.Label(self.tab_log, text="Operaciones de 4 bits", font=("Arial", 9, "italic"), bg="white").pack(pady=10)
        grid_frame = tk.Frame(self.tab_log, bg="white")
        grid_frame.pack()

        # Botones específicos para AND, OR, NOT, XOR
        logic_btns = [
            ('1', 0, 0), ('0', 0, 1), ('C', 0, 2, "#eb4d4b"),
            ('AND', 1, 0, "#3498db"), ('OR', 1, 1, "#3498db"), ('XOR', 1, 2, "#3498db"),
            ('NOT', 2, 0, "#9b59b6"), ('=', 2, 1, "#4caf50", 2) # El = ocupa 2 columnas
        ]

        for b in logic_btns:
            col_span = b[4] if len(b) > 4 else 1
            self.crear_boton(grid_frame, b, self.click_logico, col_span)

    # --- PESTAÑA 3: CONVERSIÓN (Basado en conversion.asm) ---
    def setup_conversion(self):
        tk.Label(self.tab_conv, text="Binario (8 bits) <-> Hex", bg="white").pack(pady=10)
        
        # Botones de acción directa para los métodos de Emmi
        btn_b2h = tk.Button(self.tab_conv, text="Binario a Hex", command=self.conv_bin_to_hex, width=20, bg="#f39c12", fg="white", font=("Arial", 10, "bold"))
        btn_b2h.pack(pady=5)
        
        btn_h2b = tk.Button(self.tab_conv, text="Hex a Binario", command=self.conv_hex_to_bin, width=20, bg="#e67e22", fg="white", font=("Arial", 10, "bold"))
        btn_h2b.pack(pady=5)

    # --- LÓGICA DE PROCESAMIENTO ---
    def crear_boton(self, parent, info, comando, span=1):
        texto = info[0]
        color = info[3] if len(info) > 3 else "white"
        fg = "white" if len(info) > 3 else "black"
        
        btn = tk.Button(parent, text=texto, width=6 if span==1 else 14, height=2, 
                        font=("Arial", 12, "bold"), bg=color, fg=fg, relief="flat",
                        command=lambda: comando(texto))
        btn.grid(row=info[1], column=info[2], columnspan=span, padx=4, pady=4)

    def click_aritmetico(self, char):
        if char == 'C':
            self.limpiar()
        elif char in ['+', '-', '×', '÷']:
            if self.expresion:
                self.operando1 = int(self.expresion)
                self.operacion_actual = char
                self.lbl_op_secundaria.config(text=f"{self.operando1} {char}")
                self.expresion = ""
        elif char == '=':
            if self.operando1 is not None and self.expresion:
                op2 = int(self.expresion)
                res = self.call_asm_arit(self.operando1, op2, self.operacion_actual)
                self.lbl_op_secundaria.config(text=f"{self.operando1} {self.operacion_actual} {op2}")
                self.lbl_main.config(text=str(res))
                self.expresion = str(res)
        else:
            self.expresion += char
            self.lbl_main.config(text=self.expresion)

    def call_asm_arit(self, n1, n2, op):
        # Mapeo a funciones de arithmetic.asm
        if op == '+': return calc.asmSuma(n1, n2)
        if op == '-': return calc.asmResta(n1, n2)
        if op == '×': return calc.asmMultiplicacion(n1, n2)
        if op == '÷':
            if n2 == 0: return "Error /0"
            return calc.asmDivision(n1, n2)
        return 0

    def click_logico(self, char):
        if char == 'C': self.limpiar()
        elif char in ['AND', 'OR', 'XOR']:
            if self.expresion:
                self.operando1 = int(self.expresion, 2)
                self.operacion_actual = char
                self.lbl_op_secundaria.config(text=f"{bin(self.operando1)[2:].zfill(4)} {char}")
                self.expresion = ""
        elif char == 'NOT':
            if self.expresion:
                val = int(self.expresion, 2)
                res = calc.asmNot(val) & 0xF # Máscara 4 bits
                self.lbl_main.config(text=bin(res)[2:].zfill(4))
        elif char == '=':
            if self.operando1 is not None and self.expresion:
                op2 = int(self.expresion, 2)
                res = self.call_asm_logic(self.operando1, op2, self.operacion_actual)
                self.lbl_main.config(text=bin(res & 0xF)[2:].zfill(4))
        else:
            if len(self.expresion) < 4:
                self.expresion += char
                self.lbl_main.config(text=self.expresion)

    def call_asm_logic(self, n1, n2, op):
        # Mapeo a funciones de logical.asm
        if op == 'AND': return calc.asmAnd(n1, n2)
        if op == 'OR': return calc.asmOr(n1, n2)
        if op == 'XOR': return calc.asmXor(n1, n2)
        return 0

    def conv_bin_to_hex(self):
        # Simula la lógica de conversion.asm
        if len(self.expresion) == 8:
            val = int(self.expresion, 2)
            hex_res = hex(val)[2:].upper()
            self.lbl_main.config(text=f"HEX: {hex_res}")
        else:
            messagebox.showwarning("Aviso", "Ingrese 8 bits")

    def conv_hex_to_bin(self):
        # Simula la lógica de conversion.asm
        if len(self.expresion) > 0:
            try:
                val = int(self.expresion, 16)
                bin_res = bin(val)[2:].zfill(8)
                self.lbl_main.config(text=f"BIN: {bin_res}")
            except:
                messagebox.showerror("Error", "Hexadecimal inválido")

    def limpiar(self):
        self.expresion = ""
        self.operando1 = None
        self.operacion_actual = None
        self.lbl_main.config(text="0")
        self.lbl_op_secundaria.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculadoraPro(root)
    root.mainloop()