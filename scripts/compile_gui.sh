#!/bin/bash
# ============================================
# compile_gui.sh
# Compila los módulos ASM separados y genera
# libcalc.so para la interfaz Python
# ============================================

echo "🔨 Compilando módulos para interfaz Python..."
mkdir -p build

echo "  ├─ aritmetica.asm (José)"
nasm -f elf64 src/aritmetica.asm -o build/aritmetica.o
if [ $? -ne 0 ]; then echo "❌ Error compilando aritmetica.asm"; exit 1; fi

echo "  ├─ logica.asm (Efraín)"
nasm -f elf64 src/logica.asm -o build/logica.o
if [ $? -ne 0 ]; then echo "❌ Error compilando logica.asm"; exit 1; fi

echo "  └─ conversion.asm (Emmi)"
nasm -f elf64 src/conversion.asm -o build/conversion.o
if [ $? -ne 0 ]; then echo "❌ Error compilando conversion.asm"; exit 1; fi

echo ""
echo "🔗 Enlazando libcalc.so..."
ld -shared \
    build/aritmetica.o \
    build/logica.o \
    build/conversion.o \
    -o build/libcalc.so

if [ $? -ne 0 ]; then echo "❌ Error generando libcalc.so"; exit 1; fi

echo ""
echo "✅ libcalc.so generada exitosamente"
echo ""
echo "📊 Símbolos exportados:"
nm -D build/libcalc.so | grep " T "
echo ""
echo "🐍 Ejecutar: python3 calculadora_gui.py"