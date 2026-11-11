# Libnsgif 1.0.0

Official NetSurf fixed release SHA-256
`6014c842f61454d2f5a0f8243d7a8d7bde9b7da3ccfdca2d346c7c0b2c4c061b`.
All 303 source files, GIF/PPM corpus files, MIT COPYING, and ISC test CLI
copyright notices are preserved. Source1 supplies the full ISC permission
text from a fixed SPDX commit; it is license data, not executable test code.
Frozen Arch extra 1.0.0-2 is discovery lineage, not executable source proof.

Keep the upstream default static build and original `make test`; add shared
build/test without changing warning errors, script, driver or corpus.
Staged and installed replays compile the original test/nsgif.c, which includes
the original ISC cli.c, against installed shared and static libraries.
Compare installed nsgif.h, verify shared SONAME and run the complete original
test script from the source root. The script counts malformed-GIF decoder
rejections as Fail but exits unsuccessfully on Error (signals or reference
PPM mismatches). Preserve that original distinction; a passing script does
not mean every malformed input decoded successfully. No filtering or shell
errexit is imposed on the upstream script. Replay logs and summary remain
visible in build/install logs.

NetSurf buildsystem >=1.10 is a repository dependency. No local source,
RPM or QEMU build was run. Exact-head target CI, physical RPM/SRPM and
installation evidence remain required before acceptance or merge.
