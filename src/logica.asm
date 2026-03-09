; ============================================
; asm_logica.asm
; Responsable: Efraín
; Operaciones lógicas de 4 bits para interfaz Python
; Convención C x86-64: RDI=arg1, RSI=arg2 → RAX
; ============================================

section .text

; soporta SysV y MSVC x64
%ifdef WIN64
%macro PASS2 0
    mov rdi, rcx
    mov rsi, rdx
%endmacro
%else
%macro PASS2 0
%endmacro
%endif

global asmAnd
asmAnd:
    PASS2
    mov rax, rdi
    and rax, rsi
    and rax, 0xF
    ret

global asmOr
asmOr:
    PASS2
    mov rax, rdi
    or  rax, rsi
    and rax, 0xF
    ret

global asmXor
asmXor:
    PASS2
    mov rax, rdi
    xor rax, rsi
    and rax, 0xF
    ret

global asmNot
asmNot:
    PASS2
    ; RDI = valor de 4 bits → RAX = NOT de 4 bits
    mov rax, rdi
    not rax
    and rax, 0xF
    ret