# Calculadora UNSAAC — Ensamblador x86-64

Una calculadora moderna con interfaz gráfica (GUI) que implementa operaciones matemáticas, lógicas y de conversión usando **ensamblador x86-64** compilado a una librería compartida, integrada con Python.

## 📋 Descripción del Proyecto

Este proyecto combina la potencia del ensamblador x86-64 con la facilidad de uso de una interfaz gráfica Python usando Tkinter. La aplicación está optimizada para el rendimiento mediante la invocación de funciones en lenguaje ensamblador desde Python mediante `ctypes`.

### Universidad
**UNSAAC** (Universidad Nacional de San Antonio Abad del Cusco)

## ✨ Características

### 📐 Operaciones Aritméticas
- Suma
- Resta
- Multiplicación
- División

### 🔢 Operaciones Lógicas
- AND (⊈)
- OR (∪)
- XOR (⊕)
- NOT (¬)

### 🔄 Conversiones
- Binario a Hexadecimal
- Hexadecimal a Binario

## 📁 Estructura del Proyecto

```
Calculadora-en-ensamblador-con-interfaz/
├── calculadora_gui.py       # Interfaz gráfica principal (Python + Tkinter)
├── README.md                # Este archivo
├── scripts/
│   └── compile_gui.sh       # Script para compilar módulos ASM
├── src/
│   ├── aritmetica.asm       # Operaciones aritméticas (José)
│   ├── logica.asm           # Operaciones lógicas (Efraín)
│   └── conversion.asm       # Conversiones numéricas (Emmi)
└── build/                   # Directorio de compilación (generado)
    ├── aritmetica.o
    ├── logica.o
    ├── conversion.o
    └── libcalc.so           # Librería compartida compilada
```

## 🛠️ Requisitos

### Sistema Operativo
- Linux (x86-64)

### Dependencias
- **Python 3.x** con tk
- **NASM** (Netwide Assembler) para compilar código ensamblador
- **GNU ld** (linker) para generar la librería compartida

### Instalación de dependencias (Debian/Ubuntu)

```bash
sudo apt-get update
sudo apt-get install python3 python3-tk nasm gcc
```

## 🚀 Instalación y Uso

### 1. Clonar o descargar el proyecto

```bash
git clone <repositorio>
cd Calculadora
```

### 2. Compilar los módulos de ensamblador

Ejecutar el script de compilación:

```bash
bash scripts/compile_gui.sh
```

Este script:
- Compila cada módulo ASM a objetos `.o`
- Enlaza los objetos para generar `libcalc.so`
- Verifica que no haya errores en la compilación

### 3. Ejecutar la calculadora

```bash
python3 calculadora_gui.py
```

La ventana de la calculadora se abrirá con acceso a todas las funcionalidades.

## ⌨️ Controles

### Operaciones Aritméticas
- Números: `0-9`
- Operadores: `+`, `-`, `*` (×), `/` (÷)
- Igualar: `Enter` o `=`
- Limpiar: `Escape`, `Delete` o `C`
- Backspace: `←` (borra el último carácter)

### Operaciones Lógicas
- Dígitos binarios: `0`, `1`
- AND: `&` (con operando previo)
- OR: `|` (con operando previo)
- XOR: `^` (con operando previo)
- NOT: `~` (con operando previo)
- Igualar: `Enter`
- Limpiar: `Escape` o `C`

### Conversiones
- Hexadecimal: `0-9`, `A-F`
- Binario: `0`, `1`
- Resultado automático después de ingresar los dígitos

## 🏗️ Arquitectura Técnica

### Flujo de Ejecución

```
Interface Tkinter (Python)
         ↓
   calculadora_gui.py
         ↓
    ctypes.CDLL()
         ↓
     libcalc.so (Compilada)
         ↓
   Módulos ASM x86-64
   - aritmetica.asm
   - logica.asm
   - conversion.asm
```

### Funciones Exportadas por libcalc.so

**Aritméticas:**
- `asmSuma(a, b)` → retorna a + b
- `asmResta(a, b)` → retorna a - b
- `asmMultiplicacion(a, b)` → retorna a × b
- `asmDivision(a, b)` → retorna a ÷ b

**Lógicas:**
- `asmAnd(a, b)` → retorna a & b
- `asmOr(a, b)` → retorna a | b
- `asmXor(a, b)` → retorna a ^ b
- `asmNot(a)` → retorna ~a

**Conversiones:**
- `asmBinToHex(cadena_binaria)` → retorna conversión a hexadecimal
- `asmHexToBin(cadena_hexadecimal)` → retorna conversión a binario

## 👥 Contribuidores

- **José** - Implementación de operaciones aritméticas
- **Efraín** - Implementación de operaciones lógicas
- **Emmi** - Implementación de conversiones

## 📝 Compilación Manual

Si necesita recompilar sin usar el script:

```bash
# Compilar cada módulo
nasm -f elf64 src/aritmetica.asm -o build/aritmetica.o
nasm -f elf64 src/logica.asm -o build/logica.o
nasm -f elf64 src/conversion.asm -o build/conversion.o

# Enlazar la librería compartida
ld -shared \
    build/aritmetica.o \
    build/logica.o \
    build/conversion.o \
    -o build/libcalc.so

# Ver símbolos exportados
nm -D build/libcalc.so | grep " T "
```

## 🐛 Solución de problemas

### Error: "No se encontró ./build/libcalc.so"

**Solución:** Ejecutar primero el script de compilación:
```bash
bash scripts/compile_gui.sh
```

### Error: "nasm: command not found"

**Solución:** Instalar NASM:
```bash
sudo apt-get install nasm
```

### Error: "No module named 'tkinter'"

**Solución:** Instalar python3-tk:
```bash
sudo apt-get install python3-tk
```

## 📚 Referencias Técnicas

- **x86-64 Assembly:** Arquitectura de 64 bits para procesadores Intel/AMD
- **NASM:** Netwide Assembler - ensamblador modular para x86
- **ctypes:** Librería FFI de Python para llamadas C/Nativas
- **Tkinter:** Toolkit GUI estándar de Python

## 📄 Licencia

Proyecto académico de UNSAAC

## 💡 Notas de Desarrollo

- La interfaz está optimizada para resolución 400x680 px y NO es redimensionable
- El tema oscuro proporciona mejor experiencia visual
- Los cálculos de gran magnitud pueden desbordarse en x86-64 (int64)
- La librería se genera en tiempo de compilación, no en tiempo de ejecución

---

**Última actualización:** 8 de marzo de 2026
