# libjson

Official `vincenthz/libjson` stable `v0.8`, fixed commit
`2bbe73f129ebf3eafd9b194f960536c146e680c2`. All 52 official Git blobs
match the pinned archive; no available tag or commit signature was observed.
The discovery snapshot's rolling `0.8.r54.ga63d882` is lineage, not this release.

The original source headers explicitly offer **LGPL-2.1-only OR LGPL-3.0-only**.
The archive contains the copyright/grant but no full license copies. Four fixed
official FSF text sources supply LGPL2.1, GPL2, LGPL3 and its incorporated GPL3;
all are SHA-256 checked and shipped as license documents. This does not change
the original grant. The original copyright/grant block is also installed.

The four complete FSF companion texts use fixed official GNU primary archive
URLs under `https://ftp.gnu.org/gnu/Licenses/` (lowercase versioned `.txt`
filenames). Their full bytes and SHA-256 digests are unchanged. This retrieval
change addresses the observed pre-build `www.gnu.org` network-unreachable
failure; it does not change the upstream grant, source, recipe or tests.
Owned QA is separately MIT-licensed with its complete text in the devel RPM.
Debian packaging files are neither reused nor installed.

Keep every default product: static archive, shared library with the original
`libjson.so.0.8.0` SONAME and relative symlink chain, `jsonlint`, public header,
pkg-config metadata, streaming parser/printer and DOM helper. Packaging patch0
adds default-`lib` LIBDIR selection (the target uses lib64), corrects missing
pkg-config variable sigils, and makes the CLI honor caller LDFLAGS. It does not
change library algorithms, header version macros, original fixtures or runner.
Upstream's header still reports JSON_MINOR=7 although the release/PC is 0.8.
Normal RPM optimization/debug flags and all generated debug output remain.

`%check` runs the unchanged upstream `make tests` target: 21 good and 12 bad
fixtures, with upstream comments enabled. Because its runner prints FAILED but
returns zero, packaging additionally rejects FAILED and requires all 33 SUCCESS
markers. Installed QA repeats that original runner and strict expected 0/1
fixture exits for both original installed CLI and original CLI source relinked
against the installed library/header. Both shared and explicit static downstream
consumers check representative streaming chunk/char events, parser state/error
and raw printer output. Format/DOM CLI smoke uses stdout with one small document.
These added checks are downstream tests, not a new upstream suite or a security,
full JSON conformance, performance, hardware or native RISC-V claim.

Patch1 materializes exact owned QA files into the unpacked source because build
staging copies only declared sources and patch-series files, not arbitrary
recipe `tests/` entries. Inert GNU patch application with fuzz=0 and byte-for-byte
comparison to the retained tests files verifies this contract. Original source,
all fixtures and test loop bytes remain unchanged. Installed files are checksum
checked; smoke verifies both RPM payloads before repeating installed QA.

Local validation executes trusted repository tooling and source-only checks,
never this upstream code, RPM or QEMU. Actual target compilation, all original
tests, installation, complete debug co-installation and physical RPM/SRPM
acceptance remain hosted CI/merge gates. Target provider metadata joins are not
a claim that DNF solved or installed the package.
