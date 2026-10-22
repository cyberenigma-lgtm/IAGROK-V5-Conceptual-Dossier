# GDT & TSS — DOSSIER TÉCNICO DE BAJO NIVEL
## Global Descriptor Table y Task State Segment en x86 (32 bits)
### Referencia: NeuroOS Genesis — `kernel_ring0_v2.c` | Noxferion

---

## 1. ¿Por qué existen GDT y TSS?

En la arquitectura x86 el procesador trabaja con **segmentación de memoria**.
Antes de que un programa pueda acceder a código o datos, el CPU comprueba dos cosas:

1. **¿Tiene permiso para acceder a ese segmento?** → Lo define la GDT
2. **¿A qué pila debe cambiar si ocurre una excepción o syscall?** → Lo define la TSS

```
CPU ejecuta instrucción
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│  Selector de Segmento  (en CS, DS, SS, ES, FS, GS)     │
│  ┌──────────────────┬────────┬────┐                     │
│  │  Índice GDT (13b)│ TI (1b)│RPL │  RPL = Ring level  │
│  └──────────────────┴────────┴────┘                     │
└─────────────────────────────────────────────────────────┘
         │
         ▼ índice × 8 (cada entrada GDT = 8 bytes)
┌─────────────────────────────────────────────────────────┐
│  GDT[índice]  → Descriptor de Segmento (8 bytes)        │
│  Contiene: base, límite, permisos, DPL (Ring 0 o 3)    │
└─────────────────────────────────────────────────────────┘
         │
         ▼ ¿DPL >= CPL?  (Descriptor Privilege Level >= Current PL)
         ✅ Acceso concedido   /   ❌ #GP General Protection Fault
```

---

## 2. Estructura de la GDT

### 2.1 Descriptor de segmento (8 bytes por entrada)

```
 63      56 55  52 51  48 47    40 39    32
┌──────────┬──────┬──────┬────────┬────────┐
│ Base[31:24]│Flags│Limit │ Access │Base[23:16]│
│  8 bits  │4 bits│[19:16]│ 8 bits │  8 bits│
└──────────┴──────┴──────┴────────┴────────┘
 31      16 15                            0
┌──────────┬────────────────────────────────┐
│ Base[15:0]│        Limit[15:0]            │
│  16 bits │           16 bits             │
└──────────┴────────────────────────────────┘
```

### 2.2 Código C de tu kernel ([`kernel_ring0_v2.c`](file:///c:/Users/cyber/OneDrive/Documentos/NeuroOs/Neuro-OS-Genesis/Quantum-OS-Virgin/kernel_ring0_v2.c#L31-L58))

```c
struct gdt_entry_struct {
    uint16_t limit_low;    // Bits [15:0]  del límite
    uint16_t base_low;     // Bits [15:0]  de la base
    uint8_t  base_middle;  // Bits [23:16] de la base
    uint8_t  access;       // Byte de acceso (permisos)
    uint8_t  granularity;  // Flags [7:4] + Limit[19:16] [3:0]
    uint8_t  base_high;    // Bits [31:24] de la base
} __attribute__((packed));  // SIN padding — crítico para el CPU

struct gdt_ptr_struct {
    uint16_t limit;  // Tamaño total GDT - 1
    uint32_t base;   // Dirección lineal de la GDT
} __attribute__((packed));

gdt_entry_t gdt_entries[8];   // 8 descriptores máximo en NeuroOS
gdt_ptr_t   gdt_ptr;          // Cargado con LGDT
```

### 2.3 Byte de Acceso — bit a bit

```
Bit 7   6   5   4   3   2   1   0
    ┌───┬───┬───┬───┬───┬───┬───┬───┐
    │ P │DPL│DPL│ S │ E │DC │ RW│ A │
    └───┴───┴───┴───┴───┴───┴───┴───┘

P   = Present (1 = segmento válido en memoria)
DPL = Descriptor Privilege Level (00=Ring0 · 11=Ring3)
S   = Descriptor Type (1=segmento código/datos · 0=sistema)
E   = Executable (1=código · 0=datos)
DC  = Direction/Conforming
RW  = Readable/Writable
A   = Accessed (el CPU lo pone a 1 cuando usa el segmento)
```

**Valores usados en NeuroOS:**

| Hex  | Binario    | Significado                        |
|------|------------|------------------------------------|
| `0x9A` | `10011010` | Ring 0, Código, Ejecutable, Legible |
| `0x92` | `10010010` | Ring 0, Datos, Escribible           |
| `0xFA` | `11111010` | Ring 3, Código, Ejecutable, Legible |
| `0xF2` | `11110010` | Ring 3, Datos, Escribible           |
| `0xE9` | `11101001` | TSS (tipo sistema, presente)        |

