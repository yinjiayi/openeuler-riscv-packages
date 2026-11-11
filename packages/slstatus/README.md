<!-- SPDX-License-Identifier: Apache-2.0 -->
# slstatus

Official stable1.1 source is SHA-256 pinned and all33 original files were read.
Actual AUR slstatus1.0-2 is only a discovery clue, not the packaged version or
frozen catalog membership. The original ISC notice remains in both packages.

Preserve byte-identical config.h copied by the original Makefile from config.def.h:
default datetime only, one-second interval. All22 original component objects still
build. Original all/install and unmodified manual text remain; only standard RPM
paths/compiler flags and deferred stripping are selected. No original test/check
target exists, so none is removed or bypassed.

The one downstream ISC patch copies interface flags before freeifaddrs in up(),
fixing a source-observed stale dereference without altering the default config.
Target-only deterministic regression compiles actual patched and SHA-bound
original source with fake getifaddrs/freeifaddrs hooks. Fake release mutates a
still-valid static fixture; both up/down and missing-interface/release counts
are mandatory, with original negative controls. This proves ordering semantics,
not allocator, sanitizer, native kernel or complete optional-metric correctness.
Remove the patch when an official stable release includes the equivalent fix.

Mandatory built/staged/installed QA covers exact CLI/version/errors, default UTC
datetime stdout, normal periodic output, USR1 liveness, owned private-Xvfb actual
root WM_NAME updates and TERM/INT cleanup. No EWMH-specific, hardware, nondefault
metric, native, latency or performance claim is made. Target execution, ordinary
DNF installation and complete exact-head CI/physical RPM/SRPM remain acceptance
gates. No local source/compiler/target/RPM/QEMU execution was used.
