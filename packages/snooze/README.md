<!-- SPDX-License-Identifier: Apache-2.0 -->
# snooze

Official stable v0.6 is pinned to peeled commit53e4afe05aaa953370141156fbeb9fc21979e9e0
and SHA-2569abd132f37a8dc8fa1eba012b01379b97df3e280d6ba10833c228b04f8a23c09.
Current AUR0.6-1 is discovery corroboration, not source/license authority.
All ten original text files are preserved/read. The explicit CC0 waiver and
URL in README.md, snooze.c and snooze.1 are retained; unchanged README.md is
distributed as license in both packages. No standalone license file is invented.

Original all/install/compiler flags and default scheduling features remain.
Optional sv/runit service installation is not the root Makefile default and is
not activated. No upstream test/check target exists and none is skipped.
The narrow checked-factor patch bounds duration before suffix multiplication;
valid boundaries/diagnostics and other parse semantics remain unchanged.

Mandatory hosted-target parser regression compiles the full SHA-bound original
and patched sources, with each harness beside its own snooze.c. Two original
unsigned64 wrap controls must reproduce44/61184 before the patched rejection.
Both versions also pass valid/invalid/boundary grammar and deterministic UTC
leap-day/ISO-week/day-of-year/conjunction/impossible-calendar controls. These
are actual source controls, not host execution or general safety certification.

Mandatory ordinary built/staged/installed QA covers dry-run/filter grammar,
timefiles/slack/minimum wait, delay/jitter bounds, signal behavior, command argv
and exit propagation, missing executable and real bounded scheduled execution.
Installed original docs/CC0 notices and exactly one raw/gzip manual are byte
verified. No default compression is disabled. Functional QEMU success does not
prove native clock-change behavior, timing precision/performance or service
supervision. Complete exact-head CI, physical RPM/SRPM, ordinary all-RPM DNF
and protected-main public byte acceptance remain separate gates.
