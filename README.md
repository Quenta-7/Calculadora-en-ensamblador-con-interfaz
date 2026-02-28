# ⚙ Calculadora ASM — WebAssembly

Calculadora con formulario web donde las operaciones aritméticas, lógicas y de conversión están implementadas en **ensamblador** mediante **WebAssembly (.wat / .wasm)**.

## 🗂 Estructura del proyecto

```
calculadora-asm/
├── index.html        ← Formulario (HTML + CSS)
├── style.css         ← Estilos retro-terminal
├── main.js           ← Puente JS ↔ WebAssembly
├── operaciones.wat   ← ⭐ ENSAMBLADOR (WebAssembly Text)
├── operaciones.wasm  ← Binario compilado del .wat
└── README.md
```

## 🔧 Operaciones implementadas en ensamblador (.wat)

### Aritméticas
| Operación | Instrucción ASM |
|-----------|----------------|
| Suma      | `i32.add` (≡ ADD EAX, EBX) |
| Resta     | `i32.sub` (≡ SUB EAX, EBX) |
| Multiplicar | `i32.mul` (≡ IMUL EAX, EBX) |
| Dividir   | `i32.div_s` (≡ IDIV EBX) |
| Módulo    | `i32.rem_s` (≡ IDIV → EDX) |
| Potencia  | loop con `i32.mul` (≡ IMUL + LOOP) |
| Valor abs | `i32.shr_s` + `i32.xor` + `i32.sub` (≡ SAR + XOR + SUB) |

### Lógicas / Bitwise
| Operación | Instrucción ASM |
|-----------|----------------|
| AND       | `i32.and` (≡ AND EAX, EBX) |
| OR        | `i32.or`  (≡ OR  EAX, EBX) |
| XOR       | `i32.xor` (≡ XOR EAX, EBX) |
| NOT       | `i32.xor` con -1 (≡ NOT EAX) |
| SHL       | `i32.shl` (≡ SHL EAX, CL) |
| SHR       | `i32.shr_u` (≡ SHR EAX, CL) |

### Conversiones
| Operación | Método |
|-----------|--------|
| DEC → BIN | `getBit()` en WASM (SHR + AND por cada bit) |
| DEC → HEX | `.toString(16)` en JS |
| DEC → OCT | `.toString(8)` en JS |

## 🚀 Cómo ejecutar

### Opción A — Servidor local (recomendado)
```bash
# Python
python -m http.server 8080

# Node.js
npx serve .
```
Luego abre: `http://localhost:8080`

### Opción B — Live Server (VS Code)
Instala la extensión **Live Server** → clic derecho en `index.html` → *Open with Live Server*

> ⚠️ **No abrir el index.html directamente** (file://) porque los navegadores bloquean fetch() de archivos locales por seguridad CORS.

## ☁️ Deploy en Netlify
1. Ve a [netlify.com/drop](https://app.netlify.com/drop)
2. Arrastra toda la carpeta `calculadora-asm/`
3. ¡Listo! Obtienes un link público

## 🛠 Compilar el .wat manualmente
Si modificas `operaciones.wat`, recompila con:
```bash
# Online: https://wat2wasm.surge.sh
# O con wabt:
npm install -g wabt
wat2wasm operaciones.wat -o operaciones.wasm
```

---
**Materia:** Arquitectura de Computadoras / Lenguaje Ensamblador  
**Tecnologías:** HTML · CSS · JavaScript · WebAssembly (WAT/WASM)