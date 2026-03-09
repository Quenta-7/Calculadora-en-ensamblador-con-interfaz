# Calculadora UNSAAC — Ensamblador x86-64

Una calculadora moderna con interfaz gráfica (GUI) que implementa operaciones matemáticas, lógicas y de conversión usando **ensamblador x86-64** compilado a una librería compartida, integrada con Python.

## 📋 Descripción del Proyecto

Este proyecto combina la potencia del ensamblador x86-64 con la facilidad de uso de una interfaz gráfica Python usando Tkinter. La aplicación está optimizada para el rendimiento mediante la invocación de funciones en lenguaje ensamblador desde Python mediante `ctypes`.

**Asignatura:** Organización y Arquitectura del Computador  
**Universidad:** Universidad Nacional de San Antonio Abad del Cusco
**Facultad:** Ingeniería Eléctrica, Electrónica, Informática y Mecánica  
**Escuela:** Profesional de Ingeniería Informática y de Sistemas  
**Docente:** Ing. Vanesa Lavilla Alvarez  
**Integrantes:**
- Emmi Daniela Huaman Tairo
- Jose Francisco Quentasi Juachin  
- Efrain Vitorino Marin

## ✨ Características Principales

### 🎨 Interfaz Gráfica (GUI)
- **Pantalla de bienvenida** con información de la universidad y equipo
- **Tema visual oscuro** optimizado para la comodidad visual
- **Interfaz responsiva** con historial en tiempo real
- **Sistema de pestañas** para acceso rápido a diferentes modos de cálculo
- **Paleta de colores profesional:** Catppuccin (morado, azul, naranja, verde, etc.)
- **Tamaño fijo no redimensionable:** 660×720 píxeles

### 📐 Operaciones Aritméticas
- Suma, Resta, Multiplicación, División
- Cálculo automático de residuo en divisiones
- Soporte para enteros hasta 6 dígitos
- Validación contra división por cero

### 🔢 Operaciones Lógicas (4 bits)
- AND (⊈) - Conjunción lógica
- OR (∪) - Disyunción lógica
- XOR (⊕) - OR exclusivo
- NOT (¬) - Negación (complemento a 1)
- Rango: 0000 a 1111 (0-15 en decimal)

### 🔄 Conversiones Numéricas
- **Binario ↔ Hexadecimal:**
  - Binario: 8 bits exactos (0-255 decimal)
  - Hexadecimal: 2 dígitos (00-FF)
  - Validación de formato automática

## 📁 Estructura del Proyecto

```
Calculadora-en-ensamblador-con-interfaz/
├── calculadora_gui.py          # Aplicación principal (GUI Tkinter + ctypes)
├── README.md                   # Este archivo de documentación
├── compile_win.bat             # Script de compilación para Windows
├── build/                      # Directorio de compilación (generado)
│   ├── aritmetica.o           # Objeto compilado de aritmetica.asm
│   ├── logica.o               # Objeto compilado de logica.asm
│   ├── conversion.o           # Objeto compilado de conversion.asm
│   ├── libcalc.so             # Librería compartida (Linux)
│   ├── libcalc.dll            # Librería dinámica (Windows)
│   └── libcalc.exp            # Tabla de exportación (Windows)
├── scripts/
│   └── compile_gui.sh         # Script de compilación para Linux
└── src/                        # Código fuente en ensamblador
    ├── aritmetica.asm         # Funciones aritméticas (Autor: José)
    ├── logica.asm             # Funciones lógicas (Autor: Efraín)
    ├── conversion.asm         # Funciones de conversión (Autor: Emmi)
    └── libcalc.def            # Definición de exportación (Windows)
```

## 🛠️ Requisitos

### Sistema Operativo
- Linux (x86-64)
- Windows 10/11 (64‑bit)

### Dependencias
- **Python 3.x** con tk
- **NASM** (Netwide Assembler) para compilar código ensamblador

#### Linux
- **GNU ld** (linker) para generar la librería compartida

#### Windows
- **Visual Studio 2019/2022** (carga de trabajo "Desarrollo de escritorio con C++")
- NASM en el PATH (el instalador de Windows suele colocarlo en `C:\Users\<usuario>\AppData\Local\bin\NASM`)

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

#### Linux
Ejecutar el script de compilación:

```bash
bash scripts/compile_gui.sh
```

#### Windows
Ejecutar el archivo por lotes desde PowerShell o CMD:

```powershell
.\compile_win.bat
```

