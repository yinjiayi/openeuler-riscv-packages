# golden-riscv-inline-asm

The source fixture deliberately rejects `__riscv`. Initial target CI must fail and queue repair. The accepted repair adds `patches/0001-riscv-use-rdcycle.patch`, references it from the SPEC, retains the smoke test, and changes no shared infrastructure.
