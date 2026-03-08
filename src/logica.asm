; ============================================
; asm_logica.asm
; Responsable: Efraín
; Operaciones lógicas de 4 bits para interfaz Python
; Convención C x86-64: RDI=arg1, RSI=arg2 → RAX
; ============================================

section .text

global asmAnd
asmAnd:
    mov rax, rdi
    and rax, rsi
    and rax, 0xF
    ret

global asmOr
asmOr:
    mov rax, rdi
    or  rax, rsi
    and rax, 0xF
    ret

global asmXor
asmXor:
    mov rax, rdi
    xor rax, rsi
    and rax, 0xF
    ret

global asmNot
asmNot:
    ; RDI = valor de 4 bits → RAX = NOT de 4 bits
    mov rax, rdi
    not rax
    and rax, 0xF
    ret