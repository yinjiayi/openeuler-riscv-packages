<!-- SPDX-License-Identifier: Apache-2.0 -->
# Tree::Simple 1.34

Noarch Perl tree and visitor modules for openEuler 24.03 LTS SP3,
riscv64/RVA23. Fixed CPAN .tgz SHA-256 agrees with MetaCPAN and the
author's CHECKSUMS. Its PAUSE clear signature was verified against the
rotated signing subkey bound to the official primary fingerprint; it
is advisory index evidence, not a detached archive signature. The full
archive SHA-256 remains mandatory. Frozen Ubuntu and Debian stable both identify
libtree-simple-perl 1.34-2; no distro recipe was executed.

The original LICENSE and both module POD notices preserve Infinity
Interactive's same-terms-as-Perl grant. The hand-written Makefile.PL
uses the installed ExtUtils::MakeMaker. No generated helper, source
patch or external fixture is added.

The SPEC runs the entire unchanged upstream default `make test`. It
requires the available Test::Memory::Cycle stack and checks that it loads
so the original memory leak and weak-reference tests are exercised rather
than silently self-skipped. Author-only xt/ files remain out of the
default suite. The installed smoke checks parent-child links, cloning,
and traversal using the packaged visitor. Host results are separate from
actual target RPM/install evidence.
