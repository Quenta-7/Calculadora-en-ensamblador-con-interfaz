// ════════════════════════════════════════════════════
//  CALCULADORA ASM — main.js
//  Puente entre el formulario HTML y WebAssembly
//  El .wasm contiene las instrucciones en ensamblador
// ════════════════════════════════════════════════════

// WASM embebido en Base64 (compilado desde operaciones.wat)
const WASM_BASE64 = "AGFzbQEAAAABDAJgAn9/AX9gAX8BfwMPDgAAAAAAAAAAAQAAAAEAB24OBHN1bWEAAAVyZXN0YQABC211bHRpcGxpY2FyAAIHZGl2aWRpcgADBm1vZHVsbwAEA2FuZAAFAm9yAAYDeG9yAAcDbm90AAgDc2hsAAkDc2hyAAoGZ2V0Qml0AAsDYWJzAAwIcG90ZW5jaWEADQqhAQ4HACAAIAFqCwcAIAAgAWsLBwAgACABbAsHACAAIAFtCwcAIAAgAW8LBwAgACABcQsHACAAIAFyCwcAIAAgAXMLBwAgAEF/cwsHACAAIAF0CwcAIAAgAXYLCgAgACABdkEBcQsQACAAIABBH3VzIABBH3VrCysBAn9BASECQQAhAwJAA0AgAyABTg0BIAIgAGwhAiADQQFqIQMMAAsLIAIL";

// Instrucciones ASM equivalentes para mostrar en el log
const ASM_CODE = {
  suma:         `MOV EAX, A\nADD EAX, B\nRET`,
  resta:        `MOV EAX, A\nSUB EAX, B\nRET`,
  multiplicar:  `MOV EAX, A\nIMUL EAX, B\nRET`,
  dividir:      `MOV EAX, A\nCDQ\nIDIV B\nRET`,
  modulo:       `MOV EAX, A\nCDQ\nIDIV B\nMOV EAX, EDX\nRET`,
  and:          `MOV EAX, A\nAND EAX, B\nRET`,
  or:           `MOV EAX, A\nOR  EAX, B\nRET`,
  xor:          `MOV EAX, A\nXOR EAX, B\nRET`,
  not:          `MOV EAX, A\nNOT EAX\nRET`,
  shl:          `MOV EAX, A\nMOV CL, B\nSHL EAX, CL\nRET`,
  shr:          `MOV EAX, A\nMOV CL, B\nSHR EAX, CL\nRET`,
  decToBin:     `MOV ECX, 31\nbucle:\n  SHR EAX, CL\n  AND EAX, 1\n  LOOP bucle\nRET`,
  decToHex:     `MOV EAX, A\nMOV EBX, 16\nDIV EBX → nibbles\nRET`,
  decToOct:     `MOV EAX, A\nMOV EBX, 8\nDIV EBX → octal\nRET`,
  abs:          `MOV EAX, A\nMOV EDX, EAX\nSAR EDX, 31\nXOR EAX, EDX\nSUB EAX, EDX\nRET`,
  potencia:     `MOV EAX, 1\nMOV ECX, B\nbucle:\n  IMUL EAX, A\n  LOOP bucle\nRET`,
};

let asm; // instancia WebAssembly

// ── Cargar el módulo WASM desde Base64 ──────────────
async function initWasm() {
  const binary = Uint8Array.from(atob(WASM_BASE64), c => c.charCodeAt(0));
  const { instance } = await WebAssembly.instantiate(binary.buffer);
  asm = instance.exports;
  setStatus("✔ WASM cargado — ensamblador listo", "ok");
}

