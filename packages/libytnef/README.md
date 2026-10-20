<!-- SPDX-License-Identifier: Apache-2.0 -->
# libytnef

This package maps the inventory's exact `libytnef` key to the official
[ytnef v2.1.2 release](https://github.com/Yeraze/ytnef/releases/tag/v2.1.2)
for openEuler 24.03 LTS SP3 on `riscv64`/RVA23. The tag resolves to commit
`d9f089144414d3b0912c29ab96f8f1c591d00319`; its HTTPS source archive
was independently downloaded and pinned to SHA-256
`340f03f495884611209e9c0bc943fad06ce920e8c79655aa228d5ca7418dc360`.
The archive has one top-level source tree and no traversal paths, links, or
special files. CI verifies the pinned hash before building.

The GitHub tag requires upstream Autotools regeneration. `%check` retains
`make check` and explicitly runs upstream `test-data/test.sh`, which extracts
and compares all included TNEF fixtures and checks specific parsed fields.
Upstream CI calls that script directly; it is not registered in Automake
`TESTS`. The installed-RPM smoke checks library initialization, public
headers and pkg-config, plus the command-line tools. It is narrower than
the full upstream fixture regression.

The library and tools retain the upstream GPL-2.0-or-later grant. The tools
subpackage includes the optional `ytnefprocess` Perl mail processor and its
module dependencies; no core utility is silently dropped. CI build
artifacts are not evidence of publication to the public RPM repository.

Target run `36501471769` at head `f371afbb` against main `51d28650` built
the complete RPM/SRPM set and passed upstream `make check` plus the full TNEF
fixture script. DNF installed `libytnef`, its tools/devel subpackages, and
the `MIME::Parser`/`Mail::Mailer` providers, but the installed public-header
smoke failed: `tnef-types.h` used `FILE` without `<stdio.h>` and `ytnef.h`
used `size_t` without `<stddef.h>`. Release 2 patches those two headers;
the smoke program and all tests remain unchanged. A new target CI run must
prove the repair before this PR is merge-ready.
