; ============================================
; asm_aritmetica.asm
; Responsable: José
; Operaciones aritméticas para interfaz Python
; Convención C x86-64: RDI=arg1, RSI=arg2 → RAX
; ============================================

section .text

; compatibles con SysV (Linux) y MSVC (Windows x64)
; en Windows los primeros argumentos llegan en rcx, rdx
%ifdef WIN64
%macro PASS2 0
    ; convertir RCX, RDX → RDI, RSI para reutilizar el código existente
    mov rdi, rcx
    mov rsi, rdx
%endmacro
%else
%macro PASS2 0
    ; no-op en SysV
%endmacro
%endif

global asmSuma
asmSuma:
    PASS2
    mov rax, rdi
    add rax, rsi
    ret

global asmResta
asmResta:
    PASS2
    mov rax, rdi
    sub rax, rsi
    ret

global asmMultiplicacion
asmMultiplicacion:
    PASS2
    mov rax, rdi
    imul rax, rsi
    ret

global asmDivision
asmDivision:
    PASS2
    cmp rsi, 0
    je .error
    mov rax, rdi
    xor rdx, rdx
    idiv rsi            ; RAX = cociente, RDX = residuo
    ret
.error:
    mov rax, -1
    ret

global asmResiduo
asmResiduo:
    PASS2
    cmp rsi, 0
    je .error
    mov rax, rdi
    xor rdx, rdx
    idiv rsi            ; RAX = cociente, RDX = residuo
    mov rax, rdx        ; retornar residuo
    ret
.error:
    mov rax, -1
    ret