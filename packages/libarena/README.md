# libarena 0.3.7

This recipe onboards the publisher's explicitly identified latest 0.3.7
release, not a version inferred from the old AUR row alone. The retained
discovery row is `aur:libarena`, 0.3.7-1, snapshot
`discovery-20260808T165000Z-9a89920c269462cd`.

Official homepage: https://25thandclement.com/~william/projects/libarena.html

Official archive: https://25thandclement.com/~william/projects/releases/libarena-0.3.7.tgz

Archive SHA-256: `6526933f218fafa5dfecb4189337eab6be3d65af250dc7dc89b1acf19a89d265`.
Its 33 ordinary files, modes and Git blob bytes match the publisher-linked
`rel-0.3.7` lightweight tag, commit
`07d292bb73e035997d3a0768234966778ba8a899`, tree
`dcaa5ffaf940e5bc6ad03d96c9894fe3e42d6d1e`. The original commit object has no
embedded signature, and the lightweight tag has no separate tag object. No
detached signature link was observed on the publisher page; this is not a
claim that every remote endpoint was exhaustively searched or an independent
cryptographic authentication claim. HTTPS origin, fixed digest and exact
Git/source identity are distinct evidence.

## Rights and original notices

The distribution composite is `MIT AND BSD-3-Clause AND
LicenseRef-dh-make-output`. William Ahern's complete project-wide MIT grant
is in original `debian/copyright`, with original 2006 notices in source
files. `src/queue.h` retains the Regents' 1991/1993 three-clause BSD grant;
it is not relabeled MIT. `LicenseRef-dh-make-output` identifies only the
complete original `debian/rules` output exception, not an invented license
for an unidentified historical source script. Its full preserved header is:

```
#!/usr/bin/make -f
# -*- makefile -*-
# Sample debian/rules that uses debhelper.
# This file was originally written by Joey Hess and Craig Small.
# As a special exception, when this file is copied by dh-make into a
# dh-make output file, you may use that output file without restriction.
# This special exception was added by Craig Small in version 0.37 of dh-make.
```

All 33 original ordinary files are copied byte-for-byte as `.notice` files
before any patch or build. The installed license directory contains these
original texts with their 33-entry relative SHA-256 manifest, plus the exact
output-exception header. The newly added API driver carries its own full MIT
grant. No original Debian helper, unused source or regression is pruned from
the source RPM to avoid rights obligations.

## Default behavior and the minimal patch

Upstream's default `all` builds `src/libarena.a`; this remains the first build
target. The recipe additionally invokes upstream's existing `pic` target for
the shared library and installed-library QA, and retains the original install
target, including static archive, libtool archive and six `arena/` headers.
The shared target is an explicit addition, not described as the original
default. Libtool version-info `0:3` predicts `libarena.so.0.0.3`; target ELF and
SONAME evidence must confirm this before acceptance.

The sole patch passes the already-declared `LDFLAGS` through the original
libtool shared-link command. It repairs generic link-flag propagation rather
than adding RISC-V optimization or changing allocator behavior. The recipe
passes RPM compiler/linker hardening flags; their actual target use remains a
CI/product inspection requirement. Remove the patch once upstream propagates
these flags. It does not change original tests, random inputs, feature
choices, compiler definitions or allocator implementations.

Original `make check` is retained exactly. It compiles `stacked` and `grow`
but executes only `stacked`. That program exercises six allocator layering
combinations with randomized allocation data/order and CRC checks, using
`/dev/urandom` and a time-seeded PRNG. It is not a deterministic workload,
timing benchmark or a native-kernel/security certification. `grow` is not
misreported as an executed upstream case. No original test is deleted,
reseeded, changed to allow failure or replaced by the additional driver.

## Additional target and installed QA

The added fixed-input driver has six assertion-bearing cases: aligned arena
reallocation and payload preservation; mark/reset reuse; pool bucket growth
and stricter alignment; nested allocator export/import and ownership; exact
string/binary duplication and formatting; and explicit zero-size
reallocation branches. Assertions remain enabled after RPM flags with
`-UNDEBUG`. Bounded cases do not establish arbitrary allocation sizes, OOM
safety, memory-error freedom, high-load reliability or performance.

Both build-root and installed smoke invoke this same dynamically linked
driver. Installed smoke clears inherited loader overrides, preserves raw
`LD_DEBUG=bindings` trace plus its SHA and real failure exit, and requires
each of six function symbols to bind from the absolute installed driver to
the same physical installed `libarena.so.0.0.3` file. It accepts loader aliases
only through `-ef` file identity, not hard-coded path spellings or broad
substring matches. Data-symbol directional bindings are not asserted.
The driver/source manifest is written after RPM install-post stripping.

The API driver compiles through a build-local `api-include/arena` view of the
original `src/` headers. Before compilation, all six public headers must be
byte-identical to the copies installed into the build root. This preserves
the installed-header API contract without embedding the absolute staged
include directory in driver debug information. Linkage still targets the
staged installed library; RPM debug processing and `check-buildroot` remain
enabled, and installed smoke still verifies all six real library bindings.

## Evidence boundaries

Local intake is inert source/metadata review and trusted repository tooling
validation only: no upstream compiler, regression, RPM, QEMU or installed
target execution is run locally. Target CI must build, run the unchanged
regression and six added cases, install the RPM and run smoke. Green tooling
checks or skipped infrastructure jobs are not successful package builds.
Full product contents, original notices, official and supplemental namespace
and physical RPM/SRPM checks remain independent merge/publication gates.

The recipe requires no undeclared source fetch during build. This does not
assert that the actual CI bridge is network-isolated. Complete metadata
provider projection is not a DNF SAT solution or physical installation proof.
