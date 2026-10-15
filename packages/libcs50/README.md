<!-- SPDX-License-Identifier: Apache-2.0 -->
# libcs50

This directory packages upstream `https://github.com/cs50/libcs50` version `11.0.4` for openEuler 24.03 LTS SP3 on `riscv64`/RVA23.

External source and patch licenses remain those of their respective upstream projects. The repository license only covers original packaging metadata, scripts, and documentation.

The fixed official `v11.0.4` commit is `37709b01398c9d72a112b864f12c789a910c61fb`;
its complete 20-file archive SHA-256 is
`0be59548bab8333842cd74931ad4970beafcaae254882fbbe00a65349ad49dcd`.
No gitlinks or borrowed packaging recipes are used. Historical discovery
`libcs50-git` was VCS-only; this recipe instead verifies the actual stable tag.

The original default is `make all`: shared SONAME 11, static archive,
header, full C implementation and all seven manuals are retained. Serial
make avoids upstream's shared multiple-output rule. Upstream's install
prefix/`lib`/ldconfig convention is staged into RPM `lib64`; no host ldconfig
is run during staging. No native/kernel/hardware claim is made.

Upstream registers no test target. Both shipped sample programs are retained
and executed; the only patch supplies `NULL` for obsolete zero-argument
calls to the current prompt API. It changes no library code or assertions,
is generic rather than RISC-V-specific, is not submitted upstream, and can
be removed when an official release fixes those calls.

Additional downstream input checks cover all seven API values, all seven
EOF sentinels, CRLF/CR/LF, empty and unterminated final lines. Each source,
staged and RPM-installed phase checks shared and static linkage, both
original samples, exact outputs, invalid/overflow integer retry and no
skips. Explicit C failure branches do not depend on `assert`/`NDEBUG`.
The installed smoke also verifies RPM ownership/checksums, loader provenance,
the header, archive, complete notices and seven valid compressed manuals.

The runtime/header contain complete BSD-3-Clause notices, retained literally
as `%license` and in installed source/header. Root `LICENSE` is the full GPLv3
text, retained conservatively for unmarked upstream material and the sample
compatibility patch. The declaration is `BSD-3-Clause AND GPL-3.0-only`;
the Makefile's old fpm `MIT` field is not treated as a source license grant.

Target provider names and complete official/supplemental filelists are
checked before admission. Local validation executes only trusted repository
tests and inert source verification. Actual DNF, build, sample/input checks
and physical RPM/SRPM acceptance remain exact-head hosted CI gates; this
initial recipe does not claim those gates already passed.