// ── Operación principal ─────────────────────────────
function calcular(operacion) {
  const aRaw = document.getElementById("inputA").value.trim();
  const bRaw = document.getElementById("inputB").value.trim();
  const a = parseInt(aRaw) || 0;
  const b = parseInt(bRaw) || 0;

  if (!asm) { setStatus("⚠ WASM no inicializado", "err"); return; }

  let resultado, extra = "";

  try {
    switch (operacion) {
      // ── Aritméticas ──
      case "suma":        resultado = asm.suma(a, b); break;
      case "resta":       resultado = asm.resta(a, b); break;
      case "multiplicar": resultado = asm.multiplicar(a, b); break;
      case "dividir":
        if (b === 0) { setStatus("⚠ División por cero", "err"); return; }
        resultado = asm.dividir(a, b);
        extra = `  Residuo: ${asm.modulo(a, b)}`;
        break;
      case "modulo":
        if (b === 0) { setStatus("⚠ División por cero", "err"); return; }
        resultado = asm.modulo(a, b); break;
      case "potencia":    resultado = asm.potencia(a, b); break;
      case "abs":         resultado = asm.abs(a); break;

      // ── Lógicas ──
      case "and": resultado = asm.and(a, b); break;
      case "or":  resultado = asm.or(a, b); break;
      case "xor": resultado = asm.xor(a, b); break;
      case "not": resultado = asm.not(a); break;
      case "shl": resultado = asm.shl(a, b); break;
      case "shr": resultado = asm.shr(a, b); break;

      // ── Conversiones (usan getBit del WASM para extraer bits) ──
      case "decToBin": {
        let bin = "";
        for (let i = 7; i >= 0; i--) bin += asm.getBit(a, i); // ← WASM
        resultado = "0b" + bin;
        break;
      }
      case "decToHex":
        resultado = "0x" + (a >>> 0).toString(16).toUpperCase();
        break;
      case "decToOct":
        resultado = "0o" + (a >>> 0).toString(8);
        break;

      default: return;
    }
  } catch (e) {
    setStatus("⚠ Error en operación: " + e.message, "err");
    return;
  }

  mostrarResultado(operacion, a, b, resultado, extra);
  mostrarASM(operacion, a, b);
  animarResultado();
}

// ── UI Helpers ──────────────────────────────────────
function mostrarResultado(op, a, b, res, extra) {
  const display = document.getElementById("display");
  const symbols = {
    suma:"+", resta:"-", multiplicar:"×", dividir:"÷",
    modulo:"%", potencia:"^", abs:"|·|",
    and:"AND", or:"OR", xor:"XOR", not:"NOT",
    shl:"SHL", shr:"SHR",
    decToBin:"→BIN", decToHex:"→HEX", decToOct:"→OCT"
  };
  const sym = symbols[op] || op;
  const expr = (op === "not" || op === "abs" || op.startsWith("dec"))
    ? `${sym}(${a})`
    : `${a} ${sym} ${b}`;

  document.getElementById("expression").textContent = expr;
  document.getElementById("result-value").textContent = res;
  if (extra) document.getElementById("result-extra").textContent = extra;
  else document.getElementById("result-extra").textContent = "";

  setStatus(`✔ Resultado calculado vía WebAssembly`, "ok");
}

function mostrarASM(op, a, b) {
  const code = (ASM_CODE[op] || "")
    .replace(/\bA\b/g, a)
    .replace(/\bB\b/g, b);
  const lines = code.split("\n").map((l, i) => {
    const num = String(i + 1).padStart(2, "0");
    return `<span class="asm-line"><span class="asm-num">${num}</span>  ${l}</span>`;
  }).join("\n");
  document.getElementById("asm-output").innerHTML = lines;
}

function setStatus(msg, type) {
  const el = document.getElementById("status");
  el.textContent = msg;
  el.className = "status " + (type || "");
}

function animarResultado() {
  const el = document.getElementById("result-value");
  el.classList.remove("pop");
  void el.offsetWidth;
  el.classList.add("pop");
}

function limpiar() {
  document.getElementById("inputA").value = "";
  document.getElementById("inputB").value = "";
  document.getElementById("expression").textContent = "_ OP _";
  document.getElementById("result-value").textContent = "---";
  document.getElementById("result-extra").textContent = "";
  document.getElementById("asm-output").innerHTML = '<span class="asm-placeholder">// Presiona una operación...</span>';
  setStatus("Sistema listo", "ok");
}

// ── Init ────────────────────────────────────────────
window.addEventListener("DOMContentLoaded", () => {
  initWasm();
  // Allow Enter key on inputs
  document.querySelectorAll("input").forEach(inp => {
    inp.addEventListener("keydown", e => {
      if (e.key === "Enter") calcular("suma");
    });
  });
});