El script para Windows:
- busca `vcvars64.bat` usando `vswhere.exe` para activar el entorno MSVC
- comprueba que NASM esté en el PATH
- ensambla los `.asm` de `src\` y enlaza `build\libcalc.dll`

Este script:
- Compila cada módulo ASM a objetos `.o`
- Enlaza los objetos para generar `libcalc.so`
- Verifica que no haya errores en la compilación

### 3. Ejecutar la calculadora

```bash
python3 calculadora_gui.py
```

La ventana de la calculadora se abrirá con acceso a todas las funcionalidades.

## ⌨️ Controles y Atajos de Teclado

### Operaciones Aritméticas
| Entrada | Función |
|---------|---------|
| `0-9` | Ingresa dígitos (máx. 6 dígitos) |
| `+` `-` `*` `/` | Operadores aritméticos |
| `Enter` / `=` | Ejecuta el cálculo |
| `Backspace` `←` | Borra el último carácter |
| `Escape` / `Delete` / `C` | Limpia toda la operación |

### Operaciones Lógicas (4 bits)
| Entrada | Función |
|---------|---------|
| `0` `1` | Ingresa dígitos binarios (máx. 4 bits) |
| `&` | Operación AND (requiere operando previo) |
| `\|` | Operación OR |
| `^` | Operación XOR |
| `~` | Operación NOT (complemento a 1) |
| `Enter` / `=` | Calcula la operación lógica |
| `Escape` / `C` | Limpia la operación |

### Conversiones (Hexadecimal ↔ Binario)
| Entrada | Función |
|---------|---------|
| `0-9` `A-F` | Ingresa dígitos hexadecimales o binarios |
| `Backspace` `←` | Borra el último carácter |
| `Escape` / `C` | Limpia la entrada |
| Botón `BIN ➜ HEX` | Convierte 8 bits binarios a hexadecimal |
| Botón `HEX ➜ BIN` | Convierte 2 dígitos hexadecimales a binario |

## 🏗️ Arquitectura Técnica

### Flujo de Ejecución

```
┌─────────────────────────────────┐
│  Pantalla de Bienvenida         │  Muestra logo UNSAAC,
│  (PantallaBienvenida)           │  equipo y docente
└──────────────┬──────────────────┘
               │ Click START
               ▼
┌─────────────────────────────────┐
│  Interfaz Principal (Calculadora)│  Tkinter GUI
│  - 3 Pestañas (Aritm/Log/Conv)  │  - Historial en tiempo real
│  - Display de resultados        │  - Sistema de colores
│  - Botones interactivos         │  - Atajos de teclado
└──────────────┬──────────────────┘
               │
    ┌──────────┴──────────┬─────────────┐
    ▼                     ▼             ▼
┌─────────┐        ┌─────────┐   ┌──────────┐
│ctypes   │        │ctypes   │   │ctypes    │
│CDLL()   │        │CDLL()   │   │CDLL()    │
└────┬────┘        └────┬────┘   └────┬─────┘
     │                  │            │
     ▼                  ▼            ▼
┌──────────────────────────────────────────┐
│         libcalc.so (Compartida)          │ ELF64 (Linux)
│         libcalc.dll (Dinámica)           │ PE/COFF (Windows)
│  - aritmetica.o  (funciones aritm.)      │
│  - logica.o      (funciones lógica)      │   Compiladas con NASM
│  - conversion.o  (funciones conversión)  │
└──────────────────────────────────────────┘
```

### Especificaciones de la GUI

**`calculadora_gui.py` (584 líneas)**
- **PantallaBienvenida:** Pantalla inicial con información académica
- **Calculadora:** Clase principal con interfaz tabular
  - **Columna izquierda:** Display + pestañas de operaciones
  - **Columna derecha:** Historial con scroll automático
  - **Tema:** Paleta Catppuccin (azul oscuro, morado, naranja)
  - **Modo oscuro:** Colores optimizados para vista prolongada
- **Características especiales:**
  - Historial numerado y scrollable con 130 px de ancho
  - Botones reactivos con efectos de presión
  - Resaltado de operadores activos
  - Modo de estado (barra inferior): Muestra modo actual y operación

**Requisitos de GUI:**
- Python 3.x con módulos: `tkinter`, `ctypes`, `PIL` (Pillow - opcional)
- Resolución recomendada: ≥ 1024×768 px
- Ancho de ventana: 660 px (no redimensionable)
- Alto de ventana: 720 px (no redimensionable)

### Funciones Exportadas por libcalc

#### Aritméticas `src/aritmetica.asm`
- `asmSuma(a, b)` → Suma de dos enteros de 64 bits
- `asmResta(a, b)` → Resta (a - b)
- `asmMultiplicacion(a, b)` → Multiplicación de dos enteros
- `asmDivision(a, b)` → División entera (cociente de a ÷ b)
- `asmResiduo(a, b)` → Módulo (residuo de a ÷ b)

#### Lógicas `src/logica.asm`
Todas las operaciones operan sobre 4 bits (0-15):
- `asmAnd(a, b)` → AND lógico (a & b), mascara a 4 bits
- `asmOr(a, b)` → OR lógico (a | b), mascara a 4 bits
- `asmXor(a, b)` → XOR lógico (a ^ b), mascara a 4 bits
- `asmNot(a, b)` → Complemento a 1 (~a), solo usa el primer argumento

#### Conversión `src/conversion.asm`
- `asmBinToNum(char* "binario")` → Convierte cadena binaria (8 bits) a entero (0-255)
  - Entrada: Cadena de 8 dígitos '0'/'1' terminada en '\n' o '\0'
  - Salida: Valor 0-255, o -1 si hay error
- `asmHexToNum(char* "hexadecimal")` → Convierte cadena hexadecimal (2 dígitos) a entero (0-255)
  - Entrada: Cadena con '0'-'9', 'A'-'F' terminada en '\n' o '\0'
  - Salida: Valor 0-255, o -1 si hay error

**Convención de llamada:** 
- **Linux (SysV):** RDI=arg1, RSI=arg2, retorna en RAX
- **Windows (x64 MSVC):** RCX=arg1, RDX=arg2, retorna en RAX

## 👥 Contribuidores

- **José** - Implementación de operaciones aritméticas
- **Efraín** - Implementación de operaciones lógicas
- **Emmi** - Implementación de conversiones

## 📝 Compilación Manual

Si necesita recompilar sin usar el script:

```bash
# Compilar cada módulo (Linux ELF64)
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

