<!-- SPDX-License-Identifier: Apache-2.0 -->
# Libedlib

This directory packages the official edlib v1.2.7 release for openEuler
24.03 LTS SP3 on `riscv64`/RVA23. The tag resolves to commit
`ec2310eda1841ab48c14cd3d866778a4f5eb1491`; the HTTPS source archive
is SHA-256 pinned as
`8767bc1b04a1a67282d57662e5702c4908996e96b1753b5520921ff189974621`.
Archive members are regular files or directories under `edlib-1.2.7/`, with
no absolute paths or parent traversal. The official `LICENSE` is MIT, which
resolves the frozen inventory's earlier license-blocked classification.

The v1.2.7 tag still says 1.2.6 in `CMakeLists.txt`. A single-line patch
corrects generated shared library, pkg-config and CMake package versions;
the algorithms are unchanged. `%check` invokes the complete upstream CTest
suite: six randomized alignment groups using their default 100 cases each,
plus specific correctness tests. Installed smoke compiles and links a C
consumer and verifies the known edit distance between `kitten` and
`sitting`. Native RISC-V performance and repository publication are not
claimed from QEMU-user CI. Debian/Ubuntu records are discovery lineage only,
and no external packaging recipe is executed.
