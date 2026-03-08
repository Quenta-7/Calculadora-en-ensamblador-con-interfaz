; ============================================
; asm_aritmetica.asm
; Responsable: José
; Operaciones aritméticas para interfaz Python
; Convención C x86-64: RDI=arg1, RSI=arg2 → RAX
; ============================================

section .text

global asmSuma
asmSuma:
    mov rax, rdi
    add rax, rsi
    ret

global asmResta
asmResta:
    mov rax, rdi
    sub rax, rsi
    ret

global asmMultiplicacion
asmMultiplicacion:
    mov rax, rdi
    imul rax, rsi
    ret

global asmDivision
asmDivision:
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