# Windows equivalente (MSVC + NASM)
# desde una terminal con `vcvars64.bat` cargado:
#
# nasm -f win64 src\aritmetica.asm -o build\aritmetica.obj
# nasm -f win64 src\logica.asm -o build\logica.obj
# nasm -f win64 src\conversion.asm -o build\conversion.obj
#
# link /DLL /NOENTRY /NODEFAULTLIB \
#      /DEF:src\libcalc.def \
#      /OUT:build\libcalc.dll \
#      build\aritmetica.obj \
#      build\logica.obj \
#      build\conversion.obj
```

## 🐛 Solución de Problemas

### Error: "No se encontró ./build/libcalc.so"
**Causa:** La librería no ha sido compilada  
**Solución:** Ejecutar primero el script de compilación:
```bash
bash scripts/compile_gui.sh
```

### Error: "nasm: command not found"
**Causa:** NASM no está instalado en el sistema  
**Solución - Debian/Ubuntu:**
```bash
sudo apt-get update
sudo apt-get install nasm
```
**Solución - Windows:** Descargar desde https://www.nasm.us/

### Error: "No module named 'tkinter'"
**Causa:** Python no tiene soporte para GUI  
**Solución - Debian/Ubuntu:**
```bash
sudo apt-get install python3-tk
```
**Solución - Fedora/RHEL:**
```bash
sudo dnf install python3-tkinter
```

### Error: "ld: cannot find -lc"
**Causa:** Librerías de C no están disponibles  
**Solución - Debian/Ubuntu:**
```bash
sudo apt-get install build-essential libc6-dev
```

### Error: "libcalc.so: cannot open shared object file"
**Causa:** La librería compilada no está en el PATH correcto  
**Solución:** Asegúrese de que el archivo esté en `./build/libcalc.so`:
```bash
ls -la build/libcalc.so
```

### Error: DLL no funciona en Windows
**Causa:** Variables de entorno no configuradas correctamente  
**Solución:** Usar PowerShell administrativo y ejecutar `compile_win.bat` desde ahí

### La interfaz se ve pequeña o cortada
**Causa:** Resolución de pantalla muy baja  
**Solución recomendada:** Usar resolución ≥ 1024×768 píxeles

## 📚 Referencias Técnicas

- **x86-64 Assembly:** Arquitectura de 64 bits para procesadores Intel/AMD
- **NASM:** Netwide Assembler - ensamblador modular para x86
- **ctypes:** Librería FFI de Python para llamadas C/Nativas
- **Tkinter:** Toolkit GUI estándar de Python

## 📄 Licencia

Proyecto académico de UNSAAC

## 💡 Notas de Desarrollo

- **Interfaz no redimensionable:** 660×720 píxeles (optimizado para resolución ≥1024×768)
- **Tema oscuro profesional:** Paleta Catppuccin para comodidad visual prolongada
- **Límites de cálculo:** 
  - Aritméticas: int64 (−9223372036854775808 a 9223372036854775807)
  - Lógicas: 4 bits (0000 a 1111, enmascarado automático)
  - Conversiones: 8 bits (0-255) para binario, 2 dígitos (00-FF) para hexadecimal
- **Cross-platform:** Windows (x64 MSVC) y Linux (SysV ELF64)
- **Historial:** Se mantiene durante la sesión, se borra al cambiar de pestaña o reiniciar
- **Carga dinámmica:** La librería ASM se carga automáticamente al iniciar el GUI

## 📖 Información Adicional

**Métodos de compilación:**
- **Linux:** `bash scripts/compile_gui.sh` - Automático con NASM y ld
- **Windows:** `.\compile_win.bat` - Automático con NASM y MSVC linker
- **Manual:** Comandos individuales disponibles en [📝 Compilación Manual](#compilación-manual)

**Directorios importantes:**
- `src/` - Código fuente en ensamblador x86-64 (70-150 líneas c/u)
- `build/` - Archivos objeto y librerías compiladas
- `scripts/` - Scripts de compilación para cada SO

---

**Última actualización:** 9 de marzo de 2026  
**Versión:** 1.0  
**Estado:** Completamente funcional en Linux y Windows x64
