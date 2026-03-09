; ============================================
; asm_conversion.asm
; Responsable: Emmi
; Conversiones binario/hexadecimal para interfaz Python
; Convención C x86-64: RDI = char* → RAX = valor o -1
; ============================================

section .text

; compatibilidad SysV / Windows
%ifdef WIN64
%macro PASS1 0
    mov rdi, rcx        ; primer argumento en RCX pasará a RDI
%endmacro
%else
%macro PASS1 0
%endmacro
%endif

; ============================================
; asmBinToNum
; Entrada : RDI = char* ej: "10101010\n"
; Salida  : RAX = 0..255 o -1 si error
; Acepta exactamente 8 dígitos binarios (0/1)
; ============================================
global asmBinToNum
asmBinToNum:
    PASS1
    push rbx
    push rcx
    mov rsi, rdi        ; RDI → RSI para leer bytes
    xor rax, rax
    xor rbx, rbx        ; índice

.bin_loop:
    movzx rcx, byte [rsi + rbx]
    cmp cl, 10          ; \n = fin
    je  .bin_check
    cmp cl, 0           ; null = fin
    je  .bin_check
    cmp cl, '0'
    je  .bin_0
    cmp cl, '1'
    je  .bin_1
    jmp .bin_err        ; carácter inválido

.bin_0:
    shl rax, 1
    jmp .bin_next

.bin_1:
    shl rax, 1
    or  rax, 1

.bin_next:
    inc rbx
    cmp rbx, 8
    jg  .bin_err        ; más de 8 dígitos
    jmp .bin_loop

.bin_check:
    cmp rbx, 8          ; exactamente 8 dígitos
    jne .bin_err
    pop rcx
    pop rbx
    ret

.bin_err:
    mov rax, -1
    pop rcx
    pop rbx
    ret

; ============================================
; asmHexToNum
; Entrada : RDI = char* ej: "AA\n"
; Salida  : RAX = 0..255 o -1 si error
; Acepta exactamente 2 dígitos hex (0-9, A-F, a-f)
; ============================================
global asmHexToNum
asmHexToNum:
    PASS1
    push rbx
    push rcx
    mov rsi, rdi        ; RDI → RSI
    xor rax, rax
    xor rbx, rbx        ; índice

.hex_loop:
    movzx rcx, byte [rsi + rbx]
    cmp cl, 10          ; \n = fin
    je  .hex_check
    cmp cl, 0           ; null = fin
    je  .hex_check

    ; shift DESPUÉS de verificar fin (evita corrupción en último char)
    shl rax, 4

    cmp cl, '0'
    jl  .hex_err
    cmp cl, '9'
    jle .hex_digit
    cmp cl, 'A'
    jl  .hex_err
    cmp cl, 'F'
    jle .hex_upper
    cmp cl, 'a'
    jl  .hex_err
    cmp cl, 'f'
    jle .hex_lower
    jmp .hex_err

.hex_digit:
    sub cl, '0'
    movzx rcx, cl
    or  rax, rcx
    jmp .hex_next

.hex_upper:
    sub cl, 'A'
    add cl, 10
    movzx rcx, cl
    or  rax, rcx
    jmp .hex_next

.hex_lower:
    sub cl, 'a'
    add cl, 10
    movzx rcx, cl
    or  rax, rcx

.hex_next:
    inc rbx
    cmp rbx, 2
    jg  .hex_err        ; más de 2 dígitos
    jmp .hex_loop

.hex_check:
    cmp rbx, 2          ; exactamente 2 dígitos
    jne .hex_err
    pop rcx
    pop rbx
    ret

.hex_err:
    mov rax, -1
    pop rcx
    pop rbx
    ret