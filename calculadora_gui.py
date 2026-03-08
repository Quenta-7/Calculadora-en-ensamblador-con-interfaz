import tkinter as tk
from tkinter import ttk, messagebox
import ctypes
import os

# ============================================
# CARGA DE LIBRERÍA DE ENSAMBLADOR
# ============================================
lib_path = os.path.abspath("./build/libcalc.so")
try:
    calc = ctypes.CDLL(lib_path)
except OSError:
    print(f"❌ No se encontró {lib_path}")
    print("   Ejecuta primero: ./scripts/compile_gui.sh")
    exit()

def bind_int(name):
    f = getattr(calc, name)
    f.argtypes = [ctypes.c_int64, ctypes.c_int64]
    f.restype  = ctypes.c_int64
    return f

def bind_str(name):
    f = getattr(calc, name)
    f.argtypes = [ctypes.c_char_p]
    f.restype  = ctypes.c_int64
    return f

asm_suma       = bind_int('asmSuma')
asm_resta      = bind_int('asmResta')
asm_mul        = bind_int('asmMultiplicacion')
asm_div        = bind_int('asmDivision')
asm_residuo    = bind_int('asmResiduo')
asm_and        = bind_int('asmAnd')
asm_or         = bind_int('asmOr')
asm_xor        = bind_int('asmXor')
asm_not        = bind_int('asmNot')
asm_bin_to_num = bind_str('asmBinToNum')
asm_hex_to_num = bind_str('asmHexToNum')

# ============================================
# PALETA (Catppuccin Mocha)
# ============================================
BG      = "#1e1e2e"
SURFACE = "#2a2a3e"
OVERLAY = "#45475a"
TEXT    = "#cdd6f4"
SUBTEXT = "#a6adc8"
ROJO    = "#f38ba8"
NARANJA = "#fab387"
AMBAR   = "#f9e2af"
VERDE   = "#a6e3a1"
AZUL    = "#89b4fa"
CELESTE = "#89dceb"
MORADO  = "#cba6f7"
ROSA    = "#f5c2e7"

