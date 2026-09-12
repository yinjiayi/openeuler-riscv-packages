<!-- SPDX-License-Identifier: Apache-2.0 -->
# recutils

This directory packages GNU recutils `1.9` for openEuler 24.03 LTS SP3 on
`riscv64`/RVA23. The official GNU archive is pinned by SHA-256
`6301592b0020c14b456757ef5d434d49f6027b8e5f3a499d13362f205c486e0e`.
It has one `recutils-1.9` root, 983 members, and no absolute paths, parent
traversal, links, or special files. GNU's detached signature was independently
verified with `gpgv` and the official GNU keyring against Jose E. Marchesi's
RSA key fingerprint `BDFA 5717 FC1D D35C 2C38 32A2 3EF9 0523 B304 AF08`.
SHA-256 remains the reproducible CI source gate; the advisory signature is not
a second build input.

Snapshot `discovery-20260808T165000Z-9a89920c269462cd` freezes Fedora 44
`1.9-13.fc44`, openSUSE Tumbleweed `1.9-3.5`, Ubuntu 26.04 LTS `1.9-4`, and
read-only AUR RPC metadata for `recutils` `1.9-2`. The catalog does not yet
contain a reviewed recutils release overlay, so this package records a separate
official-source review rather than claiming catalog-reviewed status. No AUR
PKGBUILD or distribution packaging recipe was read or executed.

The runtime package contains the nine recfile/CSV tools, the `librec.so.1`
library, translations, and `FSD.rec` system descriptor. `recutils-devel`
contains the public C header and linker name, while `recutils-bash-builtins`
contains the `readrec` and `testrec` loadable Bash modules. The target
repository has no mdbtools development package, so upstream's conditional
`mdb2rec` utility is not built; it is not replaced with the unrelated LMDB
library. Encryption, remote descriptors, UUID field types, and Bash builtins
remain enabled through their available target dependencies.

`%check` runs the complete upstream C torture and shell utility suites without
test exclusions. Installed smoke performs a typed recfile query, a CSV-to-rec
and rec-to-CSV round trip, a public `librec` API compile/link/run check, and a
Bash loadable-builtin load check. Package CI may use the network while fetching
the pinned source, resolving BuildRequires, and running the target RPM build;
the source SHA-256 gate remains mandatory and no downloaded build output is
committed to this package directory.

External source licenses remain those of upstream. Apache-2.0 covers only the
original packaging metadata, test, and documentation in this directory.
