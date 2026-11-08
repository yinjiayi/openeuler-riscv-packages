<!-- SPDX-License-Identifier: Apache-2.0 -->
# Xssstate 1.1

Official source: https://dl.suckless.org/tools/xssstate-1.1.tar.gz
SHA-256: c4b6f504a6a8eb247bc60960bd65cbf9631c008449a1d71ac4c55e34be1c6011.
All eight source files reviewed. MIT/X Consortium copyright Kai Hendry (2008)
and Christoph Lohmann (2012), complete notices retained. arg.h is distributed
inside that licensed release; no separately imported dependency source.
Canonical tools.suckless.org-xssstate, frozen discovery lineage retained.

The unchanged default all target builds the Xlib/XScreenSaver utility; upstream
has no test target. Xsidle.sh remains an example document as upstream installs
only xssstate and its manual. No source patch or removed feature/test.

Downstream checks mean authored functional checks, not upstream tests: staged
and installed isolated Xvfb with TCP disabled, usage/version/invalid display,
off/on/reset states, numeric idle/countdown and option precedence. They use
forced server state, not a measured timing threshold, physical display, lock
security, DPMS, native RISC-V hardware or performance proof. The example
background infinite loop is not started. Every subprocess has a timeout.

Full official/supplemental provider and namespace admission precedes submission;
locked openEuler 24.03 LTS SP3 riscv64/RVA23 hosted target build/install and
independent physical RPM/SRPM acceptance remain required. No local upstream,
RPM or QEMU execution, auto-merge, or native claim.