# ============================================
# INTERFAZ GRÁFICA
# ============================================
class Calculadora:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora UNSAAC — Ensamblador x86-64")
        self.root.geometry("660x720")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.expresion      = ""
        self.operando1      = None
        self.operacion      = None
        self._tab_actual    = "arit"
        self._historial     = []
        self._btn_op_activo = None

        # ── Layout raíz: izquierda (calc) | derecha (historial) ──
        self.col_left  = tk.Frame(self.root, bg=BG)
        self.col_right = tk.Frame(self.root, bg=SURFACE,
                                  highlightbackground=OVERLAY,
                                  highlightthickness=1)
        self.col_left.pack(side="left", fill="both", expand=False, padx=(10,0), pady=10)
        self.col_right.pack(side="left", fill="both", expand=True, padx=(8,10), pady=10)

        self._build_header()
        self._build_display()
        self._build_tabs()
        self._build_statusbar()
        self._build_historial()
        self._bind_keys()

    # ── HEADER ───────────────────────────────
    def _build_header(self):
        f = tk.Frame(self.col_left, bg=BG)
        f.pack(fill="x", pady=(4, 0))
        tk.Label(f, text="UNSAAC", font=("Consolas", 9, "bold"),
                 bg=BG, fg=MORADO).pack(side="left")
        tk.Label(f, text="x86-64 ASM", font=("Consolas", 9),
                 bg=BG, fg=OVERLAY).pack(side="right")

    # ── DISPLAY ──────────────────────────────
    def _build_display(self):
        frame = tk.Frame(self.col_left, bg=SURFACE,
                         highlightbackground=OVERLAY,
                         highlightthickness=1)
        frame.pack(fill="x", pady=(4, 4))

        self.lbl_secondary = tk.Label(
            frame, text="", font=("Consolas", 10),
            bg=SURFACE, fg=SUBTEXT, anchor="e"
        )
        self.lbl_secondary.pack(fill="x", padx=12, pady=(8, 0))

        self.lbl_main = tk.Label(
            frame, text="0", font=("Consolas", 30, "bold"),
            bg=SURFACE, fg=TEXT, anchor="e"
        )
        self.lbl_main.pack(fill="x", padx=12)

        self.lbl_residuo = tk.Label(
            frame, text="", font=("Consolas", 10),
            bg=SURFACE, fg=AMBAR, anchor="e"
        )
        self.lbl_residuo.pack(fill="x", padx=12, pady=(0, 8))

    # ── TABS ─────────────────────────────────
    def _build_tabs(self):
        style = ttk.Style()
        style.theme_use("default")
        style.configure("TNotebook", background=BG, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=OVERLAY, foreground=TEXT,
                        padding=[12, 6], font=("Consolas", 9, "bold"))
        style.map("TNotebook.Tab",
                  background=[("selected", AZUL)],
                  foreground=[("selected", BG)])

        nb = ttk.Notebook(self.col_left)
        nb.pack(fill="both", expand=True)

        TAB_IDS = ["arit", "logic", "conv"]
        for title, builder in [
            (" Aritmética ", self._tab_aritmetica),
            ("   Lógica   ", self._tab_logica),
            (" Conversión ", self._tab_conversion),
        ]:
            tab = tk.Frame(nb, bg=BG)
            nb.add(tab, text=title)
            builder(tab)

        def _on_tab_change(e):
            self._tab_actual = TAB_IDS[nb.index(nb.select())]
            self._reset()
            self._update_status()
        nb.bind("<<NotebookTabChanged>>", _on_tab_change)

    # ── BARRA DE ESTADO ──────────────────────
    def _build_statusbar(self):
        bar = tk.Frame(self.col_left, bg=OVERLAY, height=20)
        bar.pack(fill="x", pady=(4, 0))
        bar.pack_propagate(False)

        self.lbl_mode = tk.Label(bar, text="● ARITMÉTICA",
                                 font=("Consolas", 8, "bold"),
                                 bg=OVERLAY, fg=VERDE, anchor="w")
        self.lbl_mode.pack(side="left", padx=8)

        self.lbl_status_op = tk.Label(bar, text="",
                                      font=("Consolas", 8),
                                      bg=OVERLAY, fg=AMBAR, anchor="e")
        self.lbl_status_op.pack(side="right", padx=8)

        tk.Label(bar, text="RAX→Python",
                 font=("Consolas", 8),
                 bg=OVERLAY, fg=SUBTEXT).pack(side="right", padx=4)

    def _update_status(self, op_info=""):
        modos = {
            "arit":  ("● ARITMÉTICA",    VERDE),
            "logic": ("● LÓGICA  4 bits", AZUL),
            "conv":  ("● CONVERSIÓN",    MORADO),
        }
        txt, col = modos[self._tab_actual]
        self.lbl_mode.config(text=txt, fg=col)
        self.lbl_status_op.config(text=op_info)

    # ── HISTORIAL (columna derecha) ───────────
    def _build_historial(self):
        # Título + botón limpiar
        top = tk.Frame(self.col_right, bg=SURFACE)
        top.pack(fill="x", padx=8, pady=(10, 4))

        tk.Label(top, text="⏱  Historial",
                 font=("Consolas", 10, "bold"),
                 bg=SURFACE, fg=SUBTEXT).pack(side="left")

        tk.Button(top, text="limpiar",
                  font=("Consolas", 8), bg=SURFACE, fg=OVERLAY,
                  activebackground=OVERLAY, activeforeground=TEXT,
                  relief="flat", cursor="hand2",
                  command=self._clear_historial).pack(side="right")

        # Separador
        tk.Frame(self.col_right, bg=OVERLAY, height=1).pack(fill="x", padx=8)

        # Área scrollable de entradas
        self.hist_inner = tk.Frame(self.col_right, bg=SURFACE)
        self.hist_inner.pack(fill="both", expand=True, padx=8, pady=6)

        # Canvas + scrollbar para scroll vertical
        self.hist_canvas = tk.Canvas(self.hist_inner, bg=SURFACE,
                                     highlightthickness=0)
        scrollbar = tk.Scrollbar(self.hist_inner, orient="vertical",
                                 command=self.hist_canvas.yview)
        self.hist_canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        self.hist_canvas.pack(side="left", fill="both", expand=True)

        self.hist_list_frame = tk.Frame(self.hist_canvas, bg=SURFACE)
        self.hist_canvas_window = self.hist_canvas.create_window(
            (0, 0), window=self.hist_list_frame, anchor="nw"
        )

        self.hist_list_frame.bind("<Configure>", self._on_hist_configure)
        self.hist_canvas.bind("<Configure>", self._on_canvas_configure)

        # Hint inicial
        self.hist_hint = tk.Label(self.hist_list_frame,
                                  text="Las operaciones\naparecerán aquí",
                                  font=("Consolas", 9),
                                  bg=SURFACE, fg=OVERLAY,
                                  justify="center")
        self.hist_hint.pack(pady=20)

    def _on_hist_configure(self, e):
        self.hist_canvas.configure(
            scrollregion=self.hist_canvas.bbox("all"))

    def _on_canvas_configure(self, e):
        self.hist_canvas.itemconfig(
            self.hist_canvas_window, width=e.width)

    def _add_historial(self, texto):
        # Quitar hint la primera vez
        if self.hist_hint:
            self.hist_hint.destroy()
            self.hist_hint = None

        self._historial.append(texto)

        # Número de entrada
        idx = len(self._historial)

        entry = tk.Frame(self.hist_list_frame, bg=SURFACE)
        entry.pack(fill="x", pady=2)

        # Número índice
        tk.Label(entry, text=f"{idx:02d}",
                 font=("Consolas", 8),
                 bg=SURFACE, fg=OVERLAY,
                 width=3, anchor="e").pack(side="left", padx=(0, 4))

        # Texto de la operación
        tk.Label(entry, text=texto,
                 font=("Consolas", 9, "bold"),
                 bg=SURFACE, fg=TEXT,
                 anchor="w", wraplength=130, justify="left").pack(
                     side="left", fill="x", expand=True)

        # Scroll automático al fondo
        self.root.after(50, lambda: self.hist_canvas.yview_moveto(1.0))

    def _clear_historial(self):
        self._historial = []
        for w in self.hist_list_frame.winfo_children():
            w.destroy()
        self.hist_hint = tk.Label(self.hist_list_frame,
                                  text="Las operaciones\naparecerán aquí",
                                  font=("Consolas", 9),
                                  bg=SURFACE, fg=OVERLAY,
                                  justify="center")
        self.hist_hint.pack(pady=20)

    # ── BOTÓN HELPER ─────────────────────────
    def _btn(self, parent, text, row, col, cmd,
             color=OVERLAY, fg=TEXT, colspan=1):
        b = tk.Button(
            parent, text=text, width=5, height=2,
            font=("Consolas", 12, "bold"),
            bg=color, fg=fg,
            activebackground=fg, activeforeground=color,
            relief="flat", cursor="hand2",
            bd=0, highlightthickness=0,
            command=lambda: self._press_effect(b, color, fg, cmd)
        )
        b.grid(row=row, column=col, columnspan=colspan,
               padx=3, pady=3, sticky="nsew")
        b.bind("<Enter>", lambda e, b=b, c=color, f=fg: b.config(bg=f, fg=c))
        b.bind("<Leave>", lambda e, b=b, c=color, f=fg: b.config(bg=c, fg=f))
        return b

    def _press_effect(self, btn, orig_color, orig_fg, cmd):
        btn.config(bg=SURFACE, fg=SUBTEXT)
        self.root.after(80, lambda: btn.config(bg=orig_color, fg=orig_fg))
        cmd()

    def _highlight_op_btn(self, btn_ref):
        if self._btn_op_activo and self._btn_op_activo != btn_ref:
            old_btn, old_color, old_fg = self._btn_op_activo
            old_btn.config(bg=old_color, fg=old_fg, highlightthickness=0)
        if btn_ref:
            b, c, f = btn_ref
            b.config(bg=f, fg=c, highlightthickness=2,
                     highlightbackground=ROSA)
            self._btn_op_activo = btn_ref
        else:
            self._btn_op_activo = None

    # ── TAB ARITMÉTICA ────────────────────────
    def _tab_aritmetica(self, tab):
        tk.Label(tab, text="Enteros  (máx 6 dígitos)",
                 font=("Consolas", 8), bg=BG, fg=SUBTEXT).pack(pady=(6, 0))

        f = tk.Frame(tab, bg=BG)
        f.pack(pady=6)

        self._op_btns_arit = {}
        layout = [
            [("7",OVERLAY,TEXT),("8",OVERLAY,TEXT),("9",OVERLAY,TEXT),("÷",NARANJA,BG)],
            [("4",OVERLAY,TEXT),("5",OVERLAY,TEXT),("6",OVERLAY,TEXT),("×",NARANJA,BG)],
            [("1",OVERLAY,TEXT),("2",OVERLAY,TEXT),("3",OVERLAY,TEXT),("-",NARANJA,BG)],
            [("C",  ROJO,  BG), ("0",OVERLAY,TEXT),("=", VERDE,  BG),("+",NARANJA,BG)],
        ]
        for r, row in enumerate(layout):
            for c, (txt, col, fg) in enumerate(row):
                b = self._btn(f, txt, r, c,
                              lambda t=txt: self._arit_click(t),
                              color=col, fg=fg)
                if txt in "+-×÷":
                    self._op_btns_arit[txt] = (b, col, fg)

        tk.Label(tab, text="⌨  0-9  + - * /  Enter=igual  Esc=limpiar",
                 font=("Consolas", 7), bg=BG, fg=OVERLAY).pack(pady=(2, 0))

    def _arit_click(self, char):
        if char == "C":
            self._reset(); self._highlight_op_btn(None)
        elif char in "+-×÷":
            if self.expresion:
                self.operando1 = int(self.expresion)
                self.operacion = char
                self.lbl_secondary.config(text=f"{self.operando1} {char}")
                self.lbl_residuo.config(text="")
                self.expresion = ""
                self._highlight_op_btn(self._op_btns_arit.get(char))
                self._update_status(f"op: {char}")
        elif char == "=":
            if self.operando1 is not None and self.expresion:
                n2 = int(self.expresion)
                op = self.operacion
                self.lbl_residuo.config(text="")
                self._highlight_op_btn(None)
                if   op == "+": res = asm_suma(self.operando1, n2)
                elif op == "-": res = asm_resta(self.operando1, n2)
                elif op == "×": res = asm_mul(self.operando1, n2)
                elif op == "÷":
                    if n2 == 0:
                        self._error("División por cero"); return
                    cociente = asm_div(self.operando1, n2)
                    residuo  = asm_residuo(self.operando1, n2)
                    entrada  = f"{self.operando1} ÷ {n2}"
                    self.lbl_secondary.config(text=f"{entrada}  →  Cociente:")
                    self.lbl_main.config(text=str(cociente))
                    self.lbl_residuo.config(text=f"Residuo: {residuo}")
                    self._add_historial(f"{entrada} = {cociente} r{residuo}")
                    self._update_status()
                    self.expresion = str(cociente)
                    self.operando1 = None; self.operacion = None
                    return
                entrada = f"{self.operando1} {op} {n2}"
                self.lbl_secondary.config(text=f"{entrada} =")
                self.lbl_main.config(text=str(res))
                self._add_historial(f"{entrada} = {res}")
                self._update_status()
                self.expresion = str(res)
                self.operando1 = None; self.operacion = None
        else:
            if len(self.expresion) < 6:
                self.expresion += char
                self.lbl_main.config(text=self.expresion)

    # ── TAB LÓGICA ────────────────────────────
    def _tab_logica(self, tab):
        tk.Label(tab, text="Binarios de 4 bits  (0000 - 1111)",
                 font=("Consolas", 8), bg=BG, fg=SUBTEXT).pack(pady=(6, 0))

        f = tk.Frame(tab, bg=BG)
        f.pack(pady=6)

        self._op_btns_logic = {}
        layout = [
            [("1",OVERLAY,TEXT),("0",OVERLAY,TEXT),("C",  ROJO,  BG)       ],
            [("AND", AZUL, BG), ("OR",  AZUL, BG), ("XOR", AZUL, BG)       ],
            [("NOT",MORADO, BG),("=",  VERDE, BG, 2)                        ],
        ]
        for r, row in enumerate(layout):
            c = 0
            for item in row:
                txt, col, fg = item[0], item[1], item[2]
                span = item[3] if len(item) > 3 else 1
                b = self._btn(f, txt, r, c,
                              lambda t=txt: self._logic_click(t),
                              color=col, fg=fg, colspan=span)
                if txt in ("AND", "OR", "XOR"):
                    self._op_btns_logic[txt] = (b, col, fg)
                c += span

        tk.Label(tab, text="⌨  0 1  & AND  | OR  ^ XOR  ~ NOT  Enter=igual",
                 font=("Consolas", 7), bg=BG, fg=OVERLAY).pack(pady=(2, 0))

    def _logic_click(self, char):
        if char == "C":
            self._reset(); self._highlight_op_btn(None)
        elif char in ("AND", "OR", "XOR"):
            if self.expresion:
                self.operando1 = int(self.expresion, 2)
                self.operacion = char
                self.lbl_secondary.config(text=f"{self.expresion} {char}")
                self.expresion = ""
                self._highlight_op_btn(self._op_btns_logic.get(char))
                self._update_status(f"op: {char}")
        elif char == "NOT":
            if self.expresion:
                res = asm_not(int(self.expresion, 2), 0) & 0xF
                result = bin(res)[2:].zfill(4)
                self.lbl_secondary.config(text=f"NOT {self.expresion} =")
                self.lbl_main.config(text=result)
                self._add_historial(f"NOT {self.expresion} = {result}")
                self.expresion = result
        elif char == "=":
            if self.operando1 is not None and self.expresion:
                n2 = int(self.expresion, 2)
                op = self.operacion
                if   op == "AND": res = asm_and(self.operando1, n2)
                elif op == "OR":  res = asm_or (self.operando1, n2)
                elif op == "XOR": res = asm_xor(self.operando1, n2)
                res &= 0xF
                result  = bin(res)[2:].zfill(4)
                op1_bin = bin(self.operando1)[2:].zfill(4)
                op2_bin = bin(n2)[2:].zfill(4)
                entrada = f"{op1_bin} {op} {op2_bin}"
                self.lbl_secondary.config(text=f"{entrada} =")
                self.lbl_main.config(text=result)
                self._add_historial(f"{entrada} = {result}")
                self._highlight_op_btn(None)
                self._update_status()
                self.expresion = result
                self.operando1 = None; self.operacion = None
        else:
            if char in "01" and len(self.expresion) < 4:
                self.expresion += char
                self.lbl_main.config(text=self.expresion)

    # ── TAB CONVERSIÓN ────────────────────────
    def _tab_conversion(self, tab):
        tk.Label(tab, text="BIN: 8 dígitos  |  HEX: 2 dígitos",
                 font=("Consolas", 8), bg=BG, fg=SUBTEXT).pack(pady=(6, 0))

        f = tk.Frame(tab, bg=BG)
        f.pack(pady=6)

        layout = [
            [("7",OVERLAY,TEXT),("8",OVERLAY,TEXT),("9",OVERLAY,TEXT),("A",CELESTE,BG)],
            [("4",OVERLAY,TEXT),("5",OVERLAY,TEXT),("6",OVERLAY,TEXT),("B",CELESTE,BG)],
            [("1",OVERLAY,TEXT),("2",OVERLAY,TEXT),("3",OVERLAY,TEXT),("C",CELESTE,BG)],
            [("⌫",  ROJO,  BG), ("0",OVERLAY,TEXT),("E",CELESTE, BG),("D",CELESTE,BG)],
            [("AC", ROJO,  BG), ("F",CELESTE, BG)                                     ],
        ]
        for r, row in enumerate(layout):
            for c, (txt, col, fg) in enumerate(row):
                self._btn(f, txt, r, c,
                          lambda t=txt: self._conv_click(t),
                          color=col, fg=fg)

        btn_f = tk.Frame(tab, bg=BG)
        btn_f.pack(pady=4)
        tk.Button(btn_f, text="BIN ➜ HEX", width=12, height=1,
                  font=("Consolas", 10, "bold"), bg=NARANJA, fg=BG,
                  activebackground=BG, activeforeground=NARANJA,
                  relief="flat", cursor="hand2",
                  command=self._bin_to_hex).pack(side="left", padx=6)
        tk.Button(btn_f, text="HEX ➜ BIN", width=12, height=1,
                  font=("Consolas", 10, "bold"), bg=AMBAR, fg=BG,
                  activebackground=BG, activeforeground=AMBAR,
                  relief="flat", cursor="hand2",
                  command=self._hex_to_bin).pack(side="left", padx=6)

        tk.Label(tab, text="⌨  0-9 A-F  Backspace=borrar  Esc=limpiar",
                 font=("Consolas", 7), bg=BG, fg=OVERLAY).pack(pady=(2, 0))

    def _conv_click(self, char):
        if char == "AC":
            self._reset()
        elif char == "⌫":
            self.expresion = self.expresion[:-1]
            self.lbl_main.config(text=self.expresion or "0")
        else:
            if len(self.expresion) < 8:
                self.expresion += char
                self.lbl_main.config(text=self.expresion)

    def _bin_to_hex(self):
        val = self.lbl_main.cget("text")
        if not val or val == "0":
            self._error("Ingresa un binario de 8 bits"); return
        num = asm_bin_to_num((val + "\n").encode())
        if num == -1:
            self._error("Binario inválido — exactamente 8 bits (solo 0 y 1)"); return
        res = hex(num & 0xFF)[2:].upper().zfill(2)
        self.lbl_secondary.config(text=f"BIN {val}  =")
        self.lbl_main.config(text=res)
        self._add_historial(f"BIN {val} → {res}")
        self.expresion = res

    def _hex_to_bin(self):
        val = self.lbl_main.cget("text")
        if not val or val == "0":
            self._error("Ingresa un hexadecimal de 2 dígitos"); return
        if len(val) == 1:  val = "0" + val
        elif len(val) > 2: val = val[-2:]
        num = asm_hex_to_num((val + "\n").encode())
        if num == -1:
            self._error("Hexadecimal inválido — 2 dígitos (0-9, A-F)"); return
        res = bin(num & 0xFF)[2:].zfill(8)
        self.lbl_secondary.config(text=f"HEX {val.upper()}  =")
        self.lbl_main.config(text=res)
        self._add_historial(f"HEX {val.upper()} → {res}")
        self.expresion = res

    # ── TECLADO ──────────────────────────────
    def _bind_keys(self):
        self.root.bind("<Key>", self._on_key)

    def _on_key(self, event):
        k = event.keysym
        c = event.char

        if k in ("Escape", "Delete"):
            self._reset(); return
        if k == "BackSpace":
            self.expresion = self.expresion[:-1]
            self.lbl_main.config(text=self.expresion or "0"); return

        tab = self._tab_actual
        if tab == "arit":
            if c in "0123456789":     self._arit_click(c)
            elif c in "+-":           self._arit_click(c)
            elif c == "*":            self._arit_click("×")
            elif c == "/":            self._arit_click("÷")
            elif k in ("Return","KP_Enter","equal"): self._arit_click("=")
            elif c in ("c","C"):      self._reset()
        elif tab == "logic":
            if c in "01":             self._logic_click(c)
            elif k in ("Return","KP_Enter","equal"): self._logic_click("=")
            elif c == "&" and self.expresion: self._logic_click("AND")
            elif c == "|" and self.expresion: self._logic_click("OR")
            elif c == "^" and self.expresion: self._logic_click("XOR")
            elif c == "~" and self.expresion: self._logic_click("NOT")
            elif c in ("c","C"):      self._reset()
        elif tab == "conv":
            if c.upper() in "0123456789ABCDEF": self._conv_click(c.upper())
            elif c in ("c","C"):      self._reset()

    # ── UTILIDADES ───────────────────────────
    def _reset(self):
        self.expresion = ""
        self.operando1 = None
        self.operacion = None
        self.lbl_main.config(text="0")
        self.lbl_secondary.config(text="")
        self.lbl_residuo.config(text="")
        self._highlight_op_btn(None)
        self._update_status()

    def _error(self, msg):
        self.lbl_main.config(text="ERROR")
        messagebox.showerror("Error", msg)
        self._reset()


if __name__ == "__main__":
    root = tk.Tk()
    Calculadora(root)
    root.mainloop()