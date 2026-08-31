# nasm

This directory packages NASM 3.02 for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. Distribution aliases are deduplicated to the official
NASM component; no distribution or AUR recipe is executed.

The official stable source archive is checksum pinned, has one safe root and
no links, and carries BSD-2-Clause licensing. The assembler is portable and
generates x86 objects without executing them. `%check` runs upstream's full
`make travis` golden-output suite without suppressed failures.
