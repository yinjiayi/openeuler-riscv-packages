# Scroll 0.1

Scroll is an experimental terminal scrollback wrapper, not a full terminal
emulator. The original README explicitly says it is not recommended for productive
use and cannot correctly handle arbitrary backward cursor jumps/past-line editing.
These limitations are retained, not presented as solved by packaging QA.

Official stable source: https://dl.suckless.org/tools/scroll-0.1.tar.gz
SHA-256: `9eb2d59ce6adf60100bd2171b0d231ddb47e274b29ded02256960a11ecceeed6`.
All ten archive members were fully read and match official tag `0.1`, immutable
commit `0a2d1a06a9eb4b8ad10240c28edf612879385ac6` at https://git.suckless.org/scroll .
The release dist recipe omits LICENSE although scroll.c refers to it. The only
downstream patch adds that exact same-tag ISC notice for Jan Klemkow and Jochen
Sprickerhof; no original member is modified. Recovered LICENSE SHA-256:
`52f5f340941b3f63fc16882f3e17a9aa28751f7aedaf90f88922d14654b00e62`.
Patch provenance/digest and a mandatory prep-time digest assertion bind this notice.
Installed copies in both packages are checked against the same original digest.

Fresh https://aur.archlinux.org/rpc/v5/info?arg%5B%5D=scroll&arg%5B%5D=scroll-git
returns scroll-git0.1.r2.g51ee387-2 with the matching suckless upstream URL. That
VCS record is only an independently verified discovery clue, never the upstream
stable version or a claim of frozen-catalog membership. The distinct AUR package
named scroll is an unrelated breck7 Markdown/npm application and is excluded.
AUR MIT/license and dependency labels are not inherited over actual source review.
No AUR recipe is executed and no upstream write is made.

Retain original default all/install, VERSION/DEFAULT_SOURCE CPPFLAGS, -Os, -lutil,
and default Shift-PageUp/Shift-PageDown bindings; default mouse bindings remain
disabled exactly as upstream. Packaging hardening flags defer early -s stripping
to normal RPM processing so debug products can be generated. No feature is removed.
The full original `make test` remains mandatory unchanged: original ptty usage,
true/false child-status propagation, up.sh and exact original up.log comparison.
A bounded target-only Python driver holds the make stdin writer open until wait
completes, avoiding a devnull/EOF race in original ptty. It inherits all test
stdout/stderr, propagates status and bounds own-group cleanup; no original test
or fixture is rewritten. QEMU test timing is not native/performance proof.

Additional mandatory private-PTY QA runs built, staged and actually installed
binaries. It verifies exact CLI and no-TTY failures, actual 25-line history bytes,
down navigation, ordinary input, alternate-screen passthrough, real resize signal
propagation, child exit37 and terminal restoration. A private bounded independent
terminal fixture answers explicit cursor queries; no user terminal/display is
borrowed. Installed original README/TODO/manpage and recovered license bytes are
digest checked. The noarch Python tests package requires exact base EVR.

Target: locked openEuler24.03 LTS SP3 riscv64 RVA23 QEMU-user, offline unprivileged
build. No local source/compiler/target/RPM/QEMU execution. Inert review/tooling
tests are not runtime or physical acceptance. Exact-head complete CI, real target
build/install/smoke, RPM/SRPM and ordinary-DNF/path evidence still gate protected
explicit squash; auto-merge is not enabled.