### 2.4 Byte de Granularidad — bit a bit

```
Bit 7   6   5   4   3   2   1   0
    ┌───┬───┬───┬───┬───┬───┬───┬───┐
    │ G │D/B│ L │AVL│ Limit[19:16]  │
    └───┴───┴───┴───┴───┴───┴───┴───┘

G   = Granularity (0=límite en bytes · 1=límite en páginas de 4KB)
D/B = Default operation size (1=32 bits · 0=16 bits)
L   = 64-bit code segment (solo en IA-32e, normalmente 0)
AVL = Available (reservado para el SO)
```

**Valor `0xCF` en NeuroOS:**
```
0xCF = 1100 1111
       │││└────── Limit[19:16] = 1111 (los 4 bits altos del límite)
       ││└─────── AVL = 0
       │└──────── D/B = 1 (segmento de 32 bits)
       └───────── G   = 1 (límite en páginas de 4KB)
```

Con `limit = 0xFFFFFFFF` y `G=1` → acceso a **todo el espacio de 4 GB**.

---

## 3. Función `gdt_set_gate` — Código Real de NeuroOS

```c
// kernel_ring0_v2.c — línea 498
void gdt_set_gate(int32_t num, uint32_t base, uint32_t limit,
                  uint8_t access, uint8_t gran)
{
    // --- Campo BASE (32 bits fraccionados en 3 partes) ---
    gdt_entries[num].base_low    = (base  & 0xFFFF);        // bits [15:0]
    gdt_entries[num].base_middle = (base  >> 16) & 0xFF;    // bits [23:16]
    gdt_entries[num].base_high   = (base  >> 24) & 0xFF;    // bits [31:24]

    // --- Campo LIMIT (20 bits fraccionados en 2 partes) ---
    gdt_entries[num].limit_low   = (limit & 0xFFFF);        // bits [15:0]
    gdt_entries[num].granularity = (limit >> 16) & 0x0F;    // bits [19:16]

    // --- FLAGS en granularity (bits [7:4]) ---
    gdt_entries[num].granularity |= (gran & 0xF0);          // G, D/B, L, AVL

    // --- PERMISOS ---
    gdt_entries[num].access      = access;
}
```

---

## 4. La GDT de NeuroOS — Tabla completa

```c
void gdt_init(void) {
    gdt_ptr.limit = (sizeof(gdt_entry_t) * 8) - 1;  // 8 entradas × 8 bytes - 1
    gdt_ptr.base  = (uint32_t)&gdt_entries;           // dirección física

    // Entrada 0 → NULL obligatoria (la CPU exige que índice 0 sea nulo)
    gdt_set_gate(0, 0, 0,          0x00, 0x00);  // Selector 0x00 — NEVER USE

    // Entrada 1 → Código del Kernel (Ring 0)
    gdt_set_gate(1, 0, 0xFFFFFFFF, 0x9A, 0xCF);  // Selector 0x08

    // Entrada 2 → Datos del Kernel (Ring 0)
    gdt_set_gate(2, 0, 0xFFFFFFFF, 0x92, 0xCF);  // Selector 0x10

    // Entrada 3 → Código de Usuario (Ring 3)
    gdt_set_gate(3, 0, 0xFFFFFFFF, 0xFA, 0xCF);  // Selector 0x18

    // Entrada 4 → Datos de Usuario (Ring 3)
    gdt_set_gate(4, 0, 0xFFFFFFFF, 0xF2, 0xCF);  // Selector 0x20

    // Entrada 5 → TSS (Task State Segment)
    // → Rellenada por write_tss()

    // Cargar la GDT en el registro GDTR del procesador
    asm volatile("lgdt (%0)" :: "r"(&gdt_ptr));

    // Recargar selectores de segmento con los nuevos valores
    asm volatile(
        "mov $0x10, %ax \n"  // 0x10 = selector de datos Ring 0 (entrada 2)
        "mov %ax, %ds   \n"
        "mov %ax, %es   \n"
        "mov %ax, %fs   \n"
        "mov %ax, %gs   \n"
        "mov %ax, %ss   \n"
        "ljmp $0x08, $1f\n"  // 0x08 = selector de código Ring 0 (entrada 1)
        "1:             \n"  // Far jump para recargar CS
    );
}
```

### Mapa de selectores en memoria

```
Dirección   Selector  Nombre            DPL   Tipo
─────────── ───────── ───────────────── ───── ──────────────
GDT + 0×00   0x0000   NULL descriptor    —    Nulo
GDT + 0×08   0x0008   Kernel Code        0    Código R0
GDT + 0×10   0x0010   Kernel Data        0    Datos  R0
GDT + 0×18   0x0018   User Code          3    Código R3
GDT + 0×20   0x0020   User Data          3    Datos  R3
GDT + 0×28   0x0028   TSS               0    Sistema
```

