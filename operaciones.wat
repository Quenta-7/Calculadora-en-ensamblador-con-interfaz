(module

  ;; ════════════════════════════════════════
  ;; CALCULADORA ASM - WebAssembly Text Format
  ;; Operaciones: Aritméticas, Lógicas, Bits
  ;; ════════════════════════════════════════

  ;; ─── OPERACIONES ARITMÉTICAS ─────────────

  (func $suma (export "suma")
    (param $a i32) (param $b i32) (result i32)
    ;; MOV EAX, $a
    ;; ADD EAX, $b
    ;; RET
    local.get $a
    local.get $b
    i32.add
  )

  (func $resta (export "resta")
    (param $a i32) (param $b i32) (result i32)
    ;; MOV EAX, $a
    ;; SUB EAX, $b
    ;; RET
    local.get $a
    local.get $b
    i32.sub
  )

  (func $multiplicar (export "multiplicar")
    (param $a i32) (param $b i32) (result i32)
    ;; MOV EAX, $a
    ;; IMUL EAX, $b
    ;; RET
    local.get $a
    local.get $b
    i32.mul
  )

  (func $dividir (export "dividir")
    (param $a i32) (param $b i32) (result i32)
    ;; MOV EAX, $a
    ;; CDQ
    ;; IDIV $b
    ;; RET (cociente en EAX)
    local.get $a
    local.get $b
    i32.div_s
  )

  (func $modulo (export "modulo")
    (param $a i32) (param $b i32) (result i32)
    ;; MOV EAX, $a
    ;; CDQ
    ;; IDIV $b
    ;; MOV EAX, EDX  (residuo)
    ;; RET
    local.get $a
    local.get $b
    i32.rem_s
  )

  ;; ─── OPERACIONES LÓGICAS ─────────────────

  (func $and (export "and")
    (param $a i32) (param $b i32) (result i32)
    ;; MOV EAX, $a
    ;; AND EAX, $b
    ;; RET
    local.get $a
    local.get $b
    i32.and
  )

  (func $or (export "or")
    (param $a i32) (param $b i32) (result i32)
    ;; MOV EAX, $a
    ;; OR  EAX, $b
    ;; RET
    local.get $a
    local.get $b
    i32.or
  )

  (func $xor (export "xor")
    (param $a i32) (param $b i32) (result i32)
    ;; MOV EAX, $a
    ;; XOR EAX, $b
    ;; RET
    local.get $a
    local.get $b
    i32.xor
  )

  (func $not (export "not")
    (param $a i32) (result i32)
    ;; MOV EAX, $a
    ;; NOT EAX       (invierte todos los bits)
    ;; RET
    local.get $a
    i32.const -1
    i32.xor
  )

  (func $shl (export "shl")
    (param $a i32) (param $bits i32) (result i32)
    ;; MOV EAX, $a
    ;; MOV CL,  $bits
    ;; SHL EAX, CL   (shift left)
    ;; RET
    local.get $a
    local.get $bits
    i32.shl
  )

  (func $shr (export "shr")
    (param $a i32) (param $bits i32) (result i32)
    ;; MOV EAX, $a
    ;; MOV CL,  $bits
    ;; SHR EAX, CL   (shift right)
    ;; RET
    local.get $a
    local.get $bits
    i32.shr_u
  )

  ;; ─── EXTRACCIÓN DE BITS (para conversiones) ──

  (func $getBit (export "getBit")
    (param $num i32) (param $pos i32) (result i32)
    ;; MOV EAX, $num
    ;; MOV CL,  $pos
    ;; SHR EAX, CL
    ;; AND EAX, 1
    ;; RET
    local.get $num
    local.get $pos
    i32.shr_u
    i32.const 1
    i32.and
  )

  ;; ─── VALOR ABSOLUTO ──────────────────────

  (func $abs (export "abs")
    (param $a i32) (result i32)
    ;; CMP EAX, 0
    ;; JGE positivo
    ;; NEG EAX
    ;; positivo: RET
    local.get $a
    i32.abs
  )

  ;; ─── POTENCIA (base^exp) ─────────────────

  (func $potencia (export "potencia")
    (param $base i32) (param $exp i32) (result i32)
    (local $result i32)
    (local $i i32)
    ;; MOV EAX, 1    ; result = 1
    ;; MOV ECX, $exp ; contador
    ;; bucle:
    ;;   IMUL EAX, $base
    ;;   LOOP bucle
    ;; RET
    i32.const 1
    local.set $result
    i32.const 0
    local.set $i
    block $break
      loop $loop
        local.get $i
        local.get $exp
        i32.ge_s
        br_if $break
        local.get $result
        local.get $base
        i32.mul
        local.set $result
        local.get $i
        i32.const 1
        i32.add
        local.set $i
        br $loop
      end
    end
    local.get $result
  )

)