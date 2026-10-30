<!-- SPDX-License-Identifier: Apache-2.0 -->
# sshexec 1.2.2

Official source: https://codeberg.org/maandree/sshexec/archive/1.2.2.tar.gz
SHA-256: 7f42b9cd096f6bac9c7700f18b1fbe3b6f04091f17b005322158948e771f0d4e.
ISC copyright 2023, 2024, 2025 Mattias Andree; complete notices retained in both
binary subpackages and unchanged original QA/SRPM source archive. Frozen AUR
sshexec and sshexec-sshcd 1.2.2-1 are lineage, not executed recipes/source proof.

The unchanged default Makefile builds sshexec; no upstream test target exists.
Downstream staged/installed checks use an inert SSH argv-capture stub, then
replay only harmless generated printf commands inside target CI. They compare
all non-NUL ASCII bytes, empty/quoted arguments, shell metacharacters, trailing
newlines, @ followed by digits, option boundaries, strict/lax failure, sshcd
PTY options and error/child statuses. These are not upstream tests, live SSH,
authentication, remote-shell compatibility, non-ASCII or security proof.

One downstream ISC patch emits fixed three-digit octal escapes: @ (0100)
otherwise statically becomes \10. It consumes following safe digits, which
otherwise cannot advance the escaping loop, and uses unsigned ctype inputs.
Not RISC-V-specific; no runtime/exploit claim or upstream write. Remove when
an official fixed release passes these regressions. Other options unchanged.

Full target provider/command/manual namespace admission precedes submission.
Actual locked openEuler 24.03 LTS SP3 riscv64/RVA23 build, ordinary install,
smoke and physical RPM/SRPM acceptance remain CI gates. No local source/RPM/
QEMU execution, auto-merge or native claim.