> El selector se construye como: `índice × 8 | TI | RPL`  
> TI=0 → GDT, RPL=3 → Ring 3. Por eso `0x18 | 3 = 0x1B` en userspace.

---

## 5. TSS — Task State Segment

### 5.1 ¿Para qué sirve la TSS?

Cuando ocurre una **excepción, interrupción o syscall** y el CPU pasa de
Ring 3 → Ring 0, necesita saber:

- **¿A qué pila cambiar?** (la pila del kernel, no la del usuario)
- **¿Cuál es el Stack Pointer del kernel?** (`esp0`)
- **¿Cuál es el Stack Segment del kernel?** (`ss0`)

Sin la TSS, el CPU no puede hacer el cambio de privilegio seguro.

### 5.2 Estructura de la TSS en NeuroOS

```c
// kernel_ring0_v2.c — línea 45
struct tss_entry_struct {
    // Campo              Offset  Descripción
    uint32_t prev_tss;  // +0     TSS del task anterior (task switching, raro usar)
    uint32_t esp0;      // +4     ★ Stack pointer del KERNEL (Ring 0) ← CLAVE
    uint32_t ss0;       // +8     ★ Stack segment del kernel          ← CLAVE
    uint32_t esp1;      // +12    Stack Ring 1 (no usado en Linux/NeuroOS)
    uint32_t ss1;       // +16    Stack Segment Ring 1
    uint32_t esp2;      // +20    Stack Ring 2 (no usado)
    uint32_t ss2;       // +24    Stack Segment Ring 2
    uint32_t cr3;       // +28    Page directory (paginación)
    uint32_t eip;       // +32    Instruction pointer guardado
    uint32_t eflags;    // +36    EFLAGS guardados
    uint32_t eax;       // +40 ┐
    uint32_t ecx;       // +44 │  Registros de propósito general
    uint32_t edx;       // +48 │  (guardados en task switch HW)
    uint32_t ebx;       // +52 │
    uint32_t esp;       // +56 │
    uint32_t ebp;       // +60 │
    uint32_t esi;       // +64 │
    uint32_t edi;       // +68 ┘
    uint32_t es;        // +72 ┐
    uint32_t cs;        // +76 │  Selectores de segmento guardados
    uint32_t ss;        // +80 │
    uint32_t ds;        // +84 │
    uint32_t fs;        // +88 │
    uint32_t gs;        // +92 ┘
    uint32_t ldt;       // +96    Local Descriptor Table selector
    uint32_t trap;      // +100   Debug trap flag
    uint32_t iomap_base;// +104   Offset al mapa de puertos I/O
} __attribute__((packed));
```

**Tamaño total: 104 bytes** (más el mapa I/O si se usa).

### 5.3 Función `write_tss` — Código Real de NeuroOS

```c
void write_tss(int32_t num, uint16_t ss0, uint32_t esp0) {
    uint32_t base  = (uint32_t)&tss_entry;
    uint32_t limit = base + sizeof(tss_entry_t);

    // 1. Registrar la TSS como un descriptor especial en la GDT
    //    access=0xE9 → TSS de 32 bits, presente, Ring 0
    gdt_set_gate(num, base, limit, 0xE9, 0x00);

    // 2. Limpiar toda la estructura a cero
    k_memset(&tss_entry, 0, sizeof(tss_entry_t));

    // 3. Solo nos importa decirle al CPU:
    //    "cuando hagas ring3 → ring0, usa esta pila"
    tss_entry.ss0  = ss0;   // 0x10 → selector de datos del kernel
    tss_entry.esp0 = esp0;  // dirección de la pila del kernel

    // 4. El I/O permission bitmap no se usa → apuntar más allá del descriptor
    tss_entry.iomap_base = sizeof(tss_entry_t);
}
```

### 5.4 Carga de la TSS con `LTR`

```c
// Después de gdt_init() y write_tss(), cargar el selector TSS en el registro TR
asm volatile("ltr %%ax" :: "a"(0x2B));
// 0x2B = 0x28 (selector TSS entrada 5) | RPL=3
//        índice 5 × 8 = 0x28, con bit 0-1 = 11 (RPL=3) → 0x2B
```

---

## 6. Flujo completo: Ring 3 → Ring 0 via syscall/excepción

```
┌─────────────────────────────────────────────────────────────────────┐
│  Userspace (Ring 3) ejecuta INT 0x80 o SYSCALL                     │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  CPU comprueba IDT → busca el handler de la interrupción           │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  ¿Hay cambio de privilegio? (CPL 3 → DPL 0 del handler)           │
│  SÍ → CPU lee TSS.ss0 y TSS.esp0                                  │
│       CPU cambia SS y ESP a los valores del kernel                 │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  CPU empuja en la pila del KERNEL:                                 │
│    SS_usuario, ESP_usuario, EFLAGS, CS_usuario, EIP_usuario        │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  CPU salta al handler de la IDT en Ring 0                         │
│  → kernel puede acceder a toda la memoria                          │
│  → IAGROK / NeuroOS puede ejecutar instrucciones privilegiadas     │
└─────────────────────────────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│  IRET (Return from Interrupt)                                      │
│  CPU restaura EIP, CS, EFLAGS, ESP, SS del usuario               │
│  → Regreso transparente a Ring 3                                   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 7. Registro GDTR — Cómo el CPU encuentra la GDT

El registro `GDTR` (48 bits) contiene:

```
 47                    16  15          0
┌────────────────────────┬─────────────┐
│   Base (32 bits)       │ Limit (16b) │
│   Dirección de la GDT  │  Tamaño-1  │
└────────────────────────┴─────────────┘
```

```c
// En NeuroOS:
gdt_ptr.limit = (sizeof(gdt_entry_t) * 8) - 1;  // 8 × 8 - 1 = 63 bytes
gdt_ptr.base  = (uint32_t)&gdt_entries;

asm volatile("lgdt (%0)" :: "r"(&gdt_ptr));      // Carga GDTR
```

Equivalentemente con `SGDT` puedes leer la GDT que está activa:
```nasm
sgdt [gdtr_buffer]   ; lee el GDTR actual → 6 bytes en gdtr_buffer
```

---

## 8. GDT en x86-64 (Long Mode) — Diferencias

En **64 bits** la segmentación está mayormente desactivada:

| Campo | x86 (32 bits) | x86-64 (64 bits) |
|---|---|---|
| Segmentación activa | ✅ Completa | ❌ Ignorada (base=0, limit=4GB) |
| GDT obligatoria | ✅ | ✅ (pero solo para CS, SS) |
| TSS | 104 bytes | 128 bytes (añade RSP0, IST1–7) |
| Selectors de segmento | 16 bits | 16 bits (igual) |
| FS/GS | Igual | FS y GS usados para TLS (thread local) |

En x86-64, **FS.base** y **GS.base** se pueden escribir directamente con `WRMSR`
sin pasar por la GDT (instrucción `WRFSBASE`/`WRGSBASE`).

---

## 9. Tabla de Referencia Rápida — Selectores NeuroOS

```
Uso                 Selector  GDT idx  Access  Gran   Ring
──────────────────  ────────  ───────  ──────  ─────  ────
NULL                 0x0000      0     0x00    0x00    —
Kernel Code (CS)     0x0008      1     0x9A    0xCF    0
Kernel Data (DS/SS)  0x0010      2     0x92    0xCF    0
User Code            0x0018      3     0xFA    0xCF    3
User Data            0x0020      4     0xF2    0xCF    3
TSS                  0x002B      5     0xE9    0x00    0
```

---

## 10. Comandos de inspección en QEMU/GDB

```bash
# Conectar GDB al kernel NeuroOS en QEMU
gdb -ex "target remote :1234"

# Ver el GDTR (registro de la GDT)
(gdb) info registers gdtr

# Volcar las primeras 6 entradas de la GDT (48 bytes desde base)
(gdb) x/6xg <base_address>

# Ver la TSS
(gdb) x/26xw <tss_address>

# En QEMU monitor:
(qemu) info registers
(qemu) xp /8xg 0x<gdt_base>   # examinar GDT en memoria física
```

---

## 11. Errores comunes y síntomas

| Error | Causa | Síntoma |
|---|---|---|
| `#GP` General Protection Fault | Selector inválido o DPL menor que CPL | Triple fault / reinicio |
| `#TS` Invalid TSS | TSS no está marcada como presente en GDT | Fallo al cambiar de ring |
| `#SS` Stack Fault | `esp0` apunta a memoria no mapeada | Fallo al manejar interrupción |
| GDT con padding | Falta `__attribute__((packed))` | Descriptores corrompidos, fallo silencioso |
| `lgdt` con base incorrecta | Apunta a stack o dirección temporal | Fallo al siguiente context switch |

---

*Documento generado por IAGROK V5 / NeuroOS Genesis — Noxferion*  
*Referencia de código: [`kernel_ring0_v2.c`](file:///c:/Users/cyber/OneDrive/Documentos/NeuroOs/Neuro-OS-Genesis/Quantum-OS-Virgin/kernel_ring0_v2.c)